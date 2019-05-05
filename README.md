# Minecraft Randomiser

This program randomises every single image, sound, shader, and language file of a resource pack and automatically installs it into your resource pack folder.

This has been confirmed to work on Minecraft 1.13.2 & 1.14, and likely works on other versions aswell due to its safe way of randomizing files.

The default Minecraft resource pack is included by default. The images, sounds, and other files included in said resource pack are owned and created by Mojang AB and I
take no credit for creating them.

## Requirements

### General

Python 3.6 or greater is required to run the program.

### Windows / Linux

Pre-compiled files are available from the [releases page](https://github.com/noellekiq/minecraft-randomiser/releases) which do not require any Python installation.

## Usage

To use, simply run `randomiser.py` in python3, or double click the executable file. Options can be viewed from the command line using `randomiser.py -h`

### Examples

`python3 randomiser.py -h` - Get the program's help and list of options.

`python3 randomiser.py` - Randomises the resource pack from the "pack" folder with all default randomisation settings.

`python3 randomiser.py --pack faithful` - Randomises the resource pack from the "faithful" folder.

`python3 randomiser.py --notextures --nosounds --pack faithful` - Randomise everything except the textures and sounds from the resource pack in the "faithful" folder.

## Bugs

Please report any bugs you experience, especially on Windows and Mac, as they have had little testing. Feature requests are also allowed.
