# Anodyne Randomizer Setup

## Installation

The Anodyne Archipelago Client currently only supports
[the itch.io version](https://pixiecatsupreme.itch.io/anodyne-sharp) of the
game. The Steam version may be supported in the future.

1. Download the Anodyne Archipelago Randomizer from
   [the releases page](https://github.com/SephDB/AnodyneArchipelagoClient/releases).
2. Locate `AnodyneSharp.exe`.
3. Create a folder called `Mods` next to `AnodyneSharp.exe` if it does not
   already exist.
4. Unzip the randomizer into the `Mods` folder.

## Joining a Multiworld game

1. Open Anodyne.
2. Enter your connection details on the main menu. Text must be entered via
   keyboard, even if you are playing on controller.
3. Select "Connect".
4. Enjoy!

To continue an earlier game, you can perform the exact same steps as above. The
randomizer will remember the details of your last nine unique connections.

## Frequently Asked Questions

### Will this impact the base game?

The base game can still be played normally by not selecting "Archipelago" from
the main menu. You can also safely remove the randomizer from the `Mods` folder
and add it back later. The randomizer also uses separate save files from the
main game, so your vanilla saves will not be affected either.

### Is my progress saved locally?

The randomizer generates a savefile name based on your Multiworld seed and slot
number, so you should be able to seamlessly switch between multiworlds and even
slots within a multiworld.

The exception to this is different rooms created from the same multiworld seed.
The client is unable to tell rooms in a seed apart (this is a limitation of the
Archipelago API), so the client will use the same save file for the same slot in
different rooms on the same seed. You can work around this by manually moving or
removing the save file from the save file directory.
