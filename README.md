# Minecraft Randomiser

This is a set of programs to randomise data about Minecraft.

## `resource_randomiser.py`

This randomises every single image, sound, shader, and language file of a resource pack and automatically installs it into your resource pack folder.

This has been tested on Minecraft 1.13.2 & 1.14, and likely works on other versions as well due to its safe way of randomising files.

The regular Minecraft resource pack is included by default. The images, sounds, and other files included in said resource pack are owned and created by Mojang AB and I
take no credit for creating them.

### Requirements

#### General

Python 3.6 or greater is required to run the program.

#### Windows / Linux

Pre-compiled files are available from the [releases page](https://github.com/noellekiq/minecraft-randomiser/releases) which do not require any Python installation.

Pre-compiled releases are generally not recommended, they aren't often updated due to difficulties in doing so.

### Usage

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
