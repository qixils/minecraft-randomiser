import os
import shutil
import random
import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Randomise the assets of a Minecraft resource pack.')
parser.add_argument('-p', '--pack', default='pack', type=str, dest='pack', help='specifies a resource pack folder')
parser.add_argument('-s', '--seed', default=random.randrange(sys.maxsize), type=int, dest='seed', help='specifies a random seed')
parser.add_argument('--models', action='store_true', dest='models', help='EXPERIMENTAL: randomised block/item models')
#parser.add_argument('--noanimations', action='store_false', dest='animations', help='disables animations, fixes some missing textures')
parser.add_argument('--notextures', action='store_false', dest='textures', help='disables randomised textures')
parser.add_argument('--noblockstates', action='store_false', dest='blockstates', help='disables randomised block states')
parser.add_argument('--nosounds', action='store_false', dest='sounds', help='disables randomised sounds')
parser.add_argument('--notexts', action='store_false', dest='texts', help='disables randomised text')
parser.add_argument('--nofonts', action='store_false', dest='fonts', help='disables randomised fonts')
parser.add_argument('--noshaders', action='store_false', dest='shaders', help='disables randomised shaders')

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
if os.path.exists("shuffle/"):
    print("Please remove the 'shuffle' folder before running this program.")
    input('Press any key to exit.')
    sys.exit()

def makepath(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            print('DEBUG: tried to create an existing folder')

if not (randomisetextures or randomisesounds or randomisetext or randomisefont or randomiseshaders):
    print('Successfully randomised nothing!')
    sys.exit()
if not os.path.exists(resourcepack):
    makepath(resourcepack)
    print('Unable to locate resource pack folder! Please make sure you have an extracted resource pack in the "'+resourcepack+'" folder.')
    input('Press any key to exit.')
    sys.exit()
if not os.path.exists(resourcepack+'/assets'):
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
    f = open(imagepath,mode='rb')
    header = f.read(26)
    f.close()
    width = int.from_bytes(header[16:20],'big',signed=False)
    height = int.from_bytes(header[20:24],'big',signed=False)
    dictkey = f"{width}x{height}"
    if dictkey not in images:
        images[dictkey] = []
    images[dictkey].append(imagepath)

#find the files to swap
for dirpath, dirs, files in os.walk(resourcepack+"/assets"):
    for file in files:
        fullfilepath = f"{dirpath}/{file}"
        if file.endswith('.png') and (randomisefont or randomisetextures):
            if dirpath == resourcepack+"/assets/minecraft/textures/font" and randomisefont:
                processimage(fullfilepath)
                totaltextures += 1
            if dirpath != resourcepack+"/assets/minecraft/textures/font" and randomisetextures:
                processimage(fullfilepath)
                totaltextures += 1
        elif dirpath == resourcepack+"/assets/minecraft/models/item" and randomisemodels:
            itemmodels.append(fullfilepath)
        elif dirpath == resourcepack+"/assets/minecraft/models/block" and randomisemodels:
            blockmodels.append(fullfilepath)
        elif dirpath == resourcepack+"/assets/minecraft/blockstates" and randomiseblockstates:
            blockstates.append(fullfilepath)
        elif file.endswith('.ogg') and randomisesounds:
            sounds.append(fullfilepath)
        elif dirpath == resourcepack+"/assets/minecraft/lang" and randomisetext:
            languages.append(fullfilepath)
        elif dirpath == resourcepack+"/assets/minecraft/texts" and randomisetext:
            specialtexts.append(fullfilepath)
        elif dirpath == resourcepack+"/assets/minecraft/shaders/program" and randomiseshaders:
            shaders[file.split('.')[1]].append(fullfilepath)

print2(f"Random Seed: {randomseed}")

if (randomisetextures or randomisefont) and images != {}:
    print2("Randomising textures/fonts", True)
    processedimages = 0
    for res, textures in images.items():
        shuffled = list(textures)
        random.shuffle(shuffled)
        texturenum = 0
        while texturenum < len(textures):
            #texture
            destfile = 'shuffled'+textures[texturenum][4:]

            processedimages += 1
            progressbar = f"Randomising textures/fonts: {processedimages} of {totaltextures}: {shuffled[texturenum].split('/')[::-1][0]} -> {destfile.split('/')[::-1][0]}"
            print2(progressbar, True)

            makepath(destfile)
            shutil.copyfile(shuffled[texturenum], destfile)

            #mcmeta if it even still exists lol
            mcmeta = shuffled[texturenum]+'.mcmeta'
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

            texturenum += 1
    print2('Randomised textures/fonts')

if randomisemodels and itemmodels != []:
    print2('Randomising item models', True)
    randitemmodels = list(itemmodels)
    random.shuffle(randitemmodels)
    itemmodelcount = 0
    while itemmodelcount < len(itemmodels):
        destfile = 'shuffled'+itemmodels[itemmodelcount][4:]

        progressbar = f"Randomising item models: {itemmodelcount} of {len(itemmodels)}: {itemmodels[itemmodelcount].split('/')[::-1][0]} -> {destfile.split('/')[::-1][0]}"
        print2(progressbar, True)

        makepath(destfile)
        shutil.copyfile(randitemmodels[itemmodelcount], destfile)
        itemmodelcount += 1
    print2('Randomised item models')

if randomisemodels and blockmodels != []:
    print2('Randomising block models', True)
    randblockmodels = list(blockmodels)
    random.shuffle(randblockmodels)
    blockmodelcount = 0
    while blockmodelcount < len(blockmodels):
        destfile = 'shuffled'+blockmodels[blockmodelcount][4:]

        progressbar = f"Randomising block models: {blockmodelcount} of {len(blockmodels)}: {blockmodels[blockmodelcount].split('/')[::-1][0]} -> {destfile.split('/')[::-1][0]}"
        print2(progressbar, True)

        makepath(destfile)
        shutil.copyfile(randblockmodels[blockmodelcount], destfile)
        blockmodelcount += 1
    print2('Randomised block models')

if randomiseblockstates and blockstates != []:
    print2('Randomising block states', True)
    randblockstates = list(blockstates)
    random.shuffle(randblockstates)
    blockstatecount = 0
    while blockstatecount < len(blockstates):
        destfile = 'shuffled'+blockstates[blockstatecount][4:]

        progressbar = f"Randomising block states: {blockstatecount} of {len(blockstates)}: {blockstates[blockstatecount].split('/')[::-1][0]} -> {destfile.split('/')[::-1][0]}"
        print2(progressbar, True)

        makepath(destfile)
        shutil.copyfile(randblockstates[blockstatecount], destfile)
        blockstatecount += 1
    print2('Randomised block states')

if randomisesounds and sounds != []:
    print2("Randomising sounds", True)
    shufflesounds = list(sounds)
    random.shuffle(shufflesounds)
    soundcount = 0
    while soundcount < len(sounds):
        destfile = 'shuffled'+sounds[soundcount][4:]

        progressbar = f"Randomising sounds: {soundcount} of {len(sounds)}: {sounds[soundcount].split('/')[::-1][0]} -> {destfile.split('/')[::-1][0]}"
        print2(progressbar, True)

        makepath(destfile)
        shutil.copyfile(shufflesounds[soundcount], destfile)
        #print2(f"{shufflesounds[soundcount]} -> {destfile}")
        soundcount += 1
    print2('Randomised sounds')

if randomisetext and (languages != [] or specialtexts != []):
    print2("Randomising text", True)
    langvalues = []

    for lang in languages:
        with open(lang) as f:
            data = json.load(f)
        langvalues += list(data.values())

    for tfile in specialtexts:
        with open(tfile) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        langvalues += content

    processedlangs = 0
    totallangs = len(languages) + len(specialtexts)
    for lang in languages:
        processedlangs += 1
        progressbar = f"Randomising text: {processedlangs} of {totallangs}: {lang.split('/')[::-1][0]}"
        print2(progressbar, True)

        with open(lang) as f:
            data = json.load(f)
        shufflelang = {}
        for key in list(data.keys()):
            randindex = random.randint(0, len(langvalues)-1)
            shufflelang[key] = langvalues[randindex]
            del langvalues[randindex]
        destpath = 'shuffled'+lang[4:]
        makepath(destpath)
        with open(destpath, 'w') as output:
            json.dump(shufflelang, output)

    for tfile in specialtexts:
        processedlangs += 1
        progressbar = f"Randomising text: {processedlangs} of {totallangs}: {lang.split('/')[::-1][0]}"
        print2(progressbar, True)

        with open(tfile) as f:
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
        with open(destpath, 'w') as output:
            output.write('\n'.join(outputlines))

    print2("Randomised text")

if randomiseshaders and shaders != {'vsh': [], 'fsh': [], 'json': []}:
    print2("Randomising shaders", True)
    for ftype, shaderfiles in shaders.items():
        shufshad = list(shaderfiles)
        random.shuffle(shufshad)
        shadnumber = 0
        while shadnumber < len(shaderfiles):
            destfile = 'shuffled'+shaderfiles[shadnumber][4:]
            makepath(destfile)
            shutil.copyfile(shufshad[shadnumber], destfile)
            shadnumber += 1

print2("Creating meta files")
if os.path.exists(resourcepack+'/pack.png'):
    shutil.copyfile(random.choice(images["16x16"]), 'shuffled/pack.png')

makepath('shuffled/pack.mcmeta')
with open("shuffled/pack.mcmeta", "w") as descfile:
    descfile.write('{"pack":{"pack_format":4,"description":"Minecraft Shuffled by noellekiq"}}')

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
