import os
import shutil
import random
import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Randomise the assets of a Minecraft resource pack.')
parser.add_argument('-p', '--pack', default='pack', type=str, dest='pack', help='specifies a resource pack folder')
parser.add_argument('--notextures', action='store_false', dest='textures', help='disables randomised textures')
parser.add_argument('--nosounds', action='store_false', dest='sounds', help='disables randomised sounds')
parser.add_argument('--notexts', action='store_false', dest='texts', help='disables randomised text')
parser.add_argument('--nofonts', action='store_false', dest='fonts', help='disables randomised fonts')
parser.add_argument('--noshaders', action='store_false', dest='shaders', help='disables randomised shaders')

args = parser.parse_args()
resourcepack = args.pack
randomisetextures = args.textures
randomisesounds = args.sounds
randomisetext = args.texts
randomisefont = args.fonts
randomiseshaders = args.shaders

if resourcepack == "shuffle":
    print("The input resource pack may not be named 'shuffle'.")
    sys.exit()
if os.path.exists("shuffle/"):
    print("Please remove the 'shuffle' folder before running this program.")
    sys.exit()

def makepath(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            print('tried to create an existing folder')

if not (randomisetextures or randomisesounds or randomisetext or randomisefont or randomiseshaders):
    print('Successfully randomised nothing!')
    sys.exit()
if not os.path.exists(resourcepack):
    makepath(resourcepack)
    print('Unable to locate resource pack folder! Please make sure you have an extracted resource pack in the "'+resourcepack+'" folder.')
    sys.exit()
if not os.path.exists(resourcepack+'/assets'):
    print('Unable to locate resource pack folder! Please ensure you have extracted one properly, you should have an "assets" folder in the "'+resourcepack+'" folder.')
    sys.exit()

images = {}
randimages = {}
sounds = []
randsounds = []
languages = []
specialtexts = []
shaders = {'vsh': [], 'fsh': [], 'json': []}

def processimage(imagepath):
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
            if dirpath != resourcepack+"/assets/minecraft/textures/font" and randomisetextures:
                processimage(fullfilepath)
        elif file.endswith('.ogg') and randomisesounds:
            sounds.append(fullfilepath)
        elif dirpath == resourcepack+"/assets/minecraft/lang" and randomisetext:
            languages.append(fullfilepath)
        elif dirpath == resourcepack+"/assets/minecraft/texts" and randomisetext:
            specialtexts.append(fullfilepath)
        elif dirpath == resourcepack+"/assets/minecraft/shaders/program" and randomiseshaders:
            shaders[file.split('.')[1]].append(fullfilepath)

if randomisetextures or randomisefont:
    print("Randomising textures/fonts")
    for res, textures in images.items():
        shuffled = list(textures)
        random.shuffle(shuffled)
        texturenum = 0
        while texturenum < len(textures):

            #texture
            destfile = 'shuffled'+textures[texturenum][4:]
            makepath(destfile)
            shutil.copyfile(shuffled[texturenum], destfile)

            #mcmeta if it even still exists lol
            mcmeta = shuffled[texturenum].split('.')[0]+'mcmeta'
            mcdest = destfile.split('.')[0]+'mcmeta'
            if os.path.exists(mcmeta):
                shutil.copyfile(mcmeta, mcdest)

            #model file
            origmodel = textures[texturenum].split('/')[::-1][0].split('.')[0]+'.json'
            shufmodel = shuffled[texturenum].split('/')[::-1][0].split('.')[0]+'.json'
            blockpath = '/assets/minecraft/models/block/'
            itempath = '/assets/minecraft/models/item/'
            makepath('shuffled'+blockpath)
            makepath('shuffled'+itempath)
            if os.path.exists(resourcepack+blockpath+shufmodel):
                shutil.copyfile(resourcepack+blockpath+shufmodel, 'shuffled'+blockpath+origmodel)
            if os.path.exists(resourcepack+itempath+shufmodel):
                shutil.copyfile(resourcepack+itempath+shufmodel, 'shuffled'+itempath+origmodel)

            #blockstates
            statedir = '/assets/minecraft/blockstates/'
            makepath('shuffled'+statedir)
            if os.path.exists(resourcepack+statedir+shufmodel):
                shutil.copyfile(resourcepack+statedir+shufmodel,'shuffled'+statedir+origmodel)

            texturenum += 1

if randomisesounds:
    print("Randomising sounds")
    shufflesounds = list(sounds)
    random.shuffle(shufflesounds)
    soundcount = 0
    while soundcount < len(sounds):
        destfile = 'shuffled'+sounds[soundcount][4:]
        makepath(destfile)
        shutil.copyfile(shufflesounds[soundcount], destfile)
        #print(f"{shufflesounds[soundcount]} -> {destfile}")
        soundcount += 1

if randomisetext:
    print("Randomising text")
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

    for lang in languages:
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

if randomiseshaders:
    print("Randomising shaders")
    for ftype, shaderfiles in shaders.items():
        shufshad = list(shaderfiles)
        random.shuffle(shufshad)
        shadnumber = 0
        while shadnumber < len(shaderfiles):
            destfile = 'shuffled'+shaderfiles[shadnumber][4:]
            makepath(destfile)
            shutil.copyfile(shufshad[shadnumber], destfile)
            shadnumber += 1

print("Creating meta files")
shutil.copyfile(resourcepack+'/pack.png', 'shuffled/pack.png')

with open("shuffled/pack.mcmeta", "w") as descfile:
    descfile.write('{"pack":{"pack_format":4,"description":"Minecraft Shuffled by noahkiq"}}')

print('Installing to resource pack folder')

try:
    system = sys.platform.lower()
    if system.startswith('linux'):
        destfolder = os.path.expanduser(os.path.join('~', '.minecraft', 'resourcepacks', 'shuffle'))
    elif system.startswith('darwin'):
        destfolder = os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'minecraft', 'resourcepacks', 'shuffle'))
    elif system.startswith('win'):
        destfolder = os.path.expanduser(os.path.join('%APPDATA%', '.minecraft', 'resourcepacks', 'shuffle'))
    else:
        destfolder = 'shuffle'
        print('Failed to identify operating system, placing file in current folder instead.')
    shutil.make_archive(destfolder, 'zip', 'shuffled')
    print('Resource pack installed!')
    shutil.rmtree('shuffled')
except:
    print('Compression failed! Please manually move the "shuffled" folder to your resource pack folder.')
