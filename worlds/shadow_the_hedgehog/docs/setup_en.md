# Shadow The Hedgehgog Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- Dolphin Emulator, recommended 2409 version of higher.
- An NTSC Rom for Shadow the Hedgehog for Gamecube. The Archipelago community cannot provide this.

### Configuring Game

- Configuring Game
- Launch Dolphin, go to options - configuration - interface and tick Enable Debugging UI
- Ensure the lib folder contains the python dolphin memory engine.
- Disable use of Emulated Memory Size override, as archipelago will not work with this setting.


## Optional Software
None yet.

## Generating a Game
1. Create your options file (YAML). Refer to the generated file for information regarding the options. 
If you want the latest template, open the Archipelago Launcher and click 'Generate Templates'
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
   This will generate an output file.
3. Open `ArchipelagoLauncher.exe`
4. Host your game. You can host local games using 'Host' option on the launcher, or upload to archipelago.
5. Open Dolphin emulator.
6. Ensure you do not have a Shadow the Hedgehog save present.
7. Open the Shadow the Hedgehog rom.
8. Select 'Shadow The Hedgehog Client' in Archipelago Launcher.
9. Enter your credentials and connect to the server.

You must remain with client running whenever playing the game to receive checks and other items.
You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect.

## Auto-Tracking

Currently unavailable.