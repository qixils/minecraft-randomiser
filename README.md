# Minecraft Randomizer

This software allows ranomizing most aspects of the game that can be modified through vanilla.
Textures, sounds, shaders, languages, fonts, recipes, loot tables, advancements, and more can be randomized.
The data pack randomizer works on 1.13-1.14 and the resource pack randomizer works on 1.13+.
A handy GUI is available to use and requires the pyqt5 package to run.

This software requires Python 3.6+ to run.

## `resource_randomiser.py`

This randomises every single image, sound, shader, and language file of a resource pack and automatically installs it into your resource pack folder.

This has been tested on Minecraft 1.13.2 & 1.14, and likely works on other versions as well due to its safe way of randomising files.

The regular Minecraft resource pack is included by default. The images, sounds, and other files included in said resource pack are owned and created by Mojang AB and I
take no credit for creating them.

### Command-Line Usage

To use, simply run `resource_randomiser.py` in python3, or double click the executable file. Options can be viewed from the command line using `resource_randomiser.py -h`

#### Examples

`python3 resource_randomiser.py -h` - Get the program's help and list of options.

`python3 resource_randomiser.py` - Randomises the resource pack from the "pack" folder with all default randomisation settings.

`python3 resource_randomiser.py --pack faithful` - Randomises the resource pack from the "faithful" folder.

`python3 resource_randomiser.py --notextures --nosounds --pack faithful` - Randomise everything except the textures and sounds from the resource pack in the "faithful" folder.

## `data_randomiser.py`

This randomises the Minecraft data pack, which includes files such as loot tables for random block drops, recipes, advancements, and experimentally structures (disabled by default, some configurations crash).

Has only been tested on the 1.14.3 data pack. This may not be fully compatible with custom data packs (especially randomised advancements). Please report any issues you have.

### Usage

`python3 data_randomiser.py -h` - Get the program's help and list of options.

`python3 data_randomiser.py` - Randomises loot tables, recipes, and advancements.

`python3 data_randomiser.py --norecipes --structures` - Enables structure randomisation and disables recipes.

## Bugs

Please report any bugs for either program, especially on Windows and Mac, as they have had little testing. Feature requests are also allowed.
