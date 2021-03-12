import os
import shutil
import random
import sys
import json
import argparse
import collections
import collections.abc
import logging


def main():
    parser = argparse.ArgumentParser(description='Randomise the data of a Minecraft datapack folder.')
    parser.add_argument('-f', '--folder', default='data', type=str, dest='data', help='specifies the data folder')
    parser.add_argument('-s', '--seed', default=random.randrange(sys.maxsize), type=int, dest='seed', help='specifies a random seed')
    parser.add_argument('--noadvancements', action='store_false', dest='advancements', help='disables randomised advancements')
    parser.add_argument('--noloottables', action='store_false', dest='loottables', help='disables randomised loot tables')
    parser.add_argument('--preservechances', action='store_false', dest='lootchances', help='[loot] preserves normal loot chances instead of guranteed chance')
    parser.add_argument('--norecipes', action='store_false', dest='recipes', help='disables randomised recipes')
    parser.add_argument('--notags', action='store_false', dest='tags', help='disables randomised tags')
    parser.add_argument('--structures', action='store_true', dest='structures', help='enables randomised structures (may crash)')

    args = parser.parse_args()
    datafolder = args.data
    randomseed = args.seed
    randomiseadvancements = args.advancements
    randomiseloottables = args.loottables
    randomiserecipes = args.recipes
    randomisestructures = args.structures
    randomisetags = args.tags
    preserveloot = args.lootchances
    return run(datafolder, randomseed, randomiseadvancements, randomiseloottables, randomiserecipes,
               randomisestructures, randomisetags, preserveloot)


if __name__ == '__main__':
    print(main())
    input('Press any key to exit.')
    sys.exit()


def run(data_folder: str, seed, randomize_advancements: bool, randomize_loot_tables: bool, randomize_recipes: bool,
        randomize_structures: bool, randomize_tags: bool, preserve_loot: bool, out_dir: str = 'shuffled'):
    random.seed(seed)

    if data_folder == "shuffle":
        return "The input data folder may not be named 'shuffle'."
    if os.path.exists("shuffle"):
        return "Please remove the 'shuffle' folder before running this program."

    def makepath(path):
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except:
                logging.debug('tried to create an existing folder')

    if not (randomize_advancements or randomize_loot_tables or randomize_recipes or randomize_structures or randomize_tags):
        return 'Successfully randomised nothing!'
    if not os.path.exists(data_folder):
        makepath(data_folder)
        return 'Unable to locate data pack folder! Please make sure you have downloaded the data pack files in the "'+data_folder+'" folder.'
    # if not os.path.exists(datafolder+'/assets'):
        # print('Unable to locate resource pack folder! Please ensure you have extracted one properly, you should have an "assets" folder in the "'+datafolder+'" folder.')
        # input('Press any key to exit.')
        # sys.exit()

    logging.info(f"Preparing data")

    advlist = []
    advancements = {'icons': [], 'names': [], 'criteria': [], 'criteria_count': [], 'rewards': []}
    loottables = []
    recipes = []
    structures = []

    # find the files to swap
    for dirpath, dirs, files in os.walk(data_folder):
        for file in files:
            fullfilepath = os.path.join(dirpath, file)

            if dirpath.startswith(os.path.join(data_folder, 'advancements')) and randomize_advancements:
                with open(fullfilepath, 'r') as advfile:
                    advdata = json.loads(advfile.read())
                    thisshallpass = True
                    # for key, value in advdata['criteria'].items():
                        # if value['trigger'] == 'minecraft:impossible':
                            # thisshallpass = False

                    if thisshallpass and 'display' in advdata and 'criteria' in advdata: # some things don't have displays somehow so just ignore them. also ignore the impossible advancement(s) because wtf
                        advlist.append(fullfilepath)
                        for key, value in advdata['criteria'].items():
                            advancements['criteria'].append({key: value})
                        advancements['icons'].append(advdata['display']['icon'])
                        advancements['names'].append(advdata['display']['title'])
                        if 'rewards' in advdata:
                            advancements['rewards'].append(advdata['rewards'])
                        else:
                            advancements['rewards'].append({})
                        advancements['criteria_count'].append(len(advdata['criteria']))
            elif dirpath.startswith(os.path.join(data_folder, 'loot_tables')) and randomize_loot_tables:
                loottables.append(fullfilepath)
            elif dirpath == os.path.join(data_folder, "recipes") and randomize_recipes:
                recipes.append(fullfilepath)
            elif dirpath.startswith(os.path.join(data_folder,"structures")) and randomize_structures:
                structures.append(fullfilepath)
            # unstable, would need to work out how to avoid looping back on itself somehow
            # elif dirpath.startswith(datafolder+"/tags") and randomisetags:
                # tags[dirpath.split('/')[2]].append(fullfilepath)

    logging.info(f"Random Seed: {seed}")

    def shuffler(randoBool, toRando, inputType):
        if randoBool and toRando != []:
            logging.info("Randomising "+inputType)
            shufflelist = list(toRando)
            random.shuffle(shufflelist)
            filecount = 0
            while filecount < len(toRando):
                destfile = os.path.join(out_dir,'data','minecraft')
                for newpath in toRando[filecount].split(os.path.sep)[1:]:
                    destfile = os.path.join(destfile,newpath)

                makepath(destfile)
                if inputType == 'recipes':
                    with open(shufflelist[filecount], 'r') as recipefile:
                        recipejson = json.loads(recipefile.read())
                        with open(toRando[filecount], 'r') as destresult:
                            destresultjson = json.loads(destresult.read())
                            if 'result' in recipejson and 'result' in destresultjson:
                                origresult = recipejson['result']
                                if (isinstance(recipejson['result'], collections.abc.Mapping) and isinstance(destresultjson['result'], collections.abc.Mapping)) or (isinstance(recipejson['result'], str) and isinstance(destresultjson['result'], str)):
                                    recipejson['result'] = destresultjson['result']
                                elif isinstance(destresultjson['result'], collections.abc.Mapping) and isinstance(recipejson['result'], str):
                                    recipejson['result'] = destresultjson['result']['item']
                                else:# isinstance(destresultjson['result'], str) and isinstance(recipejson['result'], collections.abc.Mapping):
                                    recipejson['result']['item'] = destresultjson['result']
                                if isinstance(recipejson['result'], collections.abc.Mapping) and isinstance(origresult, collections.abc.Mapping):
                                    if 'count' in origresult:
                                        recipejson['result']['count'] = origresult['count']
                                with open(destfile, 'w') as destrecipe:
                                    json.dump(recipejson, destrecipe)
                elif inputType == 'loot tables':# and '/entities/' in shufflelist[filecount]:
                    with open(shufflelist[filecount], 'r') as mainloot:
                        entitty = json.loads(mainloot.read())
                        if 'pools' in entitty:
                            for pool in entitty['pools']:
                                pool.pop('conditions', None)
                                if preserve_loot:
                                    for rollentry in pool['entries']:
                                        if 'functions' in rollentry:
                                            for func in rollentry['functions']:
                                                if 'count' in func:
                                                    if not isinstance(func['count'], int):
                                                        if 'min' in func['count']:
                                                            if func['count']['min'] <= 1:
                                                                func['count']['min'] = 1
                                                    else:
                                                        if func['count'] <= 1:
                                                            func['count'] = 1
                            with open(destfile, 'w') as outputloot:
                                json.dump(entitty, outputloot)
                else:
                    shutil.copyfile(shufflelist[filecount], destfile)
                filecount += 1
            logging.info('Randomised '+inputType)

    if randomize_advancements and advancements != {'icons': [], 'names': [], 'criteria': [], 'criteria_count': [], 'rewards': []}:
        logging.info("Randomising advancements")
        random.shuffle(advlist)
        for advorigfile in advlist:
            destfile = os.path.join(out_dir, 'data', 'minecraft')
            for newpath in advorigfile.split(os.path.sep)[1:]:
                destfile = os.path.join(destfile,newpath)
            with open(advorigfile, 'r') as destadv:
                advjson = json.loads(destadv.read())
                advjson['display']['show_toast'] = True
                advjson['display']['announce_to_chat'] = True
                advjson['display']['hidden'] = False
                advjson['display']['frame'] = random.choice(['task', 'challenge', 'goal'])
                advjson['display']['title'] = advancements['names'].pop(random.randrange(len(advancements['names'])))
                advjson['display']['icon'] = advancements['icons'].pop(random.randrange(len(advancements['icons'])))
                advjson['rewards'] = advancements['rewards'].pop(random.randrange(len(advancements['rewards'])))
                criteria_grabbed = 0
                criteria_tograb = advancements['criteria_count'].pop(random.randrange(len(advancements['criteria_count'])))
                criterias = {}
                conditions = []
                #requirements = []
                while criteria_grabbed < criteria_tograb:
                    criteria_grabbed += 1
                    crit = advancements['criteria'].pop(random.randrange(len(advancements['criteria'])))
                    criterias = {**criterias, **crit}
                    for key, value in crit.items():
                        #requirements.append([key])
                        if 'conditions' in value:
                            if value['conditions'] != {}:
                                for subkey, subvalue in value['conditions'].items():
                                    if subkey == 'items' or subkey == 'victims':
                                        itemlist = []
                                        for itemdict in subvalue:
                                            if 'count' in itemdict:
                                                itemlist.append(f"{itemdict['item'].replace('minecraft:','')} x{itemdict['count']['min']}")
                                            else:
                                                for subsubkey, subsubvalue in itemdict.items():
                                                    itemlist.append(subsubvalue.replace('minecraft:', ''))
                                        conditions.append(f"{subkey}:{'+'.join(itemlist)}")
                                    elif subkey == 'item':
                                        conditions.append(f"{subkey}:{subvalue['item'].replace('minecraft:', '')}")
                                    elif subkey == 'entity' or subkey == 'parent':
                                        if 'catType' in subvalue:
                                            conditions.append(f"cat:{subvalue['catType'].split('/')[::-1][0].split('.')[0]}")
                                        else:
                                            conditions.append(f"{subkey}:{subvalue['type'].replace('minecraft:','')}")
                                    elif subkey == 'slots' or subkey == 'distance':
                                        for subsubkey, subsubvalue in subvalue.items():
                                            for subsubsubkey, subsubsubvalue in subsubvalue.items():
                                                conditions.append(f"{subkey} {subsubkey} {subsubsubkey}:{subsubsubvalue}")
                                    elif subkey == 'damage' or subkey == 'killing_blow':
                                        outpoop = 'damage:'
                                        if 'type' in subvalue:
                                            dmgtypes = []
                                            for subsubkey, subsubvalue in subvalue['type'].items():
                                                if isinstance(subsubvalue, collections.abc.Mapping):
                                                    for subsubsubkey, subsubsubvalue in subsubvalue.items():
                                                        dmgtypes.append(f"{subsubkey}={subsubsubvalue.replace('minecraft:', '')}")
                                                else:
                                                    dmgtypes.append(f"{subsubkey}={subsubvalue}")
                                            outpoop += '+'.join(dmgtypes)
                                        for scoobakey, doobavalue in subvalue.items():
                                            if scoobakey != 'type':
                                                if not isinstance(doobavalue, collections.abc.Mapping):
                                                    outpoop += f"/{scoobakey}={doobavalue}"
                                                else:
                                                    for muffinsis, prettycool in doobavalue.items():
                                                        outpoop += f"/{scoobakey}={prettycool.replace('minecraft:', '')}"
                                        conditions.append(f"{subkey}:{outpoop}")
                                    elif subkey == 'effects':
                                        efectz = []
                                        for effecc in subvalue:
                                            efectz.append(effecc.replace('minecraft:', ''))
                                        conditions.append(f"{subkey}:{'+'.join(efectz)}")
                                    elif subkey == 'level' and isinstance(subvalue, collections.abc.Mapping):
                                        for subsubkey, subsubvalue in subvalue.items():
                                            conditions.append(f"{subkey}:{subsubkey}={subsubvalue}")
                                    else:
                                        if isinstance(subvalue, int):
                                            subvalue = str(subvalue)
                                        conditions.append(f"{subkey}:{subvalue.replace('minecraft:', '')}")
                            else:
                                conditions.append(value['trigger'].replace('minecraft:', ''))
                        else:
                            #print(value)
                            conditions.append(value['trigger'].replace('minecraft:', ''))
                advjson['criteria'] = criterias
                #advjson['requirements'] = requirements # requirements are optional
                advjson.pop('requirements', None)  # TODO: requirement randomization?
                advjson['display']['description'].pop('translate', None)
                advjson['display']['description']['text'] = ', '.join(conditions)
                makepath(destfile)
                with open(destfile, 'w') as truedestlol:
                    json.dump(advjson, truedestlol)
        logging.info("Randomised advancements")
    shuffler(randomize_loot_tables, loottables, "loot tables")
    shuffler(randomize_recipes, recipes, "recipes")
    shuffler(randomize_structures, structures, "structures")
    # for tagkey, tagvalue in tags.items():
        # shuffler(randomisetags, tagvalue, f"tags [{tagkey}]")

    logging.info('Writing meta files')

    makepath(os.path.join(out_dir, 'pack.mcmeta'))
    with open(os.path.join(out_dir, 'pack.mcmeta'), "w") as descfile:
        descfile.write('{"pack":{"pack_format": 1,"description": "MC Data Randomizer, Seed: '+str(seed)+'"}}')

    initfilepath = os.path.join(out_dir, 'data', f'random_data_{seed}', 'functions', 'reset.mcfunction')
    makepath(initfilepath)
    with open(initfilepath, "w") as initfile:
        initfile.write('tellraw @a ["",{"text":"Data file randomiser by lexikiq / Seed '+str(seed)+'","color":"green"}]')

    loadjspath = os.path.join(out_dir, 'data', 'minecraft', 'tags', 'functions', 'load.json')
    makepath(loadjspath)
    with open(loadjspath, "w") as loadfile:
        loadfile.write('{"values": ["random_data_'+str(seed)+':reset"]}')

    logging.info('Compressing')

    try:
        system = sys.platform.lower()
        if system.startswith('linux'):
            destfolder = os.path.expanduser(os.path.join('~', '.minecraft', 'saves', 'WORLD_HERE', 'datapacks'))
        elif system.startswith('darwin'):
            destfolder = os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'minecraft', 'saves', 'WORLD_HERE', 'datapacks'))
        elif system.startswith('win'):
            destfolder = os.path.join('%APPDATA%', '.minecraft', 'saves', 'WORLD_HERE', 'datapacks')
        else:
            destfolder = ''
        printmsg = "File output at random_data.zip! Please copy over to your world's 'datapacks' folder"
        if destfolder != '':
            printmsg += f" ({destfolder})"
        shutil.make_archive('random_data', 'zip', out_dir)
        shutil.rmtree(out_dir)
        return printmsg
    except Exception:
        return f'Compression failed! Please manually move the "{out_dir}" folder to your datapacks folder.'
