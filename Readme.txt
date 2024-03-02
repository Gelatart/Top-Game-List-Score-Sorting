CONDA ACTIVATION: GameListScore

GRABBING FROM AI CLASS (UVU CS 4470):
[CS 4470 - Project 1.pdf helped figure a lot of this out, from Module 1]
-We used Anaconda/Conda to manage a Python environment?
-We named our environment "GameListScore"?
-Would have created it with something like "conda create --name cs4470 python=3.9"?

HOW TO WORK GENERATOR.PY:
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

MONGOSH:
(Seems like I can only properly connect to the cluster when I don't use my VPN?)

GITHUB BRANCHING:
(Ask dad for review on the console commands that can do this)
-Branch whenever get a new major feature that I want to work on
-Pull request when I've made significant progress on that feature
-Keep commiting while I wait for dad to approve the pull request
-Command line: first put "git status" to see what branch I'm on and status
-Then put "git branch <BRANCH NAME>" to start a new branch (ex. "create-mongo-db")
-Then put "git checkout <BRANCH NAME>" to switch to this new branch
-Then put "git status" to check that successfully on new branch
-Then put "git push -u origin <BRANCH NAME>" to push the new branch to the remote source
-Feel free to check the new branch exists and that you're using it

PULL REQUESTS:
-Add dad as a reviewer as soon as make new pull request so try to include him