#THIS IS AN ALTERNATE VERSION OF GENERATOR, THAT ONLY ADDS NEW FILES NOT IN DATABASE

# import required module
import os
import math
# Writing to an excel
# sheet using Python33
import xlwt
from xlwt import Workbook
#SQLite
import sqlite3
#^Replacing with mongodb?
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv

# assign directory
#directory = 'C:\Users\danie\Documents\Top-Game-List-Score-Sorting\GameLists\Ranked'
directory = r'GameLists\Ranked'
#then do unranked and former

#LOOK INTO PANDAS FOR DEALING WITH TABULAR DATA IN PYTHON

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
gamesLists = []

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

rankedFileCount = 0
unrankedFileCount = 0
formerFileCount = 0

#START USING PYMONGO FOR OUTPUTTING TO MONGODB DATABASE
#Used code sample from Atlas on how to connect with Pymongo for assistance here
#Connecting to env file to get private login data
load_dotenv()
monConnect = os.getenv('MONGO_URI')
#monClient = pymongo.MongoClient(monConnect)
monClient = pymongo.MongoClient(monConnect, server_api=ServerApi('1'))
monDB = monClient["GameSorting"]
try:
    monClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
monCol = monDB["games"]
listCol = monDB["lists"]

"loop of getting the database information"
#RANKED DIRECTORY
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        list_query = { "Title": filename}
        list_count = listCol.count_documents(list_query)
        #print(filename)
        #print(list_count)
        #if(listCol.find(list_query) != None):
        if (list_count > 0):
            #print(listCol.find(list_query).count())
            print("List was already logged!")
            #input('Wait to review\n')
            continue
        else:
            print("Brand new list to log!")
            #print(f)
            # Using readlines()
            # file1 = open(f, 'r')
            file1 = open(f, 'r', encoding="utf-8")
            rankedFileCount += 1
            startingLine = file1.readline()
            Lines = file1.readlines()
            #count = int(startingLine)
            count = len(Lines)
            #print(f)
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
                #print("Score of {}: {}".format(count, line.strip()))
                count -= 1
            gamesLists.append(filename)

directory = r'GameLists\Unranked'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        list_query = {"Title": filename}
        list_count = listCol.count_documents(list_query)
        # print(filename)
        # print(list_count)
        # if(listCol.find(list_query) != None):
        if (list_count > 0):
            # print(listCol.find(list_query).count())
            print("List was already logged!")
            # input('Wait to review\n')
            continue
        else:
            print("Brand new list to log!")
            #print(f)
            # Using readlines()
            file1 = open(f, 'r', encoding="utf-8")
            unrankedFileCount += 1
            startingLine = file1.readline()
            Lines = file1.readlines()
            #count = int(startingLine)
            floatCount = float(startingLine)
            count = math.floor(floatCount)
            count = len(Lines)
            print(count)
            originalCount = count
            #do a sum of all numbers in that count
            count = originalCount * (originalCount + 1) // 2
            #divide the factorial by the original count
            count //= originalCount
            #print(count)
            #print(f)
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
                #print("Score of {}: {}".format(count, line.strip()))
                #count -= 1
            gamesLists.append(filename)

directory = r'GameLists\Former'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        list_query = {"Title": filename}
        list_count = listCol.count_documents(list_query)
        # print(filename)
        # print(list_count)
        # if(listCol.find(list_query) != None):
        if (list_count > 0):
            # print(listCol.find(list_query).count())
            print("List was already logged!")
            # input('Wait to review\n')
            continue
        else:
            print("Brand new list to log!")
            # Using readlines()
            file1 = open(f, 'r', encoding="utf-8")
            formerFileCount += 1
            startingLine = file1.readline()
            Lines = file1.readlines()
            #count = 1
            count = int(startingLine)
            originalCount = count
            #^find out how to read the line amount ahead of time
            #originalCount = len(Lines)
            #print(originalCount)
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
                #print("Score of {}: {}".format(count, line.strip()))
                #count -= 1
            gamesLists.append(filename)

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

#INSERT ALL GAMES INTO DATABASE
#export = []
print("INSERTING INTO MONGODB!")
for game, details in gameDb.items():
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
    insertion = monCol.insert_one(exportDict)
#insertion = monCol.insert_many(gameDb)
#insertion = monCol.insert_many(export)
print("TIME TO INSERT THE LISTS INTO MONGODB!")
for list in gamesLists:
    #print(list)
    listDict = {}
    listDict["Title"] = list
    #could keep track of what type of list it is, other variables?
    listInsert = listCol.insert_one(listDict)

gameDbRanked = {}
gameDbInclusion = {}
gameDbAverage = {}
"loop of printing database to a spreadsheet file"
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

#after printed out everything to excel, then make three printed sorted lists?
#each time, sort excel a certain way, then print out excel factors to list?

sortByRanked = sorted(gameDbRanked.items(), key=lambda x:x[1], reverse=True)
convertedRanked = dict(sortByRanked)
sortByInclusion = sorted(gameDbInclusion.items(), key=lambda x:x[1], reverse=True)
convertedInclusion = dict(sortByInclusion)
sortByAverage = sorted(gameDbAverage.items(), key=lambda x:x[1], reverse=True)
convertedAverage = dict(sortByAverage)

fileR = open("Sorted by Ranked.txt","w", encoding="utf-8")
fileI = open("Sorted by Inclusion.txt","w", encoding="utf-8")
fileA = open("Sorted by Average.txt","w", encoding="utf-8")
fileUR = open("Sorted by Ranked (Uncompleted).txt", "w", encoding="utf-8")
fileUI = open("Sorted by Inclusion (Uncompleted).txt","w", encoding="utf-8")
fileUA = open("Sorted by Average (Uncompleted).txt","w", encoding="utf-8")

for game, score in convertedRanked.items():
    entry = ""
    if (gameDb[game].completed == True):
        entry += "[x]"
    entry += game.strip()
    entry += " --> "
    entry += str(score)
    fileR.write(entry)
    fileR.write("\n")
    if (gameDb[game].completed == False):
        fileUR.write(entry)
        fileUR.write("\n")
#then print out to the files for inclusion and average

for game, score in convertedInclusion.items():
    entry = ""
    if (gameDb[game].completed == True):
        entry += "[x]"
    entry += game.strip()
    entry += " --> "
    entry += str(score)
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
    entry += " --> "
    entry += str(score)
    fileA.write(entry)
    fileA.write("\n")
    if (gameDb[game].completed == False):
        fileUA.write(entry)
        fileUA.write("\n")

fileR.close()
fileI.close()
fileA.close()
fileUR.close()
fileUI.close()
fileUA.close()

#further sort by keys after sorted by values?

#print totals of the numbers of lists in each category?

#once gone through creating the lists, use separate files to mark the status of games? (completed, etc.)

listCounts = "Ranked Lists: " + str(rankedFileCount)
print(listCounts)
listCounts = "Unranked Lists: " + str(unrankedFileCount)
print(listCounts)
listCounts = "Former Lists: " + str(formerFileCount)
print(listCounts)

print("LISTS USED IN PROCESS:")
for list in gamesLists:
    print(list)

print()
print("Time to grab lists from collections!")
for list in listCol.find({}, {"_id": 0}):
    print(list)

print("Successfully completed!")

""""
REFERENCES:
(EXCLUDING THE ONES ALREADY REFERENCED IN GENERATOR.PY)
Finding results from collection: https://www.w3schools.com/python/python_mongodb_find.asp
Get count for Pymongo find results: https://stackoverflow.com/questions/4415514/in-mongodbs-pymongo-how-do-i-do-a-count
"""