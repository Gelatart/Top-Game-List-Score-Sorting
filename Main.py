#INITIAL PLANNING:
#Goal of this file is to be the main hub, the new entry point for the project
#Running this could potentially lead to all the other files I have set up, to run different operations
#So it should probably be pretty command line interface based (Maybe a GUI someday?)
#Might need to retroactively give the other py files a bit more CLI as well?
#Or maybe have them run separately then return to main.py CLI?
#The CLI may even offer opportunities for micro-operations that don't require their own files? Or could later be spun off?
#Allow the printing of reports with various customizations?

print("Welcome to Gelatart's Top-Game-List-Score-Sorting project!")

answer_check = False
while(answer_check == False):
    # Provide option to skip the intro text eventually, only see it if people want to read it?
    print("Would you like to skip the broader intro to the point of this project, and just get into operating it?")
    answer = input("Answer here, Y or N: ")
    if(answer == 'N'):
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
        answer_check = True
    elif(answer == 'Y'):
        print("Okay, let's get into it!")
        answer_check = True
    else:
        print("Not really a valid response")
        print()

print()
print("Here are your options:")
print("1. Generator.py: Run the traditional generator, which starts fresh every time")
print("2. AltGenerator.py: Run the alternate generator, which checks for new lists and only adds them")
print("3. Drop.py: Drop the collections to empty the databases in the cluster and start with a clean slate")
print()

option = input("Select what you would like to choose to run: ")

print()
print("You have chosen: " + option)
if(option == '1'):
    print("Generator.py will be run now")
elif(option == '2'):
    print("AltGenerator.py will be run now")
else:
    print("Hmm, not sure if I understand that input (or at least not yet)")