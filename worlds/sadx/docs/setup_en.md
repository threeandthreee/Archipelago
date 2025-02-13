# Sonic Adventure DX Setup Guide

## Required Software

- Sonic Adventure DX (2004 version)
- SA Mod Manager from: [SA Mod Manager GameBanana Page](https://gamebanana.com/tools/15436)
- Archipelago Mod for Sonic Adventure DX
  from: [Sonic Adventure DX Classic Randomizer Mod Releases Page](https://github.com/ClassicSpeed/sadx-classic-randomizer/releases)

## Installation Procedures (Windows)

1. Install Sonic Adventure DX
   from: [Sonic Adventure DX Steam Store Page](https://store.steampowered.com/app/71250/Sonic_Adventure_DX/).
2. Install SA Mod Manager as per [its instructions in GameBanana](https://gamebanana.com/tools/15436).
3. Unpack the Archipelago Mod into the `/mods` directory in the folder into which you installed Sonic Adventure DX so
   that `/mods/SADX_Archipelago` is a valid path.
4. Launch the `SAModManager.exe` and make sure the SADX_Archipelago mod is listed and enabled. Make sure the mod is at
   the bottom of the list.
5. Disable the "Steam Achievements Mod" if enabled.
6. Disable the "Fixes, Adds, and Beta Restores" if enabled.

## Joining a MultiWorld Game

1. Before launching the game, run the `SAModManager.exe`, select the SADX_Archipelago mod, and hit the `Configure Mod`
   button.
2. For the `Server IP` field under `AP Settings`, enter the address of the server, such as archipelago.gg:54321. Your
   server host should be able to tell you this.
3. For the `PlayerName` field under `AP Settings`, enter your "name" field from the yaml or website config.
4. For the `Password` field under `AP Settings`, enter the server password if one exists, otherwise leave blank.
5. Click the `Save` button then hit `Save & Play` to launch the game.
6. Create a new save file to start playing! Use the same save file to continue playing.

## Supported and recommended mods

- The DC conversion mod is fully supported.
    - This includes every mod from the SA Mod Manager installer except for the "Steam Achievements Mod".
- Kell's Super Sonic mod. If playing with Chaos Emeralds, you can only transform after collecting all 7.
- Cream the Rabbit mod, every Tails check will work for her.

## Troubleshooting

- You get the SADX_Archipelago: DLL error - The specified module could not be found.
    - Make sure that the antivirus didn't delete the `/mods/SADX_Archipelago/sadx-classic-randomizer.dll` file.
- You get error: The code execution cannot proceeD because MSVCP140.dll was not found.
    - Install the .NET 8 from [Microsoft's website](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-desktop-8.0.10-windows-x64-installer).
- The game closes when you press start.
    - This is a Steam input issue. Either run the game from Steam or adjust the "Desktop controller configuration" to
      just be a controller.
    - You can also simply close Steam.
- Some of the emblems don't give me checks.
    - Disable the "Steam Achievements Mod" if enabled.
- Some checks or elements of the randomizer are missing.
    - Disable the "Fixes, Adds, and Beta Restores" mod if enabled.
- Some enemies are not being tracked correctly with the indicator when playing with enemy-sanity.
    - Disable the "SADX:FE" mod if enabled.
- Failed to generate the world.
    - Try updating your Archipelago mod to the latest version (at least 0.5.0).
    - Try enabling more options in the yaml, being too restrictive will prevent the world from generating.