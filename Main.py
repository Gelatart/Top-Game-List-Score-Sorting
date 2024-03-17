#INITIAL PLANNING:
#Goal of this file is to be the main hub, the new entry point for the project
#Running this could potentially lead to all the other files I have set up, to run different operations
#So it should probably be pretty command line interface based (Maybe a GUI someday?)
#Might need to retroactively give the other py files a bit more CLI as well?
#Or maybe have them run separately then return to main.py CLI?
#The CLI may even offer opportunities for micro-operations that don't require their own files? Or could later be spun off?
#Allow the printing of reports with various customizations?

#POST-FIRST STORY PLANNING:
#Potential features to include in the future
    #Basic GUI? rather than pure CLI?
        #libraries exist for this? chatgpt suggests Tkinter, PyQt, or Kivy for visual interfaces
    #Run a mongo shell program directly interacting with the cluster?
    #Give the user the ability to create shell versions of new files with certain names?
        #allow them to start doing command line editing and saving of the files to get started?
    #Give the user the ability to write new lists within the program?
        #name the list, what type it is, and all the needed lines and such and rest will create it?
    #Create new functions/files that allow for customizable reports to be made, that we can title ourselves?
        #set platform filters, what types of ranking criteria, developer filters, title filters, etc.
        #allow more than just basic txt files? give other options that allow for more graphic/organize customization?
    #Create new file that only generates all the files locally and doesn't bother with mongodb?
        #Make sure altgenerator can fill in the gaps to the cluster when this is done? Without duplicates?
    #allow the user to write down ideas of potential new features to add in the future
        #have these automatically logged to a persistent file that keeps track across sessions
        #when writing it just appends to the already existing file
        #can be reviewed later, lines removed if felt they aren't worth concern
    #give options to change what database format using? provide support for more than mongodb? option to switch?
    #make a txt file that branches games into family groupings?
    #chatgpt: try to figure out web scraping to extract data from websites?
        #review the data afterwards to see how useful it was, give a check to original source to make sure fits my standards?
    #chatgpt: consider what other user-friendly options and interactive features I could add?
    #chatgpt: do data analysis and visualization on the data once I have it? generate visual/interactive reports/programs?
        #chatgpt: try to identify trends and patterns, in ratings over time or across genres?
        #create charts or graphs to represent aggregated scores/rankings?
        #chatgpt: "Implement statistical analysis to find correlations between different factors such as genre, platform, or release year and game ratings."
    #chatgpt: allow users to customize aggregation process
        #chatgpt: specify which sources to include, weighting scores differently, filtering games off criteria
        #chatgpt: "Implement settings to control how the data is displayed and analyzed, such as sorting options or filtering by platform or release date."
    #chatgpt: use database to enable more complex queries
        #chatgpt: "Implement functionality to update the database with new game releases and ratings automatically."
    #recommendation system
        #chatgpt: "Develop a recommendation engine that suggests games based on user preferences and aggregated scores."
        #this would require a system that tracks users and their history of preferences, which seems like a real interesting way to go
        #could try to integrate with services like glitchwave and backloggd to see what a user's preferences are to try to have a recommendation algorithm?
        #or just have my own databases to track users and their ratings of games?
        #chatgpt: "Utilize machine learning techniques to improve the accuracy of recommendations over time."
    #community features
        #chatgpt: "Add social features like user profiles, comments, and sharing capabilities to allow users to discuss and recommend games within the application."
        #chatgpt: "Implement user ratings and reviews to complement aggregated scores from professional sources."
        #another approach I wasn't really considering, that definitely pushes it more public oriented
        #I guess that means I would have a mass aggregation service that establishes its definitive rankings
        #but users could have recommendations from a mix of their tastes and the "official" tastes?
        #maybe allow users to try to enter their own lists? have a process that qualifies what they submit? allow them to submit from other sources?
        #maybe have a public facing version that cleans things up more generally
        #and my private facing version that aggregates based on the way I do things
        #might have to introduce more significant weighting options at some point if I go along this road
    #localization and internationalization
        #chatgpt: "Support multiple languages by implementing localization features."
        #chatgpt: "Integrate data from international sources to provide a more diverse range of game ratings and reviews."
        #I guess provide some support in the background that could pull different text for different languages?
        #But I def think I should prioritize international sources of data (should try to push that in tracking more)
    #Error Handling and Logging:
        #chatgpt: "Improve error handling to provide informative error messages and gracefully handle unexpected situations."
        #chatgpt: "Implement logging to track program activities and debug issues more effectively."
        #not sure if things are at the level where there are much errors to handle yet
        #will have to keep in mind as it gets more advanced and robust
    #Performance Optimization:
        #chatgpt: "Profile the application to identify performance bottlenecks and optimize critical sections of the code."
        #chatgpt: "Implement caching mechanisms to reduce the need for repeated data retrieval and processing."
        #might be worth analyzing with tools, and looking for redundancies
        #though I think for now that might not be something that could help too much, not until it gets more advanced
    #SEE IF CAN GET OTHER USEFUL IDEAS/BRAINSTORMS FROM CHATGPT?

#import os #To run a python script from this file in a new shell, doesn't seem to work right now
import subprocess #Used to run other py files as a subprocess

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
        print("3. Drop.py: Drop the collections to empty the databases in the cluster and start with a clean slate")
        print("4. QuickMath.py: Not entirely related to this project, more personal use for tracking hours in games I've played")
        print("5. Quit/Exit: Quit this program and finish your business")
        print()

        #Let user pick their option of program
        option = input("Select what you would like to choose to run: ")

        #Potential valid options
        if(option == '1' or option == 'Generator.py' or option == 'Generator' or option == 'generator' or option == 'generator.py'):
            #print("Generator.py will be run now")
            option_check = True
            program_selected = 'Generator.py'
        elif(option == '2' or option == 'AltGenerator.py' or option == 'AltGenerator' or option == 'altgenerator' or option == 'altgenerator.py'):
            #print("AltGenerator.py will be run now")
            option_check = True
            program_selected = 'AltGenerator.py'
        elif (option == '3' or option == 'Drop.py' or option == 'Drop' or option == 'drop' or option == 'drop.py'):
            #print("Drop.py will be run now")
            option_check = True
            program_selected = 'Drop.py'
        elif (option == '4' or option == 'QuickMath.py' or option == 'QuickMath' or option == 'quickmath' or option == 'quickmath.py'):
            option_check = True
            program_selected = 'QuickMath.py'
        elif(option == '5' or option == 'Quit' or option == 'quit' or option == 'Exit' or option == 'exit'):
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
    #print("You have chosen: " + option)
    #print("You have chosen: " + str(program_selected))
    print("You have chosen: " + program)
    #print(str(program_selected) + " will be run now")
    print(program + " will be run now")

    #TIME TO RUN REAL PROGRAM
    #os.system(program_selected)
    #os.system(program)
    subprocess.run(["python", program])

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