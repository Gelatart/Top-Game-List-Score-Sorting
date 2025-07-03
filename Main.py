#INITIAL PLANNING:
#Goal of this file is to be the main hub, the new entry point for the project
#Running this could potentially lead to all the other files I have set up, to run different operations
#So it should probably be pretty command line interface based (Maybe a GUI someday?)
#Might need to retroactively give the other py files a bit more CLI as well?
#Or maybe have them run separately then return to main.py CLI?
#The CLI may even offer opportunities for micro-operations that don't require their own files? Or could later be spun off?
#Allow the printing of reports with various customizations?

import os #To run a python script from this file in a new shell, doesn't seem to work right now
import subprocess #Used to run other py files as a subprocess
import sys

#Introduce users to the main program
print("Welcome to Gelatart's Top-Game-List-Score-Sorting project!")

#Keep looping on asking user if they want to skip intro text until good response given
answer_check = False
while(answer_check == False):
    print("Would you like to skip the broader intro to the point of this project, and just get into operating it?")
    answer = input("Answer here, Y or N: ")
    if(answer == 'N' or answer == 'n' or answer == 'No' or answer == 'no'):
        #The full intro text is given here, consider storing this elsewhere and importing it in at some point?
        print("This project is a personal-use project")
        print("It was originally quickly designed to fulfill a very specific use of interest for me and me alone")
        print()
        print("For likely autistic reasons, I like to look at lists of things that are considered the best")
        print("It's interesting for me as I check out new movies, albums, or whatnot, to refer to compiled lists for material")
        print("Especially when user ratings are taken into account")
        print("Around 2015, I felt there wasn't a good authoritative source for video games like Letterboxd or RateYourMusic")
        print("Some options have come up like Glitchwave and Backloggd since then, but they still have a long way to go")
        print("Regardless, I came upon the idea of gathering multiple video game lists and aggregating them for overall scores")
        print("This was an attempt to take a broad yet deep look at what kinds of video games have gotten the most acclaim")
        print("I used to do this manually, using Google Sheets to keep track of all the lists I had catalogued and the results")
        print("This meant for every game, I had to see where it ended up on every handwritten list and tally up all the scores")
        print("As list rankings also shift over time, and I planned to keep adding more lists, this started becoming a big timesink")
        print("Honestly that timesink didn't bother me too much at first, I partially enjoyed having busywork to do among other things")
        print("But as I started getting up to more things in life, it became way too demanding of a task, left outdated and unfinished")
        print()
        print("Years later, I was suddenly hit with inspiration, when I had been thinking on advice given to me from a friend")
        print("On how aside from the work you get up to in your classes, it's important to have personal portfolio work for recruiters")
        print("I had only recently started using Python, and wanted to do more with it to familiarize myself with such a popular language")
        print("But I had become familiar enough with how easy it is to get things running off the ground with basic implementation in Python")
        print("And I think some of that Python experience helped give me a jolt of sudden inspiration, things suddenly clicking into place")
        print("I had tried coding some sort of automated solution in the past, but gave up quickly, probably trying to take on too much at once")
        print("But it had suddenly hit me to do a minimum viable prototype approach, starting very basic and working from there")
        print("Within a few hours I had implemented a working basic version, essentially the skeleton of the process I still use to this point")
        print()
        print("I started with Generator.py, which first only printed to a spreadsheet, then sorted txt files, and now uses MongoDB")
        print("Since then I've added other files as well, and plan to keep expanding this project in as many useful ways as I can think of")
        print("I hope you enjoy using this program!")
        answer_check = True
    elif(answer == 'Y' or answer == 'y' or answer == 'Yes' or answer == 'yes'):
        #Skip the intro text and get to running programs
        print("Okay, let's get into it!")
        answer_check = True
    else:
        #Loop again until get response program understands
        print("Not really a valid response")
        print()

#Keep looping on allowing user to run other Python programs from the main program
option_check = False
program_completed = False
#Make a loop to keep going until program done?
program_selected = None
while(program_completed == False):
    #Loop on giving options, wait until given good response
    while(option_check == False):
        #List all the options
        print()
        print("Here are your options:")
        print("1. Generator.py: Run the traditional generator, which starts fresh every time")
        print("2. AltGenerator.py: Run the alternate generator, which checks for new lists and only adds them")
        print("3. PrintReports.py: Print custom reports with custom criteria off of the data in the cluster")
        print("4. Drop.py: Drop the collections to empty the databases in the cluster and start with a clean slate")
        print("5. QuickMath.py: Not entirely related to this project, more personal use for tracking hours in games I've played")
        print("6. IGDB-Query.py: Tool for writing up command line querying of the IGDB API for testing purposes")
        print("7. Mongo-Query.py: Tool for writing up command line querying of the MongoDB Cluster for testing purposes")
        print("8. Quit/Exit: Quit this program and finish your business")
        print()

        #Let user pick their option of program
        option = input("Select what you would like to choose to run: ")

        #Potential valid options
        if(option == '1' or option == 'generator.py' or option == 'Generator' or option == 'generator' or option == 'generator.py'):
            option_check = True
            program_selected = 'src.generator.generator'
        elif(option == '2' or option == 'alt_generator.py' or option == 'AltGenerator' or option == 'altgenerator' or option == 'altgenerator.py'):
            option_check = True
            program_selected = 'src.alt_generator'
        elif (option == '3' or option == 'print_reports.py' or option == 'PrintReports' or option == 'printreports' or option == 'printreports.py'):
            option_check = True
            program_selected = 'src.print_reports'
        elif (option == '4' or option == 'drop.py' or option == 'Drop' or option == 'drop' or option == 'drop.py'):
            option_check = True
            program_selected = 'src.drop'
        elif (option == '5' or option == 'quick_math.py' or option == 'QuickMath' or option == 'quickmath' or option == 'quickmath.py'):
            option_check = True
            program_selected = 'src.quick_math'
        elif (option == '6' or option == 'igdb_query.py' or option == 'IGDB-Query' or option == 'igdb-query' or option == 'igdb-query.py'):
            option_check = True
            program_selected = 'src.igdb_query'
        elif (option == '7' or option == 'mongo_query.py' or option == 'Mongo-Query' or option == 'mongo-query' or option == 'mongo-query.py'):
            option_check = True
            program_selected = 'src.mongo_query'
        elif(option == '8' or option == 'Quit' or option == 'quit' or option == 'Exit' or option == 'exit'):
            option_check = True
            print("Thank you for spending time with this program.")
            program_completed = True
            break
            #Break out of the loop because we are exited
        else:
            #An entry that the program is not yet designed to understand
            print("Hmm, not sure if I understand that input (or at least not yet)")
    #The program is set to complete, so break the loop
    if(program_completed == True):
        break

    #Print out the program that was selected
    print()
    program = str(program_selected)
    print("You have chosen: " + program)
    print(program + " will be run now")

    # Set PYTHONPATH to include 'src' so imports like 'from generator...' work
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath("src")

    #TIME TO RUN REAL PROGRAM
    #subprocess.run(["python", program])
    # Run the program with modified environment
    #subprocess.run([sys.executable, program], env=env)
    subprocess.run([sys.executable, "-m", program])

    option_check = False #To prevent the loop from going through again before it's ready

#Wrap up the program
print()
print("All done! Goodbye!")

"""
DATA API SAMPLE ATLAS GAVE ME FOR PYTHON AND GAMESORTING GAMES COLLECTION:
"""
"""
import os
from dotenv import load_dotenv

load_dotenv()
data_key = os.getenv('API_KEY')

import requests
import json
url = "https://us-west-2.aws.data.mongodb-api.com/app/data-sghta/endpoint/data/v1/action/findOne"
#^Do I need to put the App ID (or cluster name?) in the env file?

payload = json.dumps({
    "collection": "games",
    "database": "GameSorting",
    "dataSource": "GameSorting",
    "projection": {
        "_id": 1,
        "Title": 1
    }
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': data_key,
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
"""

"""
REFERENCES:
Running a python script from another: https://www.geeksforgeeks.org/run-one-python-script-from-another-in-python/
"""