# Minecraft Randomiser

This is a set of programs to randomise data about Minecraft.

Requires Python 3.6+ to run. (~~Experimental compiled builds are avaiable from the releases tab.~~ These are extra broken right now, please use Python to run.)

tl;dr just open randomize.bat if you are too lazy to figure out idk

## `resource_randomiser.py`

This randomises every single image, sound, shader, and language file of a resource pack and automatically installs it into your resource pack folder.

~~This has been tested on Minecraft 1.13.2 & 1.14, and likely works on other versions as well due to its safe way of randomising files.~~

I only tested this once on 1.16-pre7 and I think it should work idk

**The regular Minecraft resource pack is included by default. The images, sounds, and other files included in said resource pack are owned and created by Mojang AB and I
take no credit for creating them.**

### Usage

To use, simply run `resource_randomiser.py` in python3, or double click the executable file. Options can be viewed from the command line using `resource_randomiser.py -h`

#### Examples

`python3 resource_randomiser.py -h` - Get the program's help and list of options.

`python3 resource_randomiser.py` - Randomises the resource pack from the "pack" folder with all default randomisation settings.

`python3 resource_randomiser.py --pack faithful` - Randomises the resource pack from the "faithful" folder.

`python3 resource_randomiser.py --notextures --nosounds --pack faithful` - Randomise everything except the textures and sounds from the resource pack in the "faithful" folder.

## `data_randomiser.py`

This randomises the Minecraft data pack, which includes files such as loot tables for random block drops, recipes, advancements, and experimentally structures (disabled by default, some configurations crash).

~~Has only been tested on the 1.14.3 data pack. This may not be fully compatible with custom data packs (especially randomised advancements). Please report any issues you have.~~

I tested it and it kinda works on 1.16-pre7 lol

### Usage

`python3 data_randomiser.py -h` - Get the program's help and list of options.

`python3 data_randomiser.py` - Randomises loot tables, recipes, and advancements.

`python3 data_randomiser.py --norecipes --structures` - Enables structure randomisation and disables recipes.

`python3 data_randomiser.py --randomlootamount 64` - Items can drop up to 64 times (not amount of items but rather amount of loot)

`python3 data_randomiser.py --norecipes --noloottables --notags --noadvancements --randomlootamount 256` - Literally just Minecraft but loots are randomly generated up to 4 stacks

## Bugs

~~Please report any bugs for either program, especially on Windows and Mac, as they have had little testing. Feature requests are also allowed.~~

Please report bugs but I might not know how to fix but ill do best i can.

