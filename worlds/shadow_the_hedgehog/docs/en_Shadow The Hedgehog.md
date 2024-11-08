# Shadow The Hedgehog

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

## What does randomization do to this game?

Randomisation in this game affects the memory of the game to unlock various events and behaviours.
Story mode should not be used and in future versions may be disabled. Any progress through this will not be logic.
All level access is handled via the Select menu where levels will be unlocked as you find the required items to unlock them.
Once you have the goal met, The Last Way will open and be available from the Story menu.

## What items and locations get randomized?

Every level completion is a check in the game, so this includes Hero missions, Neutral missions and Dark mission.
Future versions will include further level completions as checks for The Last Way and boss fights.

Items are used to unlock stages via the Select menu, which should happen automatically upon receiving the item from the multiworld.

Shadow The Hedgehog has mission objectives which require obtaining a number of things.
Each step of progress on these checks is a multiworld item.
Likewise, all of these mission objectives are items that can be received, requiring you to meet the total to finish
the several Dark and Hero missions of the game.

The latest version includes further enemysanity and configuration around the percent of these checks to include.
Checkpoint sanity is a recent addition, allowing each numbered checkpoint to be an individual check.

There are some junk items and special weapon unlocks are also available.

It is possible to tweak the settings to remove some of the specific checks and alter total to the players choice.
Likewise, it is possible to exclude stages.

Future checks and items are expected to be added in the future.

## What other changes are made to the game?

The current changes to the game are all in-memory so the game has not been modified in any major way.
However, in order for the randomisation to work the way that level accessibility behaves is changed.

When entering a level with an objective (excluding all Neutral missions and missions with only 1 objective)
the total amount required for each check per level will be increased by 2. This number and range may change with future versions.

This is to prevent levels and checks becoming unreachable once you have all the required items as you would unable to play some levels as the level would auto-complete.

Once you make progress on an objective, the number will increase in game, but will be reset when handled by the client.
The client will keep the current amount set to the amount you have received from the Multiworld.

If you have the original max (remember, 2 less than what is displayed) you can complete the level.
Ensure you have the mission character selected and pause the game, press the SELECT button, and the total value will visibly change.

Levels which require you to defeat a number of enemies of a particular type will clear as soon as you close the pause menu.
Other missions require you to achieve 1 more step in the objective.

Character interactions in levels have been made to not happen, but will happen the first time when charactersanity is enabled.
This is done by setting the flags to true when the player enters a level, but for those which have been seen.

## What does the game look like?

Currently this project has no feedback on what the item you have found is, and requires the use of the Text Client.

## When the player receives an item, what happens?

When you receive an item, the Text Client will update to inform you. 

## Can I play offline?

This game requires to be online at all times as it is completely memory based. Level restriction and similar paths
will not work when playing offline, nor will item collection.

## How do I finish an objective?
Meet the alignment character in the stage, select that mission, pause the game, press SELECT and the requirement count
will return to normal. This will auto clear for enemy-based missions, but other missions require you to add to the objective count.
If SELECT does not change your view, you do not have the required archipelago items to finish the stage.

For further details, fully read other sections.

## How do I finish?

You select your goal type when setting up in the yaml file. Once you reach these conditions you have set,
based on percentage and enabling, Last Story will unlock in the Story menu. Walk through this and defeat the final boss to finish.

## Known Issues
- Sometimes the stage will not detect the correct mission objectives and will not shift the total. 
Exiting and re-entering the level should hopefully resolve this.
