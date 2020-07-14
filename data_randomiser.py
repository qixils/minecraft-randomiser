import os
import shutil
import random
import sys
import json
import argparse
import datetime
import collections
import collections.abc

parser = argparse.ArgumentParser(description='Randomise the data of a Minecraft datapack folder.')
parser.add_argument('-f', '--folder', default='data', type=str, dest='data', help='specifies the data folder')
parser.add_argument('-s', '--seed', default=int(datetime.datetime.timestamp(datetime.datetime.now())), type=int, dest='seed', help='specifies a random seed')
parser.add_argument('-r', '--randomlootamountmax', default='0', type=int, dest='randomlootamount', help='randomized loot amount max - 0 for no')
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
randomlootamount = args.randomlootamount

random.seed(randomseed)
def print2(toprint, toupdate=False):
    global longestbar
    if toupdate:
        if len(toprint) > longestbar:
            longestbar = len(toprint)
        print(toprint.ljust(longestbar, ' '), end='\r', flush=True)
    else:
        print(toprint.ljust(longestbar, ' '))
        longestbar = 0
longestbar = 0

if datafolder == "shuffle":
    print("The input data folder may not be named 'shuffle'.")
    input('Press any key to exit.')
    sys.exit()
if os.path.exists("shuffle"):
    print("Please remove the 'shuffle' folder before running this program.")
    input('Press any key to exit.')
    sys.exit()

def makepath(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            print('DEBUG: tried to create an existing folder')

if not (randomiseadvancements or randomiseloottables or randomiserecipes or randomisestructures or randomisetags):
    print('Successfully randomised nothing!')
    sys.exit()
if not os.path.exists(datafolder):
    makepath(datafolder)
    print('Unable to locate data pack folder! Please make sure you have downloaded the data pack files in the "'+datafolder+'" folder.')
    input('Press any key to exit.')
    sys.exit()
# if not os.path.exists(datafolder+'/assets'):
    # print('Unable to locate resource pack folder! Please ensure you have extracted one properly, you should have an "assets" folder in the "'+datafolder+'" folder.')
    # input('Press any key to exit.')
    # sys.exit()

print2(f"Preparing data")

advlist = []
advancements = {'icons': [], 'names': [], 'criteria': [], 'criteria_count': [], 'rewards': []}
loottables = []
specialbois = []
recipes = []
structures = []
tags = {'blocks': [], 'entity_types': [], 'fluids': [], 'items': []}

#find the files to swap
for dirpath, dirs, files in os.walk(datafolder):
    for file in files:
        fullfilepath = os.path.join(dirpath,file)

        if dirpath.startswith(os.path.join(datafolder,'advancements')) and randomiseadvancements:
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
        elif dirpath.startswith(os.path.join(datafolder,'loot_tables')) and randomiseloottables:
            loottables.append(fullfilepath)
        elif dirpath == os.path.join(datafolder,"recipes") and randomiserecipes:
            recipes.append(fullfilepath)
        elif dirpath.startswith(os.path.join(datafolder,"structures")) and randomisestructures:
            structures.append(fullfilepath)
        # unstable, would need to work out how to avoid looping back on itself somehow
        # elif dirpath.startswith(datafolder+"/tags") and randomisetags:
            # tags[dirpath.split('/')[2]].append(fullfilepath)

print2(f"Random Seed: {randomseed}")
def shuffler(randoBool, toRando, inputType):
    if randoBool and toRando != []:
        print2("Randomising "+inputType, True)
        shufflelist = list(toRando)
        random.shuffle(shufflelist)
        filecount = 0
        while filecount < len(toRando):
            destfile = os.path.join('shuffled','data','minecraft')
            for newpath in toRando[filecount].split(os.path.sep)[1:]:
                destfile = os.path.join(destfile,newpath)

            progressbar = f"Randomising {inputType}: {filecount} of {len(toRando)}: {toRando[filecount].split(os.path.sep)[::-1][0]} -> {destfile.split(os.path.sep)[::-1][0]}"
            print2(progressbar, False)

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
                            if preserveloot:
                                for rollentry in pool['entries']:
                                    if 'functions' in rollentry:
                                        for func in rollentry['functions']:
                                            if randomlootamount>=1:
                                                if 'count' in func:
                                                        func['count']={"min": 1,"max": randomlootamount,"type": "minecraft:uniform"}
                                                else:
                                                    pool['rolls']={"min": 1,"max": randomlootamount,"type": "minecraft:uniform"}
                                            else:
                                                if 'count' in func:
                                                    if not isinstance(func['count'], int):
                                                        if 'min' in func['count']:
                                                            if func['count']['min'] <= 1:
                                                                func['count']['min'] = 1
                                                    else:
                                                        if func['count'] <= 1:
                                                            func['count'] = 1
                                else:
                                    if randomlootamount>=1:
                                        pool['rolls']={"min": 1,"max": randomlootamount,"type": "minecraft:uniform"}

                        with open(destfile, 'w') as outputloot:
                            json.dump(entitty, outputloot)
            else:
                shutil.copyfile(shufflelist[filecount], destfile)
            filecount += 1
        print2('Randomised '+inputType)

if randomiseadvancements and advancements != {'icons': [], 'names': [], 'criteria': [], 'criteria_count': [], 'rewards': []}:
    print2("Randomising advancements", True)
    random.shuffle(advlist)
    for advorigfile in advlist:
        destfile = os.path.join('shuffled','data','minecraft')
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
                    print(key,value,"\n")
                    #requirements.append([key])
                    if 'conditions' in value:
                        if value['conditions'] != {}:
                            for subkey, subvalue in value['conditions'].items():
                                if subkey == 'items' or subkey == 'victims':
                                    """ 
                                    itemlist = []
                                    for itemdict in subvalue:
                                        if 'count' in itemdict:
                                            itemlist.append(f"{itemdict['item'].replace('minecraft:','')} x{itemdict['count']['min']}")
                                        else:
                                            for subsubkey, subsubvalue in itemdict.items():
                                                itemlist.append(subsubvalue.replace('minecraft:', ''))
                                    conditions.append(f"{subkey}:{'+'.join(itemlist)}") """
                                    pass
                                elif subkey == 'item':
                                    conditions.append(f"{subkey}:{subvalue}")
                                elif subkey == 'entity' or subkey == 'parent':
                                    for eachsubvalue in subvalue:
                                        if 'catType' in eachsubvalue['predicate']:
                                            conditions.append(f"cat:{eachsubvalue['predicate']['catType'].split('/')[::-1][0].split('.')[0]}")
                                        else:
                                            for oneofthekeysinsubvalue,oneofthevaluesinsubvalue in eachsubvalue.items():
                                                conditions.append(f"{subkey}:{eachsubvalue['predicate']['type'].replace('minecraft:','')}")
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
                                        efectz.append(effecc.replace('minecraft:',''))
                                    conditions.append(f"{subkey}:{'+'.join(efectz)}")
                                elif subkey == 'level' and isinstance(subvalue, collections.abc.Mapping):
                                    for subsubkey, subsubvalue in subvalue.items():
                                        conditions.append(f"{subkey}:{subsubkey}={subsubvalue}")
                                elif isinstance(subvalue,list):
                                    subvalue = ((str(subvalue)))
                                    conditions.append(f"{subkey}:{subvalue}")
                                    pass
                                elif isinstance(subvalue,str):
                                    conditions.append(f"{subkey}:{subvalue}")
                                    pass
                                elif isinstance(subvalue,int):
                                    conditions.append(f"{subkey}:{subvalue}")
                                    pass
                                elif isinstance(subvalue,dict):
                                    for keysoftherest,valuesoftherest in subvalue.items():
                                        if isinstance(valuesoftherest,dict):
                                            temp=[]
                                            for fixvalue in valuesoftherest:
                                                fixvalue.replace('minecraft:', '')
                                                temp.append(str(fixvalue))
                                            conditions.append(f"{keysoftherest}:{temp}")
                                        else:
                                            conditions.append(f"{keysoftherest}:{valuesoftherest}")
                                    else:
                                        conditions.append(f"{keysoftherest}:{valuesoftherest}")
                                else:
                                    conditions.append(f"{subkey}:{subvalue}")
                                    pass
                        else:
                            conditions.append(value['trigger'].replace('minecraft:',''))
                    else:
                        #print(value)
                        conditions.append(value['trigger'].replace('minecraft:',''))
            advjson['criteria'] = criterias
            #advjson['requirements'] = requirements # requirements are optional
            advjson.pop('requirements', None) # TODO: requirement randomization?
            advjson['display']['description'].pop('translate', None)
            advjson['display']['description']['text'] = ', '.join(conditions)
            makepath(destfile)
            with open(destfile, 'w') as truedestlol:
                json.dump(advjson, truedestlol)
    print2("Randomised advancements")
shuffler(randomiseloottables, loottables, "loot tables")
shuffler(randomiserecipes, recipes, "recipes")
shuffler(randomisestructures, structures, "structures")
# for tagkey, tagvalue in tags.items():
    # shuffler(randomisetags, tagvalue, f"tags [{tagkey}]")

print('Writing meta files')

makepath(os.path.join('shuffled','pack.mcmeta'))
with open(os.path.join('shuffled','pack.mcmeta'), "w") as descfile:
    descfile.write('{"pack":{"pack_format": 5,"description": "MC Data Randomizer, Seed: '+str(randomseed)+'"}}')

initfilepath = os.path.join('shuffled','data',f'random_data_{randomseed}','functions','reset.mcfunction')
makepath(initfilepath)
with open(initfilepath, "w") as initfile:
    initfile.write('tellraw @a ["",{"text":"Data file randomiser by lexikiq - Aikoyori tries to fix this \n Seed '+str(randomseed)+'","color":"green"}]')
    #initfile.write('tellraw @a ["",{"text":"Data file randomiser by lexikiq","color":"green"}]')

loadjspath = os.path.join('shuffled','data','minecraft','tags','functions','load.json')
makepath(loadjspath)
with open(loadjspath, "w") as loadfile:
    loadfile.write('{"values": ["random_data_'+str(randomseed)+':reset"]}')

print('Compressing')

try:
    system = sys.platform.lower()
    if system.startswith('linux'):
        destfolder = os.path.expanduser(os.path.join('~','.minecraft','saves','WORLD_HERE','datapacks'))
    elif system.startswith('darwin'):
        destfolder = os.path.expanduser(os.path.join('~','Library','Application Support','minecraft','saves','WORLD_HERE','datapacks'))
    elif system.startswith('win'):
        destfolder = os.path.join('%APPDATA%','.minecraft','saves','WORLD_HERE','datapacks')
    else:
        destfolder = '*failed to identify OS*'
    printmsg = "File output at "+'random_data_'+str(randomseed)+"! Please copy over to your world's 'datapacks' folder \n OR install in upon world creation screen."
    if destfolder != '':
        printmsg += f" ({destfolder})"
    shutil.make_archive('random_data_'+str(randomseed), 'zip', 'shuffled')
    print(printmsg)
    shutil.rmtree('shuffled')
except Exception as e:
    print('Compression failed! Please manually move the "shuffled" folder to your datapacks folder.')
