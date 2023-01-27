# import required module
import os
import math
# Writing to an excel
# sheet using Python
import xlwt
from xlwt import Workbook
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

    def __init__(self, rank, list, total):
        self.rankedScore = rank
        self.listCount = 1
        self.listsReferencing = []
        self.listsReferencing.append(list)
        self.totalCount = total

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

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
        startingLine = file1.readline()
        Lines = file1.readlines()
        #count = 300 # replace with grabbing how many lines there are
        count = int(startingLine)
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
        startingLine = file1.readline()
        Lines = file1.readlines()
        #count = 300 # replace with grabbing how many lines there are
        #count = int(startingLine)
        floatCount = float(startingLine)
        count = math.floor(floatCount)
        print(count)
        originalCount = count
        #do a sum of all numbers in that count
        #count = math.factorial(originalCount)
        count = originalCount * (originalCount + 1) // 2
        print(count)
        #divide the factorial by the original count
        count //= originalCount
        print(count)
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
        startingLine = file1.readline()
        Lines = file1.readlines()
        #count = 300 # replace with grabbing how many lines there are
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

gameDbRanked = {}
gameDbInclusion = {}
gameDbAverage = {}
"loop of printing database to a spreadsheet file"
# Applying multiple styles
boldStyle = xlwt.easyxf('font: bold 1;')
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

for game, score in convertedRanked.items():
    entry = game.strip()
    #fileR.write(game)
    entry += " --> "
    #fileR.write(" --> ")
    entry += str(score)
    #fileR.write(str(score))
    fileR.write(entry)
    fileR.write("\n")
#then print out to the files for inclusion and average

for game, score in convertedInclusion.items():
    entry = game.strip()
    #fileR.write(game)
    entry += " --> "
    #fileR.write(" --> ")
    entry += str(score)
    #fileR.write(str(score))
    fileI.write(entry)
    fileI.write("\n")

for game, score in convertedAverage.items():
    entry = game.strip()
    #fileR.write(game)
    entry += " --> "
    #fileR.write(" --> ")
    entry += str(score)
    #fileR.write(str(score))
    fileA.write(entry)
    fileA.write("\n")

fileR.close()
fileI.close()
fileA.close()

#further sort by keys after sorted by values?

#print totals of the numbers of lists in each category?

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
"""