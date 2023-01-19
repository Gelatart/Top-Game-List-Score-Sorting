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

"gameDb is a dict of string titles and game object values"
gameDb = {}
"game object needs two scores"
class GameObject:
    def __init__(self, rank):
        self.rankedScore = rank
        self.listCount = 1
        self.listsReferencing = []

    #def __init__(self, rank, count):
    #    self.rankedScore = rank
    #    self.listCount = count

    def __init__(self, rank, list):
        self.rankedScore = rank
        self.listCount = 1
        self.listsReferencing = []
        self.listsReferencing.append(list)

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
        # Strips the newline character
        for line in Lines:
            if line in gameDb:
                gameDb[line].rankedScore += count
                gameDb[line].listCount += 1
                gameDb[line].listsReferencing.append(f)
            else:
                newObj = GameObject(count, f)
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
            else:
                newObj = GameObject(count, f)
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
        # Strips the newline character
        for line in Lines:
            if line in gameDb:
                gameDb[line].rankedScore += count
                gameDb[line].listCount += 1
                gameDb[line].listsReferencing.append(f)
            else:
                newObj = GameObject(count, f)
                gameDb[line] = newObj
            #searchObj = gameDb.get(newObj, 0) + 1
            #gameDb[line].listCount = gameDb.get(newObj, 0) + 1
            print("Score of {}: {}".format(count, line.strip()))
            #count -= 1

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
    sheet1.write(excelCount, 0, game)
    sheet1.write(excelCount, 1, details.rankedScore)
    sheet1.write(excelCount, 2, details.listCount)
    averageScore = details.rankedScore / details.listCount
    sheet1.write(excelCount, 3, averageScore)
    outputLists = ""
    for refList in details.listsReferencing:
        outputLists += refList
        outputLists += ", "
    sheet1.write(excelCount, 4, outputLists)
    excelCount += 1
wb.save('Sorted Database.xls')

print("Successfully completed!")

""""
REFS:
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
"""