import os
import shutil
import random
import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Randomise the assets of a Minecraft resource pack.')
parser.add_argument('-p', '--pack', default='pack', type=str, dest='pack', help='specifies a resource pack folder')
parser.add_argument('-s', '--seed', default=random.randrange(sys.maxsize), type=int, dest='seed', help='specifies a random seed')
#parser.add_argument('--noanimations', action='store_false', dest='animations', help='disables animations, fixes some missing textures')
parser.add_argument('--alttextures', action='store_true', dest='alttextures', help='alternative texture randomization, only swaps blocks with other blocks, items with items, etc. supports animated textures')
parser.add_argument('--notextures', action='store_false', dest='textures', help='disables randomised textures')
parser.add_argument('--noblockstates', action='store_false', dest='blockstates', help='disables randomised block states')
parser.add_argument('--nosounds', action='store_false', dest='sounds', help='disables randomised sounds')
parser.add_argument('--notexts', action='store_false', dest='texts', help='disables randomised text')
parser.add_argument('--nofonts', action='store_false', dest='fonts', help='disables randomised fonts')
parser.add_argument('--noshaders', action='store_false', dest='shaders', help='disables randomised shaders')
parser.add_argument('--models', action='store_true', dest='models', help='EXPERIMENTAL: randomised block/item models')

args = parser.parse_args()
resourcepack = args.pack
randomseed = args.seed
randomisetextures = args.textures
randomisemodels = args.models
#randomiseanimations = args.animations
randomiseblockstates = args.blockstates
randomisesounds = args.sounds
randomisetext = args.texts
randomisefont = args.fonts
randomiseshaders = args.shaders
alttextures = args.alttextures

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

if resourcepack == "shuffle":
    print("The input resource pack may not be named 'shuffle'.")
    input('Press any key to exit.')
    sys.exit()
if os.path.exists(os.path.join('shuffle')):
    print("Please remove the 'shuffle' folder before running this program.")
    input('Press any key to exit.')
    sys.exit()

def makepath(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            print('DEBUG: tried to create an existing folder')

if not (randomisetextures or randomisemodels or randomiseblockstates or randomisesounds or randomisetext or randomisefont or randomiseshaders):
    print('Successfully randomised nothing!')
    sys.exit()
if not os.path.exists(resourcepack):
    makepath(resourcepack)
    print('Unable to locate resource pack folder! Please make sure you have an extracted resource pack in the "'+resourcepack+'" folder.')
    input('Press any key to exit.')
    sys.exit()
if not os.path.exists(os.path.join(resourcepack, 'assets')):
    print('Unable to locate resource pack folder! Please ensure you have extracted one properly, you should have an "assets" folder in the "'+resourcepack+'" folder.')
    input('Press any key to exit.')
    sys.exit()

images = {}
randimages = {}
itemmodels = []
blockmodels = []
blockstates = []
sounds = []
randsounds = []
languages = []
specialtexts = []
shaders = {'vsh': [], 'fsh': [], 'json': []}
totaltextures = 0
longestbar = 0

def processimage(imagepath):
    #print(imagepath.replace('.png', '.mcmeta'))
    #if randomiseanimations or os.path.exists()
    if not alttextures:
        f = open(imagepath,mode='rb')
        header = f.read(26)
        f.close()
        width = int.from_bytes(header[16:20],'big',signed=False)
        height = int.from_bytes(header[20:24],'big',signed=False)
        dictkey = f"{width}x{height}"
        if dictkey not in images:
            images[dictkey] = []
        images[dictkey].append(imagepath)
    else:
        texturetype = imagepath.split(os.path.sep)[4]
        if texturetype not in images:
            images[texturetype] = []
        images[texturetype].append(imagepath)

#find the files to swap
for dirpath, dirs, files in os.walk(os.path.join(resourcepack,"assets")):
    for file in files:
        fullfilepath = os.path.join(dirpath,file)
        mcraft = os.path.join(resourcepack,'assets','minecraft')

        if file.endswith('.png') and (randomisefont or randomisetextures):
            if dirpath == os.path.join(mcraft,'textures','font') and randomisefont:
                processimage(fullfilepath)
                totaltextures += 1
            if dirpath != os.path.join(mcraft,'textures','font') and randomisetextures:
                processimage(fullfilepath)
                totaltextures += 1
        elif dirpath == os.path.join(mcraft,'models','item') and randomisemodels:
            itemmodels.append(fullfilepath)
        elif dirpath == os.path.join(mcraft,'models','block') and randomisemodels:
            blockmodels.append(fullfilepath)
        elif dirpath == os.path.join(mcraft,'blockstates') and randomiseblockstates:
            blockstates.append(fullfilepath)
        elif file.endswith('.ogg') and randomisesounds:
            sounds.append(fullfilepath)
        elif dirpath == os.path.join(mcraft,'lang') and randomisetext:
            languages.append(fullfilepath)
        elif dirpath == os.path.join(mcraft,'texts') and randomisetext:
            specialtexts.append(fullfilepath)
        elif dirpath == os.path.join(mcraft,'shaders','program') and randomiseshaders:
            shaders[file.split('.')[1]].append(fullfilepath)

print2(f"Random Seed: {randomseed}")
def shuffler(randoBool, toRando, inputType):
    if randoBool and toRando != []:
        print2("Randomising "+inputType, True)
        shufflelist = list(toRando)
        random.shuffle(shufflelist)
        filecount = 0
        while filecount < len(toRando):
            destfile = 'shuffled'
            for newpath in toRando[filecount].split(os.path.sep)[1:]:
                destfile = os.path.join(destfile,newpath)

            progressbar = f"Randomising {inputType}: {filecount+1} of {len(toRando)}: {shufflelist[filecount].split(os.path.sep)[::-1][0]} -> {destfile.split(os.path.sep)[::-1][0]}"
            print2(progressbar, True)

            makepath(destfile)
            shutil.copyfile(shufflelist[filecount], destfile)

            #for textures
            mcmeta = shufflelist[filecount]+'.mcmeta'
            mcdest = destfile+'.mcmeta'
            if os.path.exists(mcmeta):
                shutil.copyfile(mcmeta, mcdest)

            #model file
            #origmodel = textures[texturenum].split('/')[::-1][0].split('.')[0]+'.json'
            #shufmodel = shuffled[texturenum].split('/')[::-1][0].split('.')[0]+'.json'
            #blockpath = '/assets/minecraft/models/block/'
            #itempath = '/assets/minecraft/models/item/'
            #makepath('shuffled'+blockpath)
            #makepath('shuffled'+itempath)
            #if os.path.exists(resourcepack+blockpath+shufmodel):
            #    shutil.copyfile(resourcepack+blockpath+shufmodel, 'shuffled'+blockpath+origmodel)
            #if os.path.exists(resourcepack+itempath+shufmodel):
            #    shutil.copyfile(resourcepack+itempath+shufmodel, 'shuffled'+itempath+origmodel)

            #blockstates
            #statedir = '/assets/minecraft/blockstates/'
            #makepath('shuffled'+statedir)
            #if os.path.exists(resourcepack+statedir+shufmodel):
            #    shutil.copyfile(resourcepack+statedir+shufmodel,'shuffled'+statedir+origmodel)

            filecount += 1
        print2('Randomised '+inputType)

randoimagery = randomisetextures or randomisefont
for resolution, imagefiles in images.items():
    shuffler(randoimagery, imagefiles, f"textures ({resolution})")
shuffler(randomisemodels, itemmodels, "item models")  # can reduce more repeat code with a dict (ie unused tags code in data randomiser)
shuffler(randomisemodels, blockmodels, "block models")
shuffler(randomiseblockstates, blockstates, "block states")
shuffler(randomisesounds, sounds, "sounds")
for key, value in shaders.items():
    shuffler(randomiseshaders, value, f"shaders ({key})")

if randomisetext and (languages != [] or specialtexts != []):
    print2("Randomising text", True)
    langvalues = []

    for lang in languages:
        with open(lang, encoding='utf-8') as f:
            data = json.load(f)
        langvalues += list(data.values())

    for tfile in specialtexts:
        with open(tfile, encoding='utf-8') as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        langvalues += content

    processedlangs = 0
    totallangs = len(languages) + len(specialtexts)
    for lang in languages:
        processedlangs += 1
        progressbar = f"Randomising text: {processedlangs} of {totallangs}: {lang.split(os.path.sep)[::-1][0]}"
        print2(progressbar, True)

        with open(lang, encoding='utf-8') as f:
            data = json.load(f)
        shufflelang = {}
        for key in list(data.keys()):
            randindex = random.randint(0, len(langvalues)-1)
            shufflelang[key] = langvalues[randindex]
            del langvalues[randindex]
        destpath = 'shuffled'+lang[4:]
        makepath(destpath)
        with open(destpath, 'w', encoding='utf-8') as output:
            json.dump(shufflelang, output)

    for tfile in specialtexts:
        processedlangs += 1
        progressbar = f"Randomising text: {processedlangs} of {totallangs}: {lang.split(os.path.sep)[::-1][0]}"
        print2(progressbar, True)

        with open(tfile, encoding='utf-8') as f:
            content = f.readlines()
        linesadded = 0
        outputlines = []
        while linesadded < len(content):
            randindex = random.randint(0, len(langvalues)-1)
            outputlines.append(langvalues[randindex])
            del langvalues[randindex]
            linesadded += 1
        destpath = 'shuffled'+tfile[4:]
        makepath(destpath)
        with open(destpath, 'w', encoding='utf-8') as output:
            output.write('\n'.join(outputlines))

    print2("Randomised text")

print2("Creating meta files")
if "16x16" in images.keys():
    shutil.copyfile(random.choice(images["16x16"]), os.path.join('shuffled','pack.png'))
elif os.path.exists(os.path.join(resourcepack,'pack.png')):
    shutil.copyfile(os.path.join(resourcepack,'pack.png'), os.path.join('shuffled','pack.png'))

makepath(os.path.join('shuffled','pack.mcmeta'))
with open(os.path.join('shuffled','pack.mcmeta'), "w") as descfile:
    descfile.write('{"pack":{"pack_format":4,"description":"Minecraft Shuffled by lexikiq"}}')

print2('Installing to resource pack folder')

try:
    system = sys.platform.lower()
    if system.startswith('linux'):
        destfolder = os.path.expanduser(os.path.join('~', '.minecraft', 'resourcepacks', 'shuffle'))
    elif system.startswith('darwin'):
        destfolder = os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'minecraft', 'resourcepacks', 'shuffle'))
    elif system.startswith('win'):
        destfolder = os.path.expandvars(os.path.join('%APPDATA%', '.minecraft', 'resourcepacks', 'shuffle'))
    else:
        destfolder = 'shuffle'
        print2('Failed to identify operating system, placing file in current folder instead.')
    shutil.make_archive(destfolder, 'zip', 'shuffled')
    print2('Resource pack installed!')
    shutil.rmtree('shuffled')
except:
    print2('Compression failed! Please manually move the "shuffled" folder to your resource pack folder.')
