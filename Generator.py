# import required module
import os
import math
# Writing to an excel sheet using Python
import xlwt
from xlwt import Workbook
#import sqlite3
#^Replaced the need for SQL with MongoDB and Pymongo
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from igdb.wrapper import IGDBWrapper

# assign directory
#directory = 'C:\Users\danie\Documents\Top-Game-List-Score-Sorting\GameLists\Ranked'
directory = r'GameLists\Ranked'
#then do unranked and former

#LOOK INTO PANDAS FOR DEALING WITH TABULAR DATA IN PYTHON

#START FLESHING OUT GLITCHWAVE USAGE
    #FILL OUT RATINGS, COLLECTION, PLAYTHROUGHS, ETC.
    #IMPORT REVIEWS
    #START LOOKING AT GENRE (INFLUENCE?), YEAR, PLATFORM, ETC. CHARTS
#SEE IF BACKLOGGD CHARTS COMPARE, IF CAN DO SIMILAR THINGS TO GLITCHWAVE (ALSO LOOK INTO GROUVEE?)

#ONCE CLEARED ALL OF AN UP TO LIST, THEN CONSIDER EXPANDING THE RANGE (LIKE FROM UP TO 100 TO UP TO 150)

"gameDb is a dict of string titles and game object values"
gameDb = {}
"game object needs two scores"
class GameObject:
    def __init__(self, rank):
        self.rankedScore = rank
        self.listCount = 1
        self.listsReferencing = []
        self.totalCount = 0
        self.completed = False
        self.mainPlatform = 'None'
        self.listPlatforms = []
        self.releaseDate = 'Unknown' #Can I set this to some date value?
        self.playerCounts = []
        self.listDevelopers = []

    #consider storing a constantly updated average score?

    #def __init__(self, rank, count):
    #    self.rankedScore = rank
    #    self.listCount = count

    def __init__(self, rank, list):
        self.rankedScore = rank
        self.listCount = 1
        self.listsReferencing = []
        self.listsReferencing.append(list)
        self.totalCount = 0
        self.completed = False
        self.mainPlatform = 'None'
        self.listPlatforms = []
        self.releaseDate = 'Unknown'  # Can I set this to some date value?
        self.playerCounts = []
        self.listDevelopers = []

    def __init__(self, rank, list, total):
        self.rankedScore = rank
        self.listCount = 1
        self.listsReferencing = []
        self.listsReferencing.append(list)
        self.totalCount = total
        self.completed = False
        self.mainPlatform = 'None'
        self.listPlatforms = []
        self.releaseDate = 'Unknown'  # Can I set this to some date value?
        self.playerCounts = []
        self.listDevelopers = []

    #CONSIDER MAKING AN EXPORT FUNCTION FOR THE CLASS TO CONVERT TO DICTIONARY?

#Start collecting the lists used in a list, put to a new collection in MongoDB
games_lists = []

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

ranked_file_count = 0
unranked_file_count = 0
formerFileCount = 0

"Loop of getting the database information"
#RANKED DIRECTORY
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        # Using readlines()
        file1 = open(f, 'r', encoding="utf-8")
        ranked_file_count += 1
        starting_line = file1.readline()
        Lines = file1.readlines()
        #count = int(starting_line)
        count = len(Lines)
        #print(len(Lines))
        #input('Wait to review\n')
        originalCount = count
        # Strips the newline character
        for line in Lines:
            if line in gameDb:
                gameDb[line].rankedScore += count
                gameDb[line].listCount += 1
                gameDb[line].listsReferencing.append(f)
                gameDb[line].totalCount += originalCount
            else:
                newObj = GameObject(count, f, originalCount)
                gameDb[line] = newObj
            #searchObj = gameDb.get(newObj, 0) + 1
            #gameDb[line].listCount = gameDb.get(newObj, 0) + 1
            print("Score of {}: {}".format(count, line.strip()))
            count -= 1
        games_lists.append(filename)

directory = r'GameLists\Unranked'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        # Using readlines()
        file1 = open(f, 'r', encoding="utf-8")
        unranked_file_count += 1
        starting_line = file1.readline()
        Lines = file1.readlines()
        #count = int(starting_line)
        floatCount = float(starting_line)
        count = math.floor(floatCount)
        count = len(Lines)
        print(count)
        originalCount = count
        #do a sum of all numbers in that count
        count = originalCount * (originalCount + 1) // 2
        #divide the factorial by the original count
        count //= originalCount
        print(count)
        print(f)
        #input('Wait to review\n')
        # Strips the newline character
        for line in Lines:
            if line in gameDb:
                gameDb[line].rankedScore += count
                gameDb[line].listCount += 1
                gameDb[line].listsReferencing.append(f)
                gameDb[line].totalCount += originalCount
            else:
                newObj = GameObject(count, f, originalCount)
                gameDb[line] = newObj
            #searchObj = gameDb.get(newObj, 0) + 1
            #gameDb[line].listCount = gameDb.get(newObj, 0) + 1
            print("Score of {}: {}".format(count, line.strip()))
            #count -= 1
        games_lists.append(filename)

directory = r'GameLists\Former'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        # Using readlines()
        # file1 = open(f, 'r')
        file1 = open(f, 'r', encoding="utf-8")
        formerFileCount += 1
        starting_line = file1.readline()
        Lines = file1.readlines()
        #count = 1
        count = int(starting_line)
        originalCount = count
        #^find out how to read the line amount ahead of time
        #originalCount = len(Lines)
        print(originalCount)
        # Strips the newline character
        for line in Lines:
            if line in gameDb:
                gameDb[line].rankedScore += count
                gameDb[line].listCount += 1
                gameDb[line].listsReferencing.append(f)
                gameDb[line].totalCount += originalCount
            else:
                newObj = GameObject(count, f, originalCount)
                gameDb[line] = newObj
            #searchObj = gameDb.get(newObj, 0) + 1
            #gameDb[line].listCount = gameDb.get(newObj, 0) + 1
            print("Score of {}: {}".format(count, line.strip()))
            #count -= 1
        games_lists.append(filename)

completeFile = open('Completions.txt', 'r')
completeLines = completeFile.readlines()
for line in completeLines:
    if line in gameDb:
        gameDb[line].completed = True
    #else: raise error because not in database? create it with 0 score?

print("Time for attributes!")

#ADD SECTION WHERE WE START GRABBING ADDITIONAL ATTRIBUTES FOR GAME DATABASE?
attributesFile = open('AdditionalAttributes.txt', 'r')
attributesLines = attributesFile.readlines()
itr = iter(attributesLines)
#for line in attributesLines:
try:
    #if line in gameDb:
    while True:
        #Properly parse through line and indented lines?
        title = next(itr)
        if title in gameDb:
            print(title)
            #mainPlatform
            attribute = next(itr)
            print(attribute)
            gameDb[title].mainPlatform = attribute
            #listPlatforms
            attribute = next(itr)
            print(attribute)
            gameDb[title].listPlatforms = attribute
            #releaseDate
            attribute = next(itr)
            print(attribute)
            gameDb[title].releaseDate = attribute
            #playerCounts
            attribute = next(itr)
            print(attribute)
            gameDb[title].playerCounts = attribute
            #listDevelopers
            attribute = next(itr)
            print(attribute)
            gameDb[title].listDevelopers = attribute
            print('')
        #else: supposed to be in database?
except StopIteration:
        pass

#START SCRAPING FOR ATTRIBUTES
"""
Most of the requests to the API will use the POST method
The base URL is: https://api.igdb.com/v4
You define which endpoint you wish to query by appending /{endpoint name} to the base URL eg. https://api.igdb.com/v4/games
Include your Client ID and Access Token in the HEADER of your request so that your headers look like the following.
    Client-ID: Client ID
    Authorization: Bearer access_token
Take special care of the capitalisation. Bearer should be hard-coded infront of your access_token
You use the BODY of your request to specify the fields you want to retrieve as well as any other filters, sorting etc

Example
If your Client ID is abcdefg12345 and your access_token is access12345token, a simple request to get information about 10 games would be.
    POST: https://api.igdb.com/v4/games
    Client-ID: abcdefg12345
    Authorization: Bearer access12345token
    Body: "fields *;"

"""
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
post = 'https://id.twitch.tv/oauth2/token?client_id='
post += client_id
post += '&client_secret='
post += client_secret
post += '&grant_type=client_credentials'

#page = requests.get(post) #404
page = requests.post(post) #gives access token we can use
print(page.text)
input("Here we pause")

#wrapper = IGDBWrapper("YOUR_CLIENT_ID", "YOUR_APP_ACCESS_TOKEN")
access_token = page.text["access_token"]
print(access_token)
wrapper = IGDBWrapper(client_id, access_token)
input("Here we pause")
exit()

"""
MEDIUM EXAMPLE:
URL = 'https://www.bookdepository.com/top-new-releases'
page = requests.get(URL)
soup = BeautiulSoup(page.content, "html.parser")
books = soup.find_all("div", class_ = "book-item")
"""

#START USING PYMONGO FOR OUTPUTTING TO MONGODB DATABASE
#Used code sample from Atlas on how to connect with Pymongo for assistance here
#Connecting to env file to get private login data
mon_connect = os.getenv('MONGO_URI')
#monClient = pymongo.MongoClient(mon_connect)
monClient = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
#Reference code: client = MongoClient(uri, server_api=ServerApi('1'))
monDB = monClient["GameSorting"]
try:
    monClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
mon_col = monDB["games"]
list_col = monDB["lists"]

#TEST INSERT_ONE
#testDict = { "title": "This is a test", "score": 69}
#test = mon_col.insert_one(testDict)

#INSERT ALL GAMES INTO DATABASE
#Clear database to begin with?
mon_col.drop()
list_col.drop()
#export = []
print("INSERTING INTO MONGODB!")
for game, details in gameDb.items():
    #print(details)
    #insertion = mon_col.insert_one(details)
    #insertion = mon_col.insert_one(gameDb[game])
    #export.append(details)
    exportDict = {}
    exportDict["Title"] = game
    exportDict["Ranked Score"] = details.rankedScore
    exportDict["Inclusion Score"] = details.listCount
    averageScore = details.rankedScore / details.totalCount
    exportDict["Average Score"] = averageScore
    exportDict["List of References"] = details.listsReferencing
    exportDict["Completed"] = details.completed
    exportDict["Main Platform"] = details.mainPlatform
    exportDict["List of Platforms"] = details.listPlatforms
    exportDict["Release Date"] = details.releaseDate
    exportDict["Player Counts"] = details.playerCounts
    exportDict["Developers"] = details.listDevelopers
    exportDict["Total Count"] = details.totalCount
    insertion = mon_col.insert_one(exportDict)
#insertion = mon_col.insert_many(gameDb)
#insertion = mon_col.insert_many(export)
print("TIME TO INSERT THE LISTS INTO MONGODB!")
for list in games_lists:
    #print(list)
    listDict = {}
    listDict["Title"] = list
    #could keep track of what type of list it is, other variables?
    list_insert = list_col.insert_one(listDict)

"""
gameDbRanked = {}
gameDbInclusion = {}
gameDbAverage = {}
"""
"loop of printing database to a spreadsheet file"

"""
# Applying multiple styles
boldStyle = xlwt.easyxf('font: bold 1;')
crossedStyle = xlwt.easyxf('font: struck_out 1;')
sheet1.write(0, 0, 'TITLE', boldStyle)
sheet1.write(0, 1, 'RANKED SCORE', boldStyle)
sheet1.write(0, 2, 'INCLUSION SCORE', boldStyle)
sheet1.write(0, 3, 'AVERAGE SCORE', boldStyle)
sheet1.write(0, 4, 'LISTS INCLUDED ON', boldStyle)
sheet1.write(0, 5, 'MAIN PLATFORM', boldStyle)
sheet1.write(0, 6, 'LIST OF PLATFORMS', boldStyle)
sheet1.write(0, 7, 'RELEASE DATE', boldStyle)
sheet1.write(0, 8, 'PLAYER COUNTS', boldStyle)
sheet1.write(0, 9, 'DEVELOPERS', boldStyle)
excelCount = 1
for game, details in gameDb.items():
    rScore = details.rankedScore
    iScore = details.listCount
    aScore = rScore / details.totalCount
    if(details.completed == True):
        sheet1.write(excelCount, 0, game, crossedStyle)
    else:
        sheet1.write(excelCount, 0, game)
    #sheet1.write(excelCount, 1, details.rankedScore)
    #sheet1.write(excelCount, 2, details.listCount)
    sheet1.write(excelCount, 1, rScore)
    sheet1.write(excelCount, 2, iScore)
    #averageScore = details.rankedScore / details.listCount
    #averageScore = (details.rankedScore / details.listCount)/details.totalCount
    #averageScore = details.rankedScore / details.totalCount
    #sheet1.write(excelCount, 3, averageScore)
    sheet1.write(excelCount, 3, aScore)
    outputLists = ""
    for refList in details.listsReferencing:
        outputLists += refList
        outputLists += ", "
    sheet1.write(excelCount, 4, outputLists)
    mPlat = details.mainPlatform
    sheet1.write(excelCount, 5, mPlat)
    lPlat = details.listPlatforms
    sheet1.write(excelCount, 6, lPlat)
    rDate = details.releaseDate
    sheet1.write(excelCount, 7, rDate)
    pCounts = details.playerCounts
    sheet1.write(excelCount, 8, pCounts)
    lDevs = details.listDevelopers
    sheet1.write(excelCount, 9, lDevs)
    excelCount += 1
    #add to the individual databases
    #gameDbRanked[game] = details.rankedScore
    #gameDbInclusion[game] = details.listCount
    #gameDbAverage[game] = averageScore
    gameDbRanked[game] = rScore
    gameDbInclusion[game] = iScore
    gameDbAverage[game] = aScore
wb.save('Sorted Database.xls')
"""

#after printed out everything to excel, then make three printed sorted lists?
#each time, sort excel a certain way, then print out excel factors to list?

"""
sortByRanked = sorted(gameDbRanked.items(), key=lambda x:x[1], reverse=True)
convertedRanked = dict(sortByRanked)
sortByInclusion = sorted(gameDbInclusion.items(), key=lambda x:x[1], reverse=True)
convertedInclusion = dict(sortByInclusion)
sortByAverage = sorted(gameDbAverage.items(), key=lambda x:x[1], reverse=True)
convertedAverage = dict(sortByAverage)
"""

"""
file_ranked = open("Sorted by Ranked.txt","w", encoding="utf-8")
fileI = open("Sorted by Inclusion.txt","w", encoding="utf-8")
fileA = open("Sorted by Average.txt","w", encoding="utf-8")
fileUR = open("Sorted by Ranked (Uncompleted).txt", "w", encoding="utf-8")
fileUI = open("Sorted by Inclusion (Uncompleted).txt","w", encoding="utf-8")
fileUA = open("Sorted by Average (Uncompleted).txt","w", encoding="utf-8")
"""

"""
for game, score in convertedRanked.items():
    entry = ""
    if (gameDb[game].completed == True):
        entry += "[x]"
    entry += game.strip()
    entry += " --> "
    entry += str(score)
    file_ranked.write(entry)
    file_ranked.write("\n")
    if (gameDb[game].completed == False):
        fileUR.write(entry)
        fileUR.write("\n")
#then print out to the files for inclusion and average

for game, score in convertedInclusion.items():
    entry = ""
    if (gameDb[game].completed == True):
        entry += "[x]"
    entry += game.strip()
    #file_ranked.write(game)
    entry += " --> "
    #file_ranked.write(" --> ")
    entry += str(score)
    #file_ranked.write(str(score))
    fileI.write(entry)
    fileI.write("\n")
    if (gameDb[game].completed == False):
        fileUI.write(entry)
        fileUI.write("\n")

for game, score in convertedAverage.items():
    entry = ""
    if (gameDb[game].completed == True):
        entry += "[x]"
    entry += game.strip()
    #file_ranked.write(game)
    entry += " --> "
    #file_ranked.write(" --> ")
    entry += str(score)
    #file_ranked.write(str(score))
    fileA.write(entry)
    fileA.write("\n")
    if (gameDb[game].completed == False):
        fileUA.write(entry)
        fileUA.write("\n")
"""

"""
file_ranked.close()
fileI.close()
fileA.close()
fileUR.close()
fileUI.close()
fileUA.close()
"""

#SQLite Segment
#conn = sqlite3.connect('games.db')
#print("Games database opened successfully")
#... (EXPAND THE ACTUAL TABLE CREATION, ETC.?)
#conn.close()

#further sort by keys after sorted by values?

#print totals of the numbers of lists in each category?

#once gone through creating the lists, use separate files to mark the status of games? (completed, etc.)

list_counts = "Ranked Lists: " + str(ranked_file_count)
print(list_counts)
list_counts = "Unranked Lists: " + str(unranked_file_count)
print(list_counts)
list_counts = "Former Lists: " + str(formerFileCount)
print(list_counts)

print("LISTS USED IN PROCESS:")
for list in games_lists:
    print(list)

print()
print("Time to grab the games from the database!")
games_pulled = mon_col.find()
games_pulled_ranked = mon_col.find().sort("Ranked Score", -1)
games_pulled_inclusion = mon_col.find().sort("Inclusion Score", -1)
games_pulled_average = mon_col.find().sort("Average Score", -1)

file_ranked = open("Sorted by Ranked.txt","w", encoding="utf-8")
file_inclusion = open("Sorted by Inclusion.txt","w", encoding="utf-8")
file_average = open("Sorted by Average.txt","w", encoding="utf-8")
file_ranked_uncompleted = open("Sorted by Ranked (Uncompleted).txt", "w", encoding="utf-8")
file_inclusion_uncompleted = open("Sorted by Inclusion (Uncompleted).txt","w", encoding="utf-8")
file_average_uncompleted = open("Sorted by Average (Uncompleted).txt","w", encoding="utf-8")

for game in games_pulled_ranked:
    #print(game)
    entry = ""
    completed = game["Completed"]
    if (completed == True):
        entry += "[x]"
    entry += game['Title'].strip()
    entry += " --> "
    entry += str(game['Ranked Score'])
    file_ranked.write(entry)
    file_ranked.write("\n")
    if (completed == False):
        file_ranked_uncompleted.write(entry)
        file_ranked_uncompleted.write("\n")

for game in games_pulled_inclusion:
    entry = ""
    completed = game["Completed"]
    if (completed == True):
        entry += "[x]"
    entry += game['Title'].strip()
    entry += " --> "
    entry += str(game['Inclusion Score'])
    file_inclusion.write(entry)
    file_inclusion.write("\n")
    if (completed == False):
        file_inclusion_uncompleted.write(entry)
        file_inclusion_uncompleted.write("\n")

for game in games_pulled_average:
    entry = ""
    completed = game["Completed"]
    if (completed == True):
        entry += "[x]"
    entry += game['Title'].strip()
    entry += " --> "
    entry += str(game['Average Score'])
    file_average.write(entry)
    file_average.write("\n")
    if (completed == False):
        file_average_uncompleted.write(entry)
        file_average_uncompleted.write("\n")

#Writing to excel using new approach from MongoDB Atlas
bold_style = xlwt.easyxf('font: bold 1;')
crossed_style = xlwt.easyxf('font: struck_out 1;')
sheet1.write(0, 0, 'TITLE', bold_style)
sheet1.write(0, 1, 'RANKED SCORE', bold_style)
sheet1.write(0, 2, 'INCLUSION SCORE', bold_style)
sheet1.write(0, 3, 'AVERAGE SCORE', bold_style)
sheet1.write(0, 4, 'LISTS INCLUDED ON', bold_style)
sheet1.write(0, 5, 'MAIN PLATFORM', bold_style)
sheet1.write(0, 6, 'LIST OF PLATFORMS', bold_style)
sheet1.write(0, 7, 'RELEASE DATE', bold_style)
sheet1.write(0, 8, 'PLAYER COUNTS', bold_style)
sheet1.write(0, 9, 'DEVELOPERS', bold_style)
excel_count = 1
for game in games_pulled:
    ranked_score = game['Ranked Score']
    inclusion_score = game['Inclusion Score']
    average_score = ranked_score / game['Total Count']
    if(game['Completed'] == True):
        sheet1.write(excel_count, 0, game['Title'], crossed_style)
    else:
        sheet1.write(excel_count, 0, game['Title'])
    sheet1.write(excel_count, 1, ranked_score)
    sheet1.write(excel_count, 2, inclusion_score)
    sheet1.write(excel_count, 3, average_score)
    output_lists = ""
    for ref_list in game['List of References']:
        output_lists += ref_list
        output_lists += ", "
    sheet1.write(excel_count, 4, output_lists)
    #mPlat = details.mainPlatform
    sheet1.write(excel_count, 5, game['Main Platform'].strip())
    #lPlat = details.listPlatforms
    sheet1.write(excel_count, 6, game['List of Platforms'])
    #^Try to strip escape chars out earlier or the items themselves
    #rDate = details.releaseDate
    sheet1.write(excel_count, 7, game['Release Date'].strip())
    #pCounts = details.playerCounts
    sheet1.write(excel_count, 8, game['Player Counts'])
    # ^Try to strip escape chars out earlier or the items themselves
    #lDevs = details.listDevelopers
    sheet1.write(excel_count, 9, game['Developers'])
    # ^Try to strip escape chars out earlier or the items themselves
    excel_count += 1
wb.save('Sorted Database.xls')

print("Successfully completed!")

""""
REFERENCES:
Iterate over files in directory: https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/
https://www.w3schools.com/python/python_dictionaries.asp
https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
https://www.geeksforgeeks.org/convert-string-to-integer-in-python/
https://www.geeksforgeeks.org/python-initializing-dictionary-with-empty-lists/
https://linuxhint.com/initialize-dictionary-python/#:~:text=Another%20way%20to%20initialize%20a,print%20out%20the%20initialized%20dictionary.
https://www.geeksforgeeks.org/writing-excel-sheet-using-python/
https://stackoverflow.com/questions/9848299/importerror-no-module-named-xlwt
https://www.geeksforgeeks.org/python-increment-value-in-dictionary/
https://www.educative.io/answers/how-to-check-if-a-key-exists-in-a-python-dictionary
Factorial in python: https://www.geeksforgeeks.org/factorial-in-python/
https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file
https://kodify.net/python/math/round-integers/
https://stackoverflow.com/questions/27946595/how-to-manage-division-of-huge-numbers-in-python
https://www.geeksforgeeks.org/python-add-one-string-to-another/
Counting the number of lines in file: https://pynative.com/python-count-number-of-lines-in-file/
https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
https://www.geeksforgeeks.org/reading-writing-text-files-python/
https://www.geeksforgeeks.org/convert-integer-to-string-in-python/
https://www.geeksforgeeks.org/python-removing-newline-character-from-string/
https://github.com/python-excel/xlwt/blob/master/xlwt/Style.py
https://www.digitalocean.com/community/tutorials/python-wait-time-wait-for-input
https://www.tutorialspoint.com/sqlite/sqlite_python.htm
https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
Pymongo Tutorial: https://www.w3schools.com/python/python_mongodb_getstarted.asp
Mongodb Tutorial: https://www.w3schools.com/mongodb/mongodb_get_started.php
Add to a list: https://www.w3schools.com/python/python_lists_add.asp
How to keep sensitive data safe in an ENV file: https://forum.freecodecamp.org/t/how-to-store-a-mongodb-username-and-password-persistently-using-dotenv/50994
How to setup ENV file to work with Python: https://configu.com/blog/using-py-dotenv-python-dotenv-package-to-manage-env-variables/
Pre-commit safety: https://docs.gitguardian.com/ggshield-docs/integrations/git-hooks/pre-commit?utm_source=product&utm_medium=GitHub_checks&utm_campaign=check_run
Fix for UnicodeEncodeError after pre-commit safety integration: https://github.com/mwouts/jupytext/issues/770
Python Requests post: https://www.w3schools.com/python/ref_requests_post.asp
Python IGDB API Wrapper: https://github.com/twitchtv/igdb-api-python
"""