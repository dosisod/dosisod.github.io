# WASM-4 Game Jam: Day 8

I've been dealing with head gasket repairs and haven't really had time to work on the
jam (blog on that later, perhaps). Today I mustered up the energy to keep
going, especially given that there is about 1.5 days left before everything has
to be submitted.

Some milestones:

* Code has been uploaded to [GitHub](https://github.com/dosisod/matcha9000)!
* A GitHub action workflow has been added to create a release (with build artifacts) whenever a commit is made to master.
* Auto saving current level
* Hashed out the first 5 levels

One of the hardest things that I have ran into is making the levels hard enough to be fun,
but easy enough to be solvable, and fit within the 20 line mark. I have a few ideas to make
things easier/more playable, including:

* Making the `ROT` op code take a turn count
* Make `USE` op code work regardless of player direction
* Add a play/pause button to allow you to stop/resume normal execution
* Add sort of a grid system to make counting out steps easier

I have a lot of work ahead of me tomorrow. I was planning on making 20 levels to match the
20 available instructions, but that might be hard, especially with the game play adjustments I need
to make.
