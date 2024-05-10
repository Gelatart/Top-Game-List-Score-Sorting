#Imports grabbed from generator.py I thought I might need
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv
import datetime

print("Welcome to PrintReports!")

#print("For now let's start with a test pull. Best games for the Wii!")

#Right now going to attempt to build an or query? Make an option for an and query style later?
"""
AND STYLE:
query = {'x': 1}
if checkbox == 'checked':
    query['y'] = 2

results = db.collection.find(query)

OR STYLE:
query = [{'x': 1}]
if checkbox == 'checked':
    query.append({'y': 2})

results = db.collection.find({'$or': query})

REFERENCE: https://stackoverflow.com/questions/11269680/dynamically-building-queries-in-pymongo
"""

load_dotenv()

#Start connecting to Mongo cluster
mon_connect = os.getenv('MONGO_URI')
#print(mon_connect)
mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
#mon_client = pymongo.MongoClient(mon_connect)
mon_db = mon_client["GameSorting"]
try:
    mon_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
mon_col = mon_db["games"]
list_col = mon_db["lists"]

#test_query = {"Main Platform": "Wii"}
#test_query = {"Main Platform": {"$exists": True}}
#test_query = {"Ranked Score": { "$gt": 2400 } }

print("Time to grab the games!")
#games_pulled = mon_db.mon_col.find().limit(15)
#games_pulled = mon_col.find().limit(10)
#games_pulled = GameSorting.games.find().limit(10)
#games_pulled = mon_db.find().limit(15)
#games_pulled = mon_col.find({},{"Title": 1, "Main Platform": 1}).limit(10)
#games_pulled_query = mon_col.find(test_query, { "List of References": 0, "Total Count": 0}).limit(10)
#games_pulled_ranked = mon_col.find(test_query).sort("Ranked Score", -1)
#games_pulled_inclusion = mon_col.find(test_query).sort("Inclusion Score", -1)
#games_pulled_average = mon_col.find(test_query).sort("Average Score", -1)

#print(games_pulled_query)

"""
for game in games_pulled:
    print("Here is a game")
    print(game)
    if(game["Main Platform"] == "Wii"):
        print("We found one!")
        print(game)
    print()
"""

#input("Brief pause\n")

"""
for game in games_pulled_query:
    print("Here is a game")
    print(game)
    #if(game["Main Platform"] == "Wii"):
    #    print("We found one!")
    #    print(game)
    print()
"""

print("Now it's time for us to pick some options in generating a report")

#add in more answer checks later? or come up with a better way to do menu progression and repeated asking?

answer_check_main = False
queries = []
or_queries = []
and_queries = []
#^Try to split the natural or queries and the natural and queries?
while(answer_check_main == False):
    print()
    print("Which filter category would you like to add on to your report?")
    print("1. Platform Inclusion")
    print("2. Main Platform")
    print("3. Release Date")
    print("4. Completion Status")
    print("5. Title")
    print("6. Ranked Score")
    print("7. Inclusion Score")
    print("8. Average Score")
    print("9. Player Count")
    print("10. Developers")
    print("11. Miscellaneous")
    print("12. Finish and Generate Report")
    #consider franchise option when that data is pulled? genre? other fields?

    filter_category = input("Make selection here: ")

    if(filter_category == '1'):
        print("You have selected 1. Platform Inclusion")
        print("Would you like to include single platforms, entire brands, generations of platform, or formats of platforms?")
        print("1. Single Platform")
        print("2. Brand of Platform")
        print("3. Generation of Platform")
        print("4. Format of Platform")
        platforms_option = input()
        if(platforms_option == '1'):
            print("Now we are going to list all of the options of platforms you can choose from")
            print("Note that the numbers are listed as so because they are the platform ID's listed in IGDB's API")
            input("Whenever you are ready, the platform options will be listed in full (For now use the text version)\n")
            print("3. Linux")
            print("4. N64")
            print("5. Wii")
            print("6. PC (Windows)")
            print("7. PS1")
            print("8. PS2")
            print("9. PS3")
            print("11. Xbox")
            print("12. X360")
            print("13. PC-DOS")
            print("14. Mac")
            print("15. C64 & C128")
            print("16. Amiga")
            print("18. NES")
            print("19. SNES")
            print("20. DS")
            print("21. GCN")
            print("22. GBC")
            print("23. DC")
            print("24. GBA")
            print("25. Amstrad CPC")
            print("26. ZX Spectrum")
            print("27. MSX")
            print("29. GEN/MD")
            print("30. 32X")
            print("32. SAT")
            print("33. GB")
            print("34. Android")
            print("35. Sega Game Gear")
            print("36. XBLA")
            print("37. 3DS")
            print("38. PSP")
            print("39. iOS")
            print("41. Wii U")
            print("42. N-Gage")
            print("44. Tapwave Zodiac")
            print("45. PSN")
            print("46. Vita")
            print("48. PS4")
            print("49. XONE")
            print("52. Arcade")
            print("58. Super Famicom")
            print("59. 2600")
            print("64. Sega Master System")
            print("65. Atari 8-bit")
            print("71. Commodore VIC-20")
            print("75. Apple II")
            print("79. Neo Geo MVS")
            print("80. Neo Geo AES")
            print("88. Magnavox Odyssey")
            print("99. Famicom")
            print("129. Texas Instruments TI-99")
            print("130. Switch")
            print("137. New Nintendo 3DS")
            print("149. PC-98")
            print("169. Xbox Series")
            print("306. Satellaview")
            print("379. Game.com")
            print("Which platform would you like to include?")
            #have function to check if number just given was one of the valid options?
            #going to go off of IGDB ID's for now, need to keep adding more
            platform_selection = input()
            new_query = {"List of Platforms": platform_selection}
            queries.append(new_query)
        print("Which brand of platform would you like to include?")
        print("1. Nintendo")
        print("2. Sony")
        print("3. Microsoft")
        print("4. Sega")
        print("5. Atari")
        #...
        print("Which generation of platform would you like to include?")
        #include options for non-gen platforms? Like PC/operating system, arcade, etc.?
        #...
        print("Which format of platform would you like to include?")
        print("1. Console")
        print("2. Handheld")
        print("3. Computer")
        print("4. Arcade")
        #...
        print("Returning back to main menu")
    elif (filter_category == '2'):
        print("You have selected 2. Main Platform")
        print("Which platform would you like to be the main platform?")
        print("Note that the numbers are listed as so because they are the platform ID's listed in IGDB's API")
        input("Whenever you are ready, the platform options will be listed in full (For now use the text version)\n")
        print("3. Linux")
        print("4. N64")
        print("5. Wii")
        print("6. PC (Windows)")
        print("7. PS1")
        print("8. PS2")
        print("9. PS3")
        print("11. Xbox")
        print("12. X360")
        print("13. PC-DOS")
        print("14. Mac")
        print("15. C64 & C128")
        print("16. Amiga")
        print("18. NES")
        print("19. SNES")
        print("20. DS")
        print("21. GCN")
        print("22. GBC")
        print("23. DC")
        print("24. GBA")
        print("25. Amstrad CPC")
        print("26. ZX Spectrum")
        print("27. MSX")
        print("29. GEN/MD")
        print("30. 32X")
        print("32. SAT")
        print("33. GB")
        print("34. Android")
        print("35. Sega Game Gear")
        print("36. XBLA")
        print("37. 3DS")
        print("38. PSP")
        print("39. iOS")
        print("41. Wii U")
        print("42. N-Gage")
        print("44. Tapwave Zodiac")
        print("45. PSN")
        print("46. Vita")
        print("48. PS4")
        print("49. XONE")
        print("52. Arcade")
        print("58. Super Famicom")
        print("59. 2600")
        print("64. Sega Master System")
        print("65. Atari 8-bit")
        print("71. Commodore VIC-20")
        print("75. Apple II")
        print("79. Neo Geo MVS")
        print("80. Neo Geo AES")
        print("88. Magnavox Odyssey")
        print("99. Famicom")
        print("129. Texas Instruments TI-99")
        print("130. Switch")
        print("137. New Nintendo 3DS")
        print("149. PC-98")
        print("169. Xbox Series")
        print("306. Satellaview")
        print("379. Game.com")
        print("Which platform would you like to include?")
        # have function to check if number just given was one of the valid options?
        # going to go off of IGDB ID's for now, need to keep adding more
        platform_selection = input()
        new_query = {"Main Platform": platform_selection}
        queries.append(new_query)
    elif (filter_category == '3'):
        print("You have selected 3. Release Date")
        print("Would you like to enter a specific date? Or specify a time range?")
        print("1. Specific date")
        print("2. Specified time range")
        time_style_option = input()
        if (time_style_option == '1'):
            print("Type in the date you would like to filter for")
            print("First type in the year, then the month, then the day")
            date_year = int(input())
            date_month = int(input())
            date_day = int(input())
            filter_date = datetime.datetime(date_year, date_month, date_day)
            print(filter_date)
            new_query = {"Release Date": filter_date}
            queries.append(new_query)
        elif (time_style_option == '2'):
            print("Here are the time range options")
            print("1. Specific year")
            print("2. Specific decade")
            print("3. Before a date")
            print("4. After a date")
            print("5. In between two dates")
            print("6. 20th Century")
            print("7. 21st Century")
            time_range_option = input()
            #...
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
    elif (filter_category == '4'):
        print("You have selected 4. Completion Status")
        print("Would you like games you have completed? Or games you haven't completed?")
        print("1. Completed")
        print("2. Uncompleted")
        completed_option = input()
        if(completed_option == '1'):
            print("Including games you have completed")
            new_query = {"Completed": True}
            queries.append(new_query)
        elif(completed_option == '2'):
            print("Including games you have not completed")
            new_query = {"Completed": False}
            queries.append(new_query)
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
    elif (filter_category == '5'):
        #NOT WORKING YET!!!
        #try search api endpoint?
        print("You have selected 5. Title")
        print("Would you like to enter a filter string to use in filtering results?")
        title_search = input("If so, specify your filter string here: ")
        #new_query = { "Title": { "$text:": title_search}}
        #new_query = mon_col.aggregate([{"$search": {"text:": {"query": title_search, "path": "Title"}}}])
        #new_query = mon_col.find({"$text": {"$search": title_search}})
        new_query = {"$text": {"$search": title_search}}
        #new_query = {"Title": {"$search": title_search}}
        #Trying to figure this out, not working properly, need to have properly built index I refer to?
        queries.append(new_query)
    elif (filter_category == '6'):
        print("You have selected 6. Ranked Score")
        print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
        print("1. Minimum threshold score")
        print("2. Maximum threshold score")
        print("3. Target score")
        score_option = input()
        if (score_option == '3'):
            target_score = input("Set your target score: ")
            new_query = {"Ranked Score": target_score}
            queries.append(new_query)
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
        #...
    elif (filter_category == '7'):
        print("You have selected 7. Inclusion Score")
        print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
        print("1. Minimum threshold score")
        print("2. Maximum threshold score")
        print("3. Target score")
        score_option = input()
        if (score_option == '3'):
            target_score = input("Set your target score: ")
            new_query = {"Inclusion Score": target_score}
            queries.append(new_query)
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
        #...
    elif (filter_category == '8'):
        print("You have selected 8. Average Score")
        print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
        print("1. Minimum threshold score")
        print("2. Maximum threshold score")
        print("3. Target score")
        score_option = input()
        if (score_option == '3'):
            target_score = input("Set your target score: ")
            new_query = {"Average Score": target_score}
            queries.append(new_query)
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
        #...
    elif (filter_category == '9'):
        print("You have selected 9. Player Count")
        print("Would you like to select whether you want singleplayer or multiplayer?")
        print("Or select one-by-one which player counts you would like to include?")
        print("1. Singleplayer or Multiplayer")
        print("2. Pick player counts individually")
        player_type_option = input()
        if(player_type_option == '2'):
            print("Here are the player count options")
            #more elaborate multiplayer mode options?
            print("1. Single player")
            print("2. Multiplayer")
            print("3. Co-operative")
            print("4. Split screen")
            print("5. Massively Multiplayer Online (MMO)")
            print("6. Battle Royale")
            player_count_option = input()
            target_count = None
            if(player_count_option == '1'):
                target_count = "Single player"
            elif(player_count_option == '2'):
                target_count = "Multiplayer"
            elif (player_count_option == '3'):
                target_count = "Co-operative"
            elif (player_count_option == '4'):
                target_count = "Split screen"
            elif (player_count_option == '5'):
                target_count = "Massively Multiplayer Online (MMO)"
            elif (player_count_option == '6'):
                target_count = "Battle Royale"
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
            new_query = {"Player Count": target_count}
            queries.append(new_query)
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
        #...
    elif (filter_category == '10'):
        print("You have selected 10. Developers")
        #print("Are you planning on selecting filters for developers or publishers right now?")
        print("For developers, are you looking for true Developers, or just any company that worked on a game?")
        print("Would you like to try entering in a name for the developer you are looking for? Or trying by their IGDB ID?")
        print("1. Search by name")
        print("2. Search by ID")
        dev_type_option = input()
        if(dev_type_option == '1'):
            print("Which developer are you wanting to filter for? For now you'll want to be pretty exact.")
            dev_search = input()
            new_query = {"Developers": dev_search}
            queries.append(new_query)
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
        #going to be using involvedcompany and company?
        #...
    elif (filter_category == '11'):
        print("You have selected 11. Miscellaneous")
        print("This is for miscellaneous filter options that don't fit easily anywhere else")
        #...
    elif(filter_category == '12'):
        #answer_check_main = True
        print("Alright! Let's generate the report with the options selected!")
        custom_query = {}
        print(queries)
        #for query, value in queries.items():
        """
        COMMENTING UNTIL WE HAVE AND APPROACH
        for query in queries:
            #how do i combine all the old queries into one new one?
            #need to take list of queries dict values, and pull values out to build into custom_query
            #custom_query += query
            #custom_query[query] = value
            for key, value in query.items():
                custom_query[key] = value
        """
        print("Would you like your queries to build in an AND approach, OR approach, or the most natural mix of both?")
        print("1. AND approach")
        print("2. OR approach")
        print("3. Natural mix")
        and_or_type = input()
        print("How would you like your report sorted?")
        print("1. By Ranked Score")
        print("2. By Inclusion Score")
        print("3. By Average Score")
        print("4. Alphabetical")
        print("5. Oldest First")
        print("6. Newest First")
        sort_type = input()
        if (sort_type == '1' and and_or_type == '1'):
            # and approach
            # games_pulled = mon_col.find(custom_query).sort("Ranked Score", -1)
            #games_pulled = mon_col.find({'$or': queries}).sort("Ranked Score", -1)
            games_pulled = mon_col.find({'$and': queries}).sort("Ranked Score", -1)
        elif (sort_type == '2' and and_or_type == '1'):
            # and approach
            #games_pulled = mon_col.find(custom_query).sort("Inclusion Score", -1)
            games_pulled = mon_col.find({'$and': queries}).sort("Inclusion Score", -1)
        elif (sort_type == '3' and and_or_type == '1'):
            # and approach
            #games_pulled = mon_col.find(custom_query).sort("Average Score", -1)
            games_pulled = mon_col.find({'$and': queries}).sort("Average Score", -1)
        elif(sort_type == '1' and and_or_type == '2'):
            #or approach
            #games_pulled = mon_col.find(custom_query).sort("Ranked Score", -1)
            games_pulled = mon_col.find({'$or': queries}).sort("Ranked Score", -1)
        elif (sort_type == '2' and and_or_type == '2'):
            # or approach
            #games_pulled = mon_col.find(custom_query).sort("Inclusion Score", -1)
            games_pulled = mon_col.find({'$or': queries}).sort("Inclusion Score", -1)
        elif (sort_type == '3' and and_or_type == '2'):
            # or approach
            #games_pulled = mon_col.find(custom_query).sort("Average Score", -1)
            games_pulled = mon_col.find({'$or': queries}).sort("Average Score", -1)
        else:
            print("Sorry, I don't understand")
            #check again
        file_name = input("What would you like to name your file: ")
        #come up with a check if a particular file name already exists and whether they want to overwrite?
        file_name += "[CUSTOM GENERATION].txt"
        file_print = open(file_name, "w", encoding="utf-8")
        for game in games_pulled:
            # print(game)
            entry = ""
            completed = game["Completed"]
            if (completed == True):
                entry += "[x]"
            entry += game['Title'].strip()
            entry += " --> "
            entry += str(game['Ranked Score'])
            file_print.write(entry)
            file_print.write("\n")
        print("Your custom report has finished printing! Would you like to print more reports? Or quit the program")
        print("1. Print more reports")
        print("2. Quit the program")
        continue_check = input()
        if(continue_check == '1'):
            print("Alright, let's get back to the main printing menu!")
        elif(continue_check == '2'):
            answer_check_main = True
            print("Hope you enjoyed printing reports! See you later!")
        else:
            print("I'm sorry, I don't understand")
            #check again
    else:
        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")

#Close connection to open up socket (seemed to cause problems when running generator then trying printreports?)
mon_client.close()
#Close cursors too?
games_pulled.close()

print("Successfully completed! Have a good day!")

"""
REFERENCES:
(EXCLUDING THE ONES ALREADY REFERENCED IN GENERATOR.PY)
Putting python variables into mongo queries: https://stackoverflow.com/questions/37707033/mongo-query-in-python-if-i-use-variable-as-value
Building up queries dynamically in pymongo: https://stackoverflow.com/questions/11269680/dynamically-building-queries-in-pymongo
Grabbing both values of a dict as iterating: https://www.geeksforgeeks.org/iterate-over-a-dictionary-in-python/
Getting dictionary keys as variables: https://stackoverflow.com/questions/3545331/how-can-i-get-dictionary-key-as-variable-directly-in-python-not-by-searching-fr
Creating datetime objects: https://www.w3schools.com/python/python_datetime.asp
"""