import shutil
import json
import os
def makepath(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except:
            print('tried to create an existing folder')
with open('/home/noahkiq/.minecraft/assets/indexes/1.13.1.json') as f:
    data = json.load(f)
for key, value in data["objects"].items():
    if '/lang/' in key:
        destfile = "pack/assets/"+key
        hash = value["hash"]
        makepath(destfile)
        shutil.copy('/home/noahkiq/.minecraft/assets/objects/'+hash[:2]+'/'+hash, destfile)