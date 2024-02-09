ACTIVATION KEY: GameListScore

HOW TO WORK THIS:

<fill in process of running this and environment required>

<update proper score for former best pc games list (unranked will calculate score fine?)>

GRABBING FROM AI CLASS (UVU CS 4470):
[CS 4470 - Project 1.pdf helped figure a lot of this out, from Module 1]
-We used Conda to manage a Python environment?
-We used Anaconda?
-We named our environment "GameListScore"?
-Would have created it with something like "conda create --name cs4470 python=3.9"?

-Run the Anaconda Prompt program from Laptop? In pinned programs at bottom?
--Should have (base) at the beginning
--Navigate it to correct directory
--Type "activate GameListScore" to switch from (base) to (GameListScore)
--"python -V" will show the version (as of writing it is Python 3.10.9)
--"conda deactivate" will exit out of conda environment
--"python Generator.py" should run it properly once in the environment

SCORING PROCESSES:
-Ranked: 
--Take the number of entries in list
--Set the 1st entry to that number of points
--Decrement going forwards so last place is only 1 point
--Former for this list is only 1 point
-Unranked:
--Take the number of entries in list
--Count a sum of all numbers leading up to that one
--Divide the sum by the number of entries in the list (round down)
--Former for this list is that number divided in half (round down)