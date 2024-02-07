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

# assign directory
#directory = 'C:\Users\danie\Documents\Top-Game-List-Score-Sorting\GameLists\Ranked'
directory = r'GameLists\Ranked'
#then do unranked and former

#LOOK INTO PANDAS FOR DEALING WITH TABULAR DATA IN PYTHON

#CONSIDER INCORPORATING SQL, MYSQL, NOSQL, POSTGRES, ETC. INTO THIS?

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

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

rankedFileCount = 0
unrankedFileCount = 0
formerFileCount = 0

"loop of getting the database information"
# iterate over files in
# that directory
#RANKED DIRECTORY
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        # Using readlines()
        file1 = open(f, 'r')
        rankedFileCount += 1
        startingLine = file1.readline()
        Lines = file1.readlines()
        #count = int(startingLine)
        count = len(Lines)
        print(f)
        print(len(Lines))
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

directory = r'GameLists\Unranked'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        # Using readlines()
        file1 = open(f, 'r')
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
        print(count)
        print(f)
        input('Wait to review\n')
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

directory = r'GameLists\Former'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        # Using readlines()
        file1 = open(f, 'r')
        formerFileCount += 1
        startingLine = file1.readline()
        Lines = file1.readlines()
        #count = 1
        count = int(startingLine)
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
            attribute = next(itr)
            print(attribute)
            attribute = next(itr)
            print(attribute)
            attribute = next(itr)
            print(attribute)
            attribute = next(itr)
            print(attribute)
            attribute = next(itr)
            print(attribute)
            print('')
        #else: supposed to be in database?
except StopIteration:
        pass


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

fileR = open("Sorted by Ranked.txt","w")
fileI = open("Sorted by Inclusion.txt","w")
fileA = open("Sorted by Average.txt","w")
fileUR = open("Sorted by Ranked (Uncompleted).txt", "w")
fileUI = open("Sorted by Inclusion (Uncompleted).txt","w")
fileUA = open("Sorted by Average (Uncompleted).txt","w")

for game, score in convertedRanked.items():
    entry = ""
    if (gameDb[game].completed == True):
        entry += "[x]"
    entry += game.strip()
    #fileR.write(game)
    entry += " --> "
    #fileR.write(" --> ")
    entry += str(score)
    #fileR.write(str(score))
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
    #fileR.write(game)
    entry += " --> "
    #fileR.write(" --> ")
    entry += str(score)
    #fileR.write(str(score))
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
    #fileR.write(game)
    entry += " --> "
    #fileR.write(" --> ")
    entry += str(score)
    #fileR.write(str(score))
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

#SQLite Segment
conn = sqlite3.connect('games.db')
print("Games database opened successfully")
#... (EXPAND THE ACTUAL TABLE CREATION, ETC.?)
conn.close()

#further sort by keys after sorted by values?

#print totals of the numbers of lists in each category?

#once gone through creating the lists, use separate files to mark the status of games? (completed, etc.)

listCounts = "Ranked Lists: " + str(rankedFileCount)
print(listCounts)
listCounts = "Unranked Lists: " + str(unrankedFileCount)
print(listCounts)
listCounts = "Former Lists: " + str(formerFileCount)
print(listCounts)
print("Successfully completed!")

""""
REFERENCES:
https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/
https://www.w3schools.com/python/python_dictionaries.asp
https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
https://www.geeksforgeeks.org/convert-string-to-integer-in-python/
https://www.geeksforgeeks.org/python-initializing-dictionary-with-empty-lists/
https://linuxhint.com/initialize-dictionary-python/#:~:text=Another%20way%20to%20initialize%20a,print%20out%20the%20initialized%20dictionary.
https://www.geeksforgeeks.org/writing-excel-sheet-using-python/
https://stackoverflow.com/questions/9848299/importerror-no-module-named-xlwt
https://www.geeksforgeeks.org/python-increment-value-in-dictionary/
https://www.educative.io/answers/how-to-check-if-a-key-exists-in-a-python-dictionary
https://www.geeksforgeeks.org/factorial-in-python/
https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file
https://kodify.net/python/math/round-integers/
https://stackoverflow.com/questions/27946595/how-to-manage-division-of-huge-numbers-in-python
https://www.geeksforgeeks.org/python-add-one-string-to-another/
https://pynative.com/python-count-number-of-lines-in-file/
https://www.freecodecamp.org/news/sort-dictionary-by-value-in-python/
https://www.geeksforgeeks.org/reading-writing-text-files-python/
https://www.geeksforgeeks.org/convert-integer-to-string-in-python/
https://www.geeksforgeeks.org/python-removing-newline-character-from-string/
https://github.com/python-excel/xlwt/blob/master/xlwt/Style.py
https://www.digitalocean.com/community/tutorials/python-wait-time-wait-for-input
https://www.tutorialspoint.com/sqlite/sqlite_python.htm
https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
"""