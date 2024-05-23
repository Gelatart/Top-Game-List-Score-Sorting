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

#Load the env variables from .env
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
print()

#add in more answer checks later? or come up with a better way to do menu progression and repeated asking?

answer_check_main = False
queries = []

or_queries = []
and_queries = []

#Split different types of similar queries that can be partnered with OR
platform_queries = []
player_count_queries = []
dev_queries = []
#release date? title? misc?
misc_queries = []
#^Try to split the natural or queries and the natural and queries? go by categories?

#Loop for the main PrintReports program (this one should be answer_check_main because different case?)
while(answer_check_main == False):
#while True:
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
        print()
        print("You have selected 1. Platform Inclusion")
        print()
        while True:
            print("Would you like to include single platforms, entire brands, generations of platform, or formats of platforms?")
            print("1. Single Platform")
            print("2. Brand of Platform")
            print("3. Generation of Platform")
            print("4. Format of Platform")
            platforms_option = input()
            if(platforms_option == '1'):
                #no real validation on this option yet? add later? has to be one of the valid numbers or valid names?
                print("Now we are going to list all of the options of platforms you can choose from")
                print("Note that the numbers are listed as so because they are the platform ID's listed in IGDB's API")
                input("Whenever you are ready, the platform options will be listed in full (For now use the text version)\n")
                print("3. Linux")
                print("4. Nintendo 64")
                print("5. Wii")
                print("6. PC (Microsoft Windows)")
                print("7. PlayStation")
                print("8. PlayStation 2")
                print("9. PlayStation 3")
                print("11. Xbox")
                print("12. Xbox 360")
                print("13. DOS")
                print("14. Mac")
                print("15. C64 & C128")
                print("16. Amiga")
                print("18. Nintendo Entertainment System")
                print("19. Super Nintendo Entertainment System")
                print("20. Nintendo DS")
                print("21. Nintendo GameCube")
                print("22. Game Boy Color")
                print("23. Dreamcast")
                print("24. Game Boy Advance")
                print("25. Amstrad CPC")
                print("26. ZX Spectrum")
                print("27. MSX")
                print("29. Sega Mega Drive/Genesis")
                print("30. Sega 32X")
                print("32. Sega Saturn")
                print("33. Game Boy")
                print("34. Android")
                print("35. Sega Game Gear")
                print("36. Xbox Live Arcade")
                print("37. Nintendo 3DS")
                print("38. PlayStation Portable")
                print("39. iOS")
                print("41. Wii U")
                print("42. N-Gage")
                print("44. Tapwave Zodiac")
                print("45. PlayStation Network")
                print("46. PlayStation Vita")
                print("47. Virtual Console")
                print("48. PlayStation 4")
                print("49. Xbox One")
                print("50. 3DO Interactive Multiplayer")
                print("51. Family Computer Disk System")
                print("52. Arcade")
                print("53. MSX2")
                print("55. Mobile")
                #print("56. WiiWare") #Removed?
                print("57. WonderSwan")
                print("58. Super Famicom")
                print("59. Atari 2600")
                print("60. Atari 7800")
                print("61. Atari Lynx")
                print("62. Atari Jaguar")
                print("63. Atari ST/STE")
                print("64. Sega Master System/Mark III")
                print("65. Atari 8-bit")
                print("66. Atari 5200")
                print("67. Intellivision")
                print("68. ColecoVision")
                print("70. Vectrex")
                print("71. Commodore VIC-20")
                print("73. BlackBerry OS")
                print("74. Windows Phone")
                print("75. Apple II")
                print("78. Sega CD")
                print("79. Neo Geo MVS")
                print("80. Neo Geo AES")
                print("84. SG-1000")
                print("86. TurboGrafx-16/PC Engine")
                print("87. Virtual Boy")
                print("88. Odyssey")
                print("89. Microvision")
                print("91. Bally Astrocade")
                print("99. Family Computer")
                print("114. Amiga CD32")
                print("117. Philips CD-i")
                print("118. FM Towns")
                print("119. Neo Geo Pocket")
                print("120. Neo Geo Pocket Color")
                print("123. WonderSwan Color")
                print("127. Fairchild Channel F")
                print("128. PC Engine SuperGrafx")
                print("129. Texas Instruments TI-99")
                print("130. Nintendo Switch")
                print("131. Nintendo PlayStation")
                print("133. Odyssey 2 / Videopac G7000")
                print("135. Hyper Neo Geo 64")
                print("136. Neo Geo CD")
                print("137. New Nintendo 3DS")
                print("138. VC 4000")
                print("139. 1292 Advanced Programmable Video System")
                print("142. PC-50X Family")
                print("149. PC-98")
                print("150. Turbografx-16/PC Engine CD")
                print("152. FM-7")
                print("159. Nintendo DSi")
                print("165. PlayStation VR")
                print("166. Pokémon mini")
                print("167. PlayStation 5")
                print("169. Xbox Series X|S")
                print("170. Google Stadia")
                print("240. Zeebo")
                print("274. PC-FX")
                print("306. Satellaview")
                print("307. Game & Watch")
                print("308. Playdia")
                print("309. Evercade")
                print("339. Sega Pico")
                print("375. Epoch Cassette Vision")
                print("376. Epoch Super Cassette Vision")
                print("378. Gamate")
                print("379. Game.com")
                print("381. Playdate")
                print("390. PlayStation VR2")
                print("407. HyperScan")
                print("410. Atari Jaguar CD")
                print("412. Leapster")
                print("413. Leapster Explorer/LeadPad Explorer")
                print("414. LeapTV")
                print("417. Palm OS")
                print("439. V.Smile")
                print("440. Visual Memory Unit / Visual Memory System")
                print("441. PocketStation")
                print("471. Meta Quest 3")
                print("476. Apple Pippin")
                print("477. Panasonic Jungle")
                print("478. Panasonic M2")
                print("486. Digiblast")
                print("Which platform would you like to include?")
                #have function to check if number just given was one of the valid options?
                #going to go off of IGDB ID's for now, need to keep adding more
                platform_selection = input()
                new_query = {"List of Platforms": platform_selection}
                queries.append(new_query)
                platform_queries.append(new_query)
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif (platforms_option == '2'):
                while True:
                    """
                    TYPE FOR PLATFORM FAMILIES (Based on id #):
                    1: PlayStation
                    2: Xbox
                    3: Sega
                    4: Linux
                    5: Nintendo
                    """
                    #use or approach within family types?
                    print("Which brand of platform would you like to include?")
                    print("1. Sony (PlayStation)")
                    print("2. Microsoft (Xbox)")
                    print("3. Sega")
                    print("4. Linux")
                    print("5. Nintendo")
                    print("6. Atari") #doesn't have a family
                    #others? neo geo? apple? windows?
                    brand_option = int(input())
                    if (brand_option > 0 and brand_option < 5):
                        #platform family approach, just grab the value and plug it in?
                        #store platform family value? if/elif case or api endpoint to store it?
                        print("ONE OF THE FAMILY OPTIONS")
                        if (brand_option == 1):
                            #playstation family
                            #PlayStation
                            #PlayStation 2
                            #PlayStation 3
                            #PlayStation 4
                            #PlayStation 5
                            #PlayStation Portable
                            #PlayStation Vita
                            #PlayStation VR
                            #PlayStation VR2
                            #PocketStation
                            new_query = {"List of Platforms": "PlayStation"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PlayStation 2"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PlayStation 3"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PlayStation 4"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PlayStation 5"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PlayStation Portable"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PlayStation Vita"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PlayStation VR"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PlayStation VR2"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "PocketStation"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                        elif (brand_option == 2):
                            #xbox family
                            #Xbox
                            #Xbox 360
                            #Xbox One
                            #
                            new_query = {"List of Platforms": "Xbox"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Xbox 360"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Xbox One"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Xbox Series X|S"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                        elif (brand_option == 3):
                            #sega family
                            #SG-1000
                            #Sega Master System/Mark III
                            #Sega Mega Drive/Genesis
                            #Sega CD
                            #Sega 32X
                            #Sega Saturn
                            #Dreamcast
                            #Visual Memory Unit / Visual Memory System
                            #Sega Game Gear
                            #Sega Pico
                            new_query = {"List of Platforms": "SG-1000"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Sega Master System/Mark III"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Sega Mega Drive/Genesis"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Sega CD"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Sega 32X"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Sega Saturn"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Dreamcast"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Visual Memory Unit / Visual Memory System"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Sega Game Gear"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Sega Pico"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                        elif (brand_option == 4):
                            #linux family
                            #Linux
                            #Android
                            #Google Stadia
                            new_query = {"List of Platforms": "Linux"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Android"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Google Stadia"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                        elif (brand_option == 5):
                            #nintendo family
                            #Nintendo Entertainment System
                            #Super Nintendo Entertainment System
                            #Nintendo 64
                            #Nintendo GameCube
                            #Wii
                            #Wii U
                            #Nintendo Switch
                            #Game & Watch
                            #Game Boy
                            #Game Boy Color
                            #Virtual Boy
                            #Game Boy Advance
                            #Nintendo DS
                            #Nintendo DSi
                            #Nintendo 3DS
                            #New Nintendo 3DS
                            #Family Computer
                            #Family Computer Disk System
                            #Super Famicom
                            #Satellaview
                            #Pokémon mini
                            #Virtual Console
                            #Nintendo PlayStation
                            #any others missing? wiiware (removed?)? nintendo eshop (removed?)?
                            new_query = {"List of Platforms": "Nintendo Entertainment System"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Super Nintendo Entertainment System"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Nintendo 64"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Nintendo GameCube"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Wii"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Wii U"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Nintendo Switch"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Game Boy"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Game Boy Color"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Virtual Boy"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Game Boy Advance"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Nintendo DS"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Nintendo DSi"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Nintendo 3DS"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "New Nintendo 3DS"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Family Computer"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Family Computer Disk System"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Super Famicom"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Pokémon mini"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Virtual Console"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                            new_query = {"List of Platforms": "Nintendo PlayStation"}
                            queries.append(new_query)
                            platform_queries.append(new_query)
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (brand_option == 6):
                        #we arrange this one ourselves for atari options
                        #consider making my own atari family in a platform family category in the mongo cluster?
                        print("LONER ATARI")
                        """
                        ATARI PLATFORMS:
                        Atari 2600 (59)
                        Atari 7800 (60)
                        Atari Lynx (61)
                        Atari Jaguar (62)
                        Atari ST/STE (63)
                        Atari 8-bit (65)
                        Atari 5200 (66)
                        Atari Jaguar CD (410)
                        """
                        #...
                        new_query = {"List of Platforms": "Atari 2600"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari 7800"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari Lynx"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari Jaguar"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari ST/STE"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari 8-bit"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari 5200"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari Jaguar CD"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.\n")
                        print()
                        continue
                break
            elif (platforms_option == '3'):
                while True:
                    # elif 3
                    print("Which generation of platform would you like to include?")
                    print("Note: For formats not split by generation (ex. PC and Arcade), you will likely want to go by format")
                    print("1. 1st-Generation Consoles")
                    print("2. 2nd-Generation Consoles")
                    print("3. 3rd-Generation Consoles")
                    print("4. 4th-Generation Consoles")
                    print("5. 5th-Generation Consoles")
                    print("6. 6th-Generation Consoles")
                    print("7. 7th-Generation Consoles")
                    print("8. 8th-Generation Consoles")
                    print("9. 9th-Generation Consoles")
                    # include options for non-gen platforms? Like PC/operating system, arcade, etc.?
                    generation_option = input()
                    # Generation 1:
                    #Odyssey
                    #PC-50X Family
                    #---(^from igdb query for gen 1)
                    #Home Pong series (unfound?)
                    #TV Tennis Electrotennis (unfound?)
                    #Coleco Telstar (unfound?)
                    #Color TV-Game (unfound?)
                    # ...?

                    # Generation 2:
                    #Atari 2600
                    #Atari 5200
                    #Intellivision
                    #ColecoVision
                    #Odyssey 2 / Videopac G7000
                    #Game & Watch
                    #Fairchild Channel F
                    #Vectrex
                    #Epoch Cassette Vision
                    #1292 Advanced Programmable Video System
                    #VC 4000
                    #Bally Astrocade
                    #Microvision
                    # ...?

                    # Generation 3:
                    #Nintendo Entertainment System
                    #Family Computer
                    #Family Computer Disk System
                    #Sega Master System/Mark III
                    #SG-1000
                    #Atari 7800
                    #Epoch Super Cassette Vision
                    #___
                    #Atari XEGS (unfound?)
                    # ...?

                    # Generation 4:
                    #Super Nintendo Entertainment System
                    #Super Famicom
                    #Satellaview
                    #Game Boy
                    #Sega Mega Drive/Genesis
                    #Sega CD
                    #Sega 32X
                    #Sega Game Gear
                    #Sega Pico
                    #TurboGrafx-16/PC Engine
                    #Turbografx-16/PC Engine CD
                    #PC Engine SuperGrafx
                    #Neo Geo AES
                    #Neo Geo CD
                    #Atari Lynx
                    #Philips CD-i
                    #Gamate
                    #Nintendo PlayStation (cancelled)
                    # ...?

                    #Generation 5:
                    #Nintendo 64
                    #Game Boy Color
                    #Virtual Boy
                    #Sega Saturn
                    #PlayStation
                    #PocketStation
                    #PC-FX
                    #Neo Geo Pocket
                    #Neo Geo Pocket Color
                    #Atari Jaguar
                    #Atari Jaguar CD
                    #3DO Interactive Multiplayer
                    #Amiga CD32
                    #WonderSwan
                    #WonderSwan Color
                    #Apple Pippin
                    #Playdia
                    #...?
                    #FM Towns Marty (unfound?)

                    #Generation 6:
                    #Nintendo GameCube
                    #Game Boy Advance
                    #Dreamcast
                    #Visual Memory Unit / Visual Memory System
                    #PlayStation 2
                    #Xbox
                    #N-Gage
                    #Leapster
                    #V.Smile
                    #Panasonic M2 (cancelled)
                    #...?

                    #Generation 7:
                    #Wii
                    #Nintendo DS
                    #Nintendo DSi
                    #PlayStation 3
                    #PlayStation Portable
                    #Xbox 360
                    #Zeebo
                    #HyperScan
                    #Leapster Explorer/LeadPad Explorer
                    #Digiblast
                    #...?

                    #Generation 8:
                    #Wii U
                    #Nintendo Switch (special case)
                    #Nintendo 3DS
                    #New Nintendo 3DS
                    #PlayStation 4
                    #PlayStation Vita
                    #PlayStation VR
                    #Xbox One
                    #Evercade
                    #LeapTV
                    #Panasonic Jungle (cancelled)
                    #...?

                    #Generation 9:
                    #PlayStation 5
                    #PlayStation VR2
                    #Xbox Series X|S
                    #Meta Quest 3
                    #Playdate
                    # ...?

                    #Handhelds with no results:
                    #TurboExpress / PC Engine GT
                    #Watara Supervision
                    #...?

                    if(generation_option == "1"):
                        # Generation 1:
                        # Odyssey
                        # PC-50X Family
                        new_query = {"List of Platforms": "Odyssey"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PC-50X Family"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 1 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif(generation_option == "2"):
                        # Generation 2:
                        # Atari 2600
                        # Atari 5200
                        # Intellivision
                        # ColecoVision
                        # Odyssey 2 / Videopac G7000
                        # Game & Watch
                        # Fairchild Channel F
                        # Vectrex
                        # Epoch Cassette Vision
                        # 1292 Advanced Programmable Video System
                        # VC 4000
                        # Bally Astrocade
                        # Microvision
                        new_query = {"List of Platforms": "Atari 2600"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari 5200"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Intellivision"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "ColecoVision"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Odyssey 2 / Videopac G7000"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Game & Watch"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Fairchild Channel F"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Vectrex"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Epoch Cassette Vision"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "1292 Advanced Programmable Video System"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "VC 4000"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Bally Astrocade"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Microvision"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 2 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "3"):
                        # Generation 3:
                        # Nintendo Entertainment System
                        # Family Computer
                        # Family Computer Disk System
                        # Sega Master System/Mark III
                        # SG-1000
                        # Atari 7800
                        # Epoch Super Cassette Vision
                        new_query = {"List of Platforms": "Nintendo Entertainment System"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Family Computer"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Family Computer Disk System"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Sega Master System/Mark III"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "SG-1000"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari 7800"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Epoch Super Cassette Vision"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 3 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "4"):
                        # Generation 4:
                        # Super Nintendo Entertainment System
                        # Super Famicom
                        # Satellaview
                        # Game Boy
                        # Sega Mega Drive/Genesis
                        # Sega CD
                        # Sega 32X
                        # Sega Game Gear
                        # Sega Pico
                        # TurboGrafx-16/PC Engine
                        # Turbografx-16/PC Engine CD
                        # PC Engine SuperGrafx
                        # Neo Geo AES
                        # Neo Geo CD
                        # Atari Lynx
                        # Philips CD-i
                        # Gamate
                        new_query = {"List of Platforms": "Super Nintendo Entertainment System"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Super Famicom"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Satellaview"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Game Boy"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Sega Mega Drive/Genesis"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Sega CD"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Sega 32X"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Sega Game Gear"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Sega Pico"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "TurboGrafx-16/PC Engine"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Turbografx-16/PC Engine CD"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PC Engine SuperGrafx"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Neo Geo AES"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Neo Geo CD"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari Lynx"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Philips CD-i"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Gamate"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 4 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "5"):
                        # Generation 5:
                        # Nintendo 64
                        # Game Boy Color
                        # Virtual Boy
                        # Sega Saturn
                        # PlayStation
                        # PocketStation
                        # PC-FX
                        # Neo Geo Pocket
                        # Neo Geo Pocket Color
                        # Atari Jaguar
                        # Atari Jaguar CD
                        # 3DO Interactive Multiplayer
                        # Amiga CD32
                        # WonderSwan
                        # WonderSwan Color
                        # Apple Pippin
                        # Playdia
                        new_query = {"List of Platforms": "Nintendo 64"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Game Boy Color"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Virtual Boy"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Sega Saturn"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PlayStation"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PocketStation"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PC-FX"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Neo Geo Pocket"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Neo Geo Pocket Color"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari Jaguar"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Atari Jaguar CD"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "3DO Interactive Multiplayer"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Amiga CD32"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "WonderSwan"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "WonderSwan Color"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Apple Pippin"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Playdia"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 5 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "6"):
                        # Generation 6:
                        # Nintendo GameCube
                        # Game Boy Advance
                        # Dreamcast
                        # Visual Memory Unit / Visual Memory System
                        # PlayStation 2
                        # Xbox
                        # N-Gage
                        # Leapster
                        # V.Smile
                        new_query = {"List of Platforms": "Nintendo GameCube"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Game Boy Advance"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Dreamcast"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Visual Memory Unit / Visual Memory System"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PlayStation 2"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Xbox"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "N-Gage"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Leapster"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "V.Smile"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 6 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "7"):
                        # Generation 7:
                        # Wii
                        # Nintendo DS
                        # Nintendo DSi
                        # PlayStation 3
                        # PlayStation Portable
                        # Xbox 360
                        # Zeebo
                        # HyperScan
                        # Leapster Explorer/LeadPad Explorer
                        # Digiblast
                        new_query = {"List of Platforms": "Wii"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Nintendo DS"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Nintendo DSi"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PlayStation 3"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PlayStation Portable"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Xbox 360"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Zeebo"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "HyperScan"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Leapster Explorer/LeadPad Explorer"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Digiblast"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 7 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "8"):
                        # Generation 8:
                        # Wii U
                        # Nintendo Switch (special case)
                        # Nintendo 3DS
                        # New Nintendo 3DS
                        # PlayStation 4
                        # PlayStation Vita
                        # PlayStation VR
                        # Xbox One
                        # Evercade
                        # LeapTV
                        new_query = {"List of Platforms": "Wii U"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Nintendo Switch"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Nintendo 3DS"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "New Nintendo 3DS"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PlayStation 4"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PlayStation Vita"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PlayStation VR"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Xbox One"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Evercade"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "LeapTV"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 8 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "9"):
                        # PlayStation 5
                        # PlayStation VR2
                        # Xbox Series X|S
                        # Meta Quest 3
                        # Playdate
                        new_query = {"List of Platforms": "PlayStation 5"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "PlayStation VR2"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Xbox Series X|S"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Meta Quest 3"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Playdate"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Generation 9 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.\n")
                        print()
                        continue
                break
            elif (platforms_option == '4'):
                while True:
                    print("Which format of platform would you like to include?")
                    print("1. Console")
                    print("2. Handheld")
                    print("3. Computer / Desktop OS")
                    print("4. Arcade")
                    print("5. Mobile Phone")
                    print("6. Virtual Reality")
                    print("7. Platform")
                    platform_format = input()
                    if (platform_format == "1"):
                        #Console
                        print()
                        #... (console querying)
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "2"):
                        #Handheld
                        print()
                        # ... (console querying)
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "3"):
                        #Computer / Desktop OS
                        #DOS
                        #PC (Microsoft Windows)
                        print()
                        # ... (console querying)
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "4"):
                        #Arcade
                        print()
                        print("Grabbing arcade platforms")
                        print()
                        #Arcade
                        #Neo Geo MVS
                        #Hyper Neo Geo 64
                        #...?
                        new_query = {"List of Platforms": "Arcade"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Neo Geo MVS"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        new_query = {"List of Platforms": "Hyper Neo Geo 64"}
                        queries.append(new_query)
                        platform_queries.append(new_query)
                        print("Arcade platforms added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "5"):
                        #Mobile Phone
                        #iOS
                        #BlackBerry OS
                        #Windows Phone
                        #Palm OS
                        print()
                        # ... (console querying)
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "6"):
                        #Virtual Reality
                        print()
                        # ... (console querying)
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "7"):
                        #Platform
                        print()
                        # ... (console querying)
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.\n")
                        print()
                        continue
                    #...?
                break
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.\n")
                print()
                continue
        print("Returning back to main menu")
        print()
    elif (filter_category == '2'):
        #import some of the platform inclusion options over here?
        print()
        print("You have selected 2. Main Platform")
        print()
        print("Which platform would you like to be the main platform?")
        print("Note that the numbers are listed as so because they are the platform ID's listed in IGDB's API")
        input("Whenever you are ready, the platform options will be listed in full (For now use the text version)\n")
        print("3. Linux")
        print("4. Nintendo 64")
        print("5. Wii")
        print("6. PC (Microsoft Windows)")
        print("7. PlayStation")
        print("8. PlayStation 2")
        print("9. PlayStation 3")
        print("11. Xbox")
        print("12. Xbox 360")
        print("13. DOS")
        print("14. Mac")
        print("15. C64 & C128")
        print("16. Amiga")
        print("18. Nintendo Entertainment System")
        print("19. Super Nintendo Entertainment System")
        print("20. Nintendo DS")
        print("21. Nintendo GameCube")
        print("22. Game Boy Color")
        print("23. Dreamcast")
        print("24. Game Boy Advance")
        print("25. Amstrad CPC")
        print("26. ZX Spectrum")
        print("27. MSX")
        print("29. Sega Mega Drive/Genesis")
        print("30. Sega 32X")
        print("32. Sega Saturn")
        print("33. Game Boy")
        print("34. Android")
        print("35. Sega Game Gear")
        print("36. Xbox Live Arcade")
        print("37. Nintendo 3DS")
        print("38. PlayStation Portable")
        print("39. iOS")
        print("41. Wii U")
        print("42. N-Gage")
        print("44. Tapwave Zodiac")
        print("45. PlayStation Network")
        print("46. PlayStation Vita")
        print("47. Virtual Console")
        print("48. PlayStation 4")
        print("49. Xbox One")
        print("50. 3DO Interactive Multiplayer")
        print("51. Family Computer Disk System")
        print("52. Arcade")
        print("53. MSX2")
        print("55. Mobile")
        # print("56. WiiWare") #Removed?
        print("57. WonderSwan")
        print("58. Super Famicom")
        print("59. Atari 2600")
        print("60. Atari 7800")
        print("61. Atari Lynx")
        print("62. Atari Jaguar")
        print("63. Atari ST/STE")
        print("64. Sega Master System/Mark III")
        print("65. Atari 8-bit")
        print("66. Atari 5200")
        print("67. Intellivision")
        print("68. ColecoVision")
        print("70. Vectrex")
        print("71. Commodore VIC-20")
        print("73. BlackBerry OS")
        print("74. Windows Phone")
        print("75. Apple II")
        print("78. Sega CD")
        print("79. Neo Geo MVS")
        print("80. Neo Geo AES")
        print("84. SG-1000")
        print("86. TurboGrafx-16/PC Engine")
        print("87. Virtual Boy")
        print("88. Odyssey")
        print("89. Microvision")
        print("91. Bally Astrocade")
        print("99. Family Computer")
        print("114. Amiga CD32")
        print("117. Philips CD-i")
        print("118. FM Towns")
        print("119. Neo Geo Pocket")
        print("120. Neo Geo Pocket Color")
        print("123. WonderSwan Color")
        print("127. Fairchild Channel F")
        print("128. PC Engine SuperGrafx")
        print("129. Texas Instruments TI-99")
        print("130. Nintendo Switch")
        print("131. Nintendo PlayStation")
        print("133. Odyssey 2 / Videopac G7000")
        print("135. Hyper Neo Geo 64")
        print("136. Neo Geo CD")
        print("137. New Nintendo 3DS")
        print("138. VC 4000")
        print("139. 1292 Advanced Programmable Video System")
        print("142. PC-50X Family")
        print("149. PC-98")
        print("150. Turbografx-16/PC Engine CD")
        print("152. FM-7")
        print("159. Nintendo DSi")
        print("165. PlayStation VR")
        print("166. Pokémon mini")
        print("167. PlayStation 5")
        print("169. Xbox Series X|S")
        print("170. Google Stadia")
        print("240. Zeebo")
        print("274. PC-FX")
        print("306. Satellaview")
        print("307. Game & Watch")
        print("308. Playdia")
        print("309. Evercade")
        print("339. Sega Pico")
        print("375. Epoch Cassette Vision")
        print("376. Epoch Super Cassette Vision")
        print("378. Gamate")
        print("379. Game.com")
        print("381. Playdate")
        print("390. PlayStation VR2")
        print("407. HyperScan")
        print("410. Atari Jaguar CD")
        print("412. Leapster")
        print("413. Leapster Explorer/LeadPad Explorer")
        print("414. LeapTV")
        print("417. Palm OS")
        print("439. V.Smile")
        print("440. Visual Memory Unit / Visual Memory System")
        print("441. PocketStation")
        print("471. Meta Quest 3")
        print("476. Apple Pippin")
        print("477. Panasonic Jungle")
        print("478. Panasonic M2")
        print("486. Digiblast")
        print("Which platform would you like to include?")
        # have function to check if number just given was one of the valid options?
        # going to go off of IGDB ID's for now, need to keep adding more
        platform_selection = input()
        new_query = {"Main Platform": platform_selection}
        queries.append(new_query)
        platform_queries.append(new_query)
        print("Returning back to main menu")
        print()
    elif (filter_category == '3'):
        print()
        print("You have selected 3. Release Date")
        print()
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
            print()
        print("Returning back to main menu")
        print()
    elif (filter_category == '4'):
        print()
        print("You have selected 4. Completion Status")
        print()
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
            print()
        print("Returning back to main menu")
        print()
    elif (filter_category == '5'):
        #NOT WORKING YET!!!
        #try search api endpoint?
        print()
        print("You have selected 5. Title")
        print()
        print("Would you like to enter a filter string to use in filtering results?")
        title_search = input("If so, specify your filter string here: ")
        #new_query = { "Title": { "$text:": title_search}}
        #new_query = mon_col.aggregate([{"$search": {"text:": {"query": title_search, "path": "Title"}}}])
        #new_query = mon_col.find({"$text": {"$search": title_search}})
        new_query = {"$text": {"$search": title_search}}
        #new_query = {"Title": {"$search": title_search}}
        #Trying to figure this out, not working properly, need to have properly built index I refer to?
        queries.append(new_query)
        print("Returning back to main menu")
        print()
    elif (filter_category == '6'):
        print()
        print("You have selected 6. Ranked Score")
        print()
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
            print()
        #...
        print("Returning back to main menu")
        print()
    elif (filter_category == '7'):
        print()
        print("You have selected 7. Inclusion Score")
        print()
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
            print()
        #...
        print("Returning back to main menu")
        print()
    elif (filter_category == '8'):
        print()
        print("You have selected 8. Average Score")
        print()
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
            print()
        #...
        print("Returning back to main menu")
        print()
    elif (filter_category == '9'):
        print()
        print("You have selected 9. Player Count")
        print()
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
                print()
            new_query = {"Player Count": target_count}
            queries.append(new_query)
            player_count_queries.append(new_query)
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
            print()
        #...
        print("Returning back to main menu")
        print()
    elif (filter_category == '10'):
        print()
        print("You have selected 10. Developers")
        print()
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
            dev_queries.append(new_query)
        else:
            print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
            print()
        #going to be using involvedcompany and company?
        #...
        print("Returning back to main menu")
        print()
    elif (filter_category == '11'):
        print()
        print("You have selected 11. Miscellaneous")
        print()
        print("This is for miscellaneous filter options that don't fit easily anywhere else")
        print()
        #Fill this if anything comes to mind that I'd like to filter for that doesn't fit in one of the other options
        print("Returning back to main menu")
        print()
    elif(filter_category == '12'):
        print()
        #answer_check_main = True
        if(len(queries) == 0):
            print("Hey, there's nothing here! We have to go back to have something to work with")
            input("When you are ready, press Enter to go back to the main print menu\n")
            continue
        else:
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
            #Loop for the AND/OR approach and the sorting
            while True:
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
                if(and_or_type == '1'):
                    #AND approach
                    if (sort_type == '1'):
                        # games_pulled = mon_col.find(custom_query).sort("Ranked Score", -1)
                        games_pulled = mon_col.find({'$and': queries}).sort("Ranked Score", -1)
                        break
                    elif (sort_type == '2'):
                        games_pulled = mon_col.find({'$and': queries}).sort("Inclusion Score", -1)
                        break
                    elif (sort_type == '3'):
                        games_pulled = mon_col.find({'$and': queries}).sort("Average Score", -1)
                        break
                    else:
                        print("Sorry, I don't understand")
                        print()
                        continue
                        # check again
                elif(and_or_type == '2'):
                    #OR approach
                    if(sort_type == '1'):
                        games_pulled = mon_col.find({'$or': queries}).sort("Ranked Score", -1)
                        break
                    elif (sort_type == '2'):
                        games_pulled = mon_col.find({'$or': queries}).sort("Inclusion Score", -1)
                        break
                    elif (sort_type == '3'):
                        games_pulled = mon_col.find({'$or': queries}).sort("Average Score", -1)
                        break
                    else:
                        print("Sorry, I don't understand")
                        print()
                        continue
                        # check again
                elif (and_or_type == '3'):
                    #NATURAL approach
                    """
                    platform_queries = []
                    player_count_queries = []
                    dev_queries = []
                    ---
                    misc_queries = []
                    """
                    #Make sure that none of the arrays are empty because that'll break it, switch approach if so?
                    natural_platform = {'$or': platform_queries}
                    natural_player = {'$or': player_count_queries}
                    natural_dev = {'$or': dev_queries}
                    and_queries = []
                    and_queries.append(natural_platform)
                    and_queries.append(natural_player)
                    and_queries.append(natural_dev)
                    and_queries.append(misc_queries)
                    natural_queries = {'$and': and_queries}
                    if (sort_type == '1'):
                        games_pulled = mon_col.find(natural_queries).sort("Ranked Score", -1)
                        break
                    elif (sort_type == '2'):
                        games_pulled = mon_col.find(natural_queries).sort("Inclusion Score", -1)
                        break
                    elif (sort_type == '3'):
                        games_pulled = mon_col.find(natural_queries).sort("Average Score", -1)
                        break
                    else:
                        print("Sorry, I don't understand")
                        print()
                        continue
                        # check again
                else:
                    print("Sorry, I don't understand")
                    print()
                    continue
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
            while True:
                print("Your custom report has finished printing! Would you like to print more reports? Or quit the program")
                print("1. Print more reports")
                print("2. Quit the program")
                continue_check = input()
                if(continue_check == '1'):
                    print("Alright, let's get back to the main printing menu!")
                    break
                elif(continue_check == '2'):
                    answer_check_main = True
                    print("Hope you enjoyed printing reports! See you later!")
                    print()
                    break
                else:
                    print("I'm sorry, I don't understand")
                    print()
                    continue
                    #check again
    else:
        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
        print()
        continue

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
Ask user for input until get valid response: https://www.python-engineer.com/posts/ask-user-for-input/
Building queries with AND and OR: https://stackoverflow.com/questions/11196101/mongodb-queries-both-with-and-and-or
"""