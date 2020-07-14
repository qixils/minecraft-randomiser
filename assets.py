# Meta file used to obtain some of the vanilla assets (sounds/languages)
# Get the textures from .minecraft/versions/1.14/1.14.jar
import shutil
import json
import os
import sys
def makepath(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            print('tried to create an existing folder')
system = sys.platform.lower()
if system.startswith('linux'):
    destfolder = os.path.expanduser(os.path.join('~', '.minecraft'))
elif system.startswith('darwin'):
    destfolder = os.path.expanduser(os.path.join('~', 'Library', 'Application Support', 'minecraft'))
elif system.startswith('win'):
    destfolder = os.path.expandvars(os.path.join('%APPDATA%', '.minecraft'))
with open(destfolder+'/assets/indexes/1.16.json') as f:
    data = json.load(f)
for key, value in data["objects"].items():
    if '/lang/' in key.lower() or '.ogg' in key.lower():
        destfile = "pack/assets/"+key
        hash = value["hash"]
        makepath(destfile)
        shutil.copyfile('/home/noahkiq/.minecraft/assets/objects/'+hash[:2]+'/'+hash, destfile)
