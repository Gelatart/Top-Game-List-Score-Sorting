#Imports grabbed from generator.py I thought I might need
import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from dotenv import load_dotenv
import datetime

#look for spots with redundancy to turn into inner functions?

#make program that can run a bunch of different report generations at once based on custom preset configs?
#use files to supply these configs?

def print_platforms():
    #Spun off into its own function so we don't have to worry about maintaining multiple versions of data in-code
    #Just grab it from here when needed
    print("Here are all the platforms that there are!")
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
    print("15. Commodore C64/128/MAX")
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
    print("55. Legacy Mobile Device")
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
    print("69. BBC Microcomputer System")
    print("70. Vectrex")
    print("71. Commodore VIC-20")
    print("72. Ouya")
    print("73. BlackBerry OS")
    print("74. Windows Phone")
    print("75. Apple II")
    print("77. Sharp X1")
    print("78. Sega CD")
    print("79. Neo Geo MVS")
    print("80. Neo Geo AES")
    print("82. Web browser")
    print("84. SG-1000")
    print("85. Donner Model 30")
    print("86. TurboGrafx-16/PC Engine")
    print("87. Virtual Boy")
    print("88. Odyssey")
    print("89. Microvision")
    print("90. Commodore PET")
    print("91. Bally Astrocade")
    #print("92. SteamOS") #Removed?
    print("93. Commodore 16")
    print("94. Commodore Plus/4")
    print("95. PDP-1")
    print("96. PDP-10")
    print("97. PDP-8")
    print("98. DEC GT40")
    print("99. Family Computer")
    print("100. Analogue electronics")
    print("101. Ferranti Nimrod Computer")
    print("102. EDSAC")
    print("103. PDP-7")
    print("104. HP 2100")
    print("105. HP 3000")
    print("106. HP SDS Sigma 7")
    print("107. Call-A-Computer time-shared mainframe computer system")
    print("108. PDP-11")
    print("109. CDC Cyber 70")
    print("110. PLATO")
    print("111. Imlac PDS-1")
    print("112. Microcomputer")
    print("113. OnLive Game System")
    print("114. Amiga CD32")
    print("115. Apple IIGS")
    print("116. Acorn Archimedes")
    print("117. Philips CD-i")
    print("118. FM Towns")
    print("119. Neo Geo Pocket")
    print("120. Neo Geo Pocket Color")
    print("121. Sharp X68000")
    print("122. Nuon")
    print("123. WonderSwan Color")
    print("124. SwanCrystal")
    print("125. PC-8800 Series")
    print("126. TRS-80")
    print("127. Fairchild Channel F")
    print("128. PC Engine SuperGrafx")
    print("129. Texas Instruments TI-99")
    print("130. Nintendo Switch")
    print("131. Nintendo PlayStation")
    print("132. Amazon Fire TV")
    print("133. Odyssey 2 / Videopac G7000")
    print("134. Acorn Electron")
    print("135. Hyper Neo Geo 64")
    print("136. Neo Geo CD")
    print("137. New Nintendo 3DS")
    print("138. VC 4000")
    print("139. 1292 Advanced Programmable Video System")
    print("140. AY-3-8500")
    print("141. AY-3-8610")
    print("142. PC-50X Family")
    print("143. AY-3-8760")
    print("144. AY-3-8710")
    print("145. AY-3-8603")
    print("146. AY-3-8605")
    print("147. AY-3-8606")
    print("148. AY-3-8607")
    print("149. PC-9800 Series")
    print("150. Turbografx-16/PC Engine CD")
    print("151. TRS-80 Color Computer")
    print("152. FM-7")
    print("153. Dragon 32/64")
    print("154. Amstrad PCW")
    print("155. Tatung Einstein")
    print("156. Thomson MO5")
    print("157. NEC PC-6000 Series")
    print("158. Commodore CDTV")
    print("159. Nintendo DSi")
    # print("160. Nintendo eShop") #Removed?
    print("161. Windows Mixed Reality")
    print("162. Oculus VR")
    print("163. SteamVR")
    print("164. Daydream")
    print("165. PlayStation VR")
    print("166. Pokémon mini")
    print("167. PlayStation 5")
    print("169. Xbox Series X|S")
    print("170. Google Stadia")
    print("238. DVD Player")
    print("240. Zeebo")
    print("274. PC-FX")
    print("306. Satellaview")
    print("307. Game & Watch")
    print("308. Playdia")
    print("309. Evercade")
    print("339. Sega Pico")
    print("372. OOParts")
    print("374. Sharp MZ-2200")
    print("375. Epoch Cassette Vision")
    print("376. Epoch Super Cassette Vision")
    print("377. Plug & Play")
    print("378. Gamate")
    print("379. Game.com")
    print("380. Casio Loopy")
    print("381. Playdate")
    print("382. Intellivision Amico")
    print("384. Oculus Quest")
    print("385. Oculus Rift")
    print("386. Meta Quest 2")
    print("390. PlayStation VR2")
    print("405. Windows Mobile")
    print("407. HyperScan")
    print("410. Atari Jaguar CD")
    print("411. Handheld Electronic LCD")
    print("412. Leapster")
    print("413. Leapster Explorer/LeadPad Explorer")
    print("414. LeapTV")
    print("416. Nintendo 64DD")
    print("417. Palm OS")
    print("439. V.Smile")
    print("440. Visual Memory Unit / Visual Memory System")
    print("441. PocketStation")
    print("471. Meta Quest 3")
    print("474. Gizmondo")
    print("476. Apple Pippin")
    print("477. Panasonic Jungle")
    print("478. Panasonic M2")
    print("486. Digiblast")
    #any others needed?
    #input()
    print()

def print_genres():
    #Spun off into its own function so we don't have to worry about maintaining multiple versions of data in-code
    #Just grab it from here when needed
    print("Here are all the genres that there are!")
    print("2. Point-and-click")
    print("4. Fighting")
    print("5. Shooter")
    print("7. Music")
    print("8. Platform")
    print("9. Puzzle")
    print("10. Racing")
    print("11. Real Time Strategy (RTS)")
    print("12. Role-playing (RPG)")
    print("13. Simulator")
    print("14. Sport")
    print("15. Strategy")
    print("16. Turn-based strategy (TBS)")
    print("24. Tactical")
    print("25. Hack and slash/Beat \'em up")
    print("26. Quiz/Trivia")
    print("30. Pinball")
    print("31. Adventure")
    print("32. Indie")
    print("33. Arcade")
    print("34. Visual Novel")
    print("35. Card & Board Game")
    print("36. MOBA")
    # any others needed?
    print()

def print_themes():
    #Spun off into its own function so we don't have to worry about maintaining multiple versions of data in-code
    #Just grab it from here when needed
    print("Here are all the themes that there are!")
    print("1. Action")
    print("17. Fantasy")
    print("18. Science fiction")
    print("19. Horror")
    print("20. Thriller")
    print("21. Survival")
    print("22. Historical")
    print("23. Stealth")
    print("27. Comedy")
    print("28. Business")
    print("31. Drama")
    print("32. Non-fiction")
    print("33. Sandbox")
    print("34. Educational")
    print("35. Kids")
    print("38. Open world")
    print("39. Warfare")
    print("40. Party")
    print("41. 4X (explore, expand, exploit, and exterminate)")
    print("42. Erotic")
    print("43. Mystery")
    print("44. Romance")
    # any others needed?
    print()

def add_query(category, value):
    #new_query = {"List of Platforms": "Odyssey"}
    new_query = {category: value}
    global queries
    queries.append(new_query)
    #platform_queries.append(new_query)

def add_plat_query(category, value):
    #Including adding to queries in general in this function, because we will always want to do that?
    new_query = {category: value}
    global queries
    queries.append(new_query)
    global platform_queries
    platform_queries.append(new_query)

def add_playcount_query(category, value):
    new_query = {category: value}
    global queries
    queries.append(new_query)
    global player_count_queries
    player_count_queries.append(new_query)

def add_dev_query(category, value):
    new_query = {category: value}
    global queries
    queries.append(new_query)
    global dev_queries
    dev_queries.append(new_query)

#make more queries options for other types of queries? see if these will support?

#or queries: platform, player count, dev
#and queries: Misc, the rest

def add_misc_query(category, value):
    #This is meant for all the misc queries that would be ANDed in a natural approach
    new_query = {category: value}
    global queries
    queries.append(new_query)
    global misc_queries
    misc_queries.append(new_query)

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

#Prep for mongo connection
mon_connect = os.getenv('MONGO_URI')
# print(mon_connect)
mon_connected = False
mon_client = None
mon_db = None
mon_col = None
list_col = None

while True:
#Ask the user if they want to connect to the Mongo cluster yet, or wait until later
#If later, make sure there is a mechanism to ensure connection later on
    print("Would you like to check to make sure you can connect to the Mongo cluster now? Or later?")
    print("1. Now")
    print("2. Later")
    monconnect_option = input()

    if(monconnect_option == '1'):
        # Start connecting to Mongo cluster
        print("Alright! Let's try out the connection")
        mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
        # mon_client = pymongo.MongoClient(mon_connect)
        mon_db = mon_client["GameSorting"]
        try:
            mon_client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        mon_col = mon_db["games"]
        list_col = mon_db["lists"]
        mon_connected = True
        break
    elif (monconnect_option == '2'):
        print("Ok, just keep in mind you won't know if you can successfully connect to the cluster until you generate the report")
        break
    else:
        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.\n")
        print()
        continue

#test_query = {"Main Platform": "Wii"}
#test_query = {"Main Platform": {"$exists": True}}
#test_query = {"Ranked Score": { "$gt": 2400 } }

#print("Time to grab the games!")
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

#input("Brief pause\n")

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
#consider filter for age range? to allow for best adult games?
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
    print("11. Gameplay Genre")
    print("12. Thematic Genre")
    print("13. Miscellaneous")
    print("14. Finish and Generate Report")
    #consider franchise option when that data is pulled? genre? country developed in? other fields?
    #store queries to pull for franchises somewhere else if have to do custom?
    #genres are gameplay genres, themes are thematic genres

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
                print_platforms() #Used to have all the info listed here
                print("Which platform would you like to include?")
                #have function to check if number just given was one of the valid options?
                #going to go off of IGDB ID's for now, need to keep adding more
                platform_selection = input()
                add_plat_query("List of Platforms", platform_selection)
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
                            add_plat_query("List of Platforms", "PlayStation")
                            add_plat_query("List of Platforms", "PlayStation 2")
                            add_plat_query("List of Platforms", "PlayStation 3")
                            add_plat_query("List of Platforms", "PlayStation 4")
                            add_plat_query("List of Platforms", "PlayStation 5")
                            add_plat_query("List of Platforms", "PlayStation Portable")
                            add_plat_query("List of Platforms", "PlayStation Vita")
                            add_plat_query("List of Platforms", "PlayStation VR")
                            add_plat_query("List of Platforms", "PlayStation VR2")
                            add_plat_query("List of Platforms", "PocketStation")
                        elif (brand_option == 2):
                            #xbox family
                            add_plat_query("List of Platforms", "Xbox")
                            add_plat_query("List of Platforms", "Xbox 360")
                            add_plat_query("List of Platforms", "Xbox One")
                            add_plat_query("List of Platforms", "Xbox Series X|S")
                        elif (brand_option == 3):
                            #sega family
                            add_plat_query("List of Platforms", "SG-1000")
                            add_plat_query("List of Platforms", "Sega Master System/Mark III")
                            add_plat_query("List of Platforms", "Sega Mega Drive/Genesis")
                            add_plat_query("List of Platforms", "Sega CD")
                            add_plat_query("List of Platforms", "Sega 32X")
                            add_plat_query("List of Platforms", "Sega Saturn")
                            add_plat_query("List of Platforms", "Dreamcast")
                            add_plat_query("List of Platforms", "Visual Memory Unit / Visual Memory System")
                            add_plat_query("List of Platforms", "Sega Game Gear")
                            add_plat_query("List of Platforms", "Sega Pico")
                        elif (brand_option == 4):
                            #linux family
                            add_plat_query("List of Platforms", "Linux")
                            add_plat_query("List of Platforms", "Android")
                            add_plat_query("List of Platforms", "Google Stadia")
                            add_plat_query("List of Platforms", "Ouya") #(!)
                        elif (brand_option == 5):
                            #nintendo family
                            #any others missing? wiiware (removed?)? nintendo eshop (removed?)?
                            add_plat_query("List of Platforms", "Nintendo Entertainment System")
                            add_plat_query("List of Platforms", "Super Nintendo Entertainment System")
                            add_plat_query("List of Platforms", "Nintendo 64")
                            add_plat_query("List of Platforms", "Nintendo 64DD")
                            add_plat_query("List of Platforms", "Nintendo GameCube")
                            add_plat_query("List of Platforms", "Wii")
                            add_plat_query("List of Platforms", "Wii U")
                            add_plat_query("List of Platforms", "Nintendo Switch")
                            add_plat_query("List of Platforms", "Game Boy")
                            add_plat_query("List of Platforms", "Game Boy Color")
                            add_plat_query("List of Platforms", "Virtual Boy")
                            add_plat_query("List of Platforms", "Game Boy Advance")
                            add_plat_query("List of Platforms", "Nintendo DS")
                            add_plat_query("List of Platforms", "Nintendo DSi")
                            add_plat_query("List of Platforms", "Nintendo 3DS")
                            add_plat_query("List of Platforms", "New Nintendo 3DS")
                            add_plat_query("List of Platforms", "Family Computer")
                            add_plat_query("List of Platforms", "Family Computer Disk System")
                            add_plat_query("List of Platforms", "Super Famicom")
                            add_plat_query("List of Platforms", "Pokémon mini")
                            add_plat_query("List of Platforms", "Virtual Console")
                            add_plat_query("List of Platforms", "Nintendo PlayStation")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (brand_option == 6):
                        #we arrange this one ourselves for atari options
                        #consider making my own atari family in a platform family category in the mongo cluster?
                        print("LONER ATARI")
                        add_plat_query("List of Platforms", "Atari 2600")
                        add_plat_query("List of Platforms", "Atari 7800")
                        add_plat_query("List of Platforms", "Atari Lynx")
                        add_plat_query("List of Platforms", "Atari Jaguar")
                        add_plat_query("List of Platforms", "Atari ST/STE")
                        add_plat_query("List of Platforms", "Atari 8-bit")
                        add_plat_query("List of Platforms", "Atari 5200")
                        add_plat_query("List of Platforms", "Atari Jaguar CD")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.\n")
                        print()
                        continue
                break
            elif (platforms_option == '3'):
                while True:
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
                    #Home Pong series (unfound?)
                    #TV Tennis Electrotennis (unfound?)
                    #Coleco Telstar (unfound?)
                    #Color TV-Game (unfound?)

                    # Generation 3:
                    #Atari XEGS (unfound?)

                    # Generation 4:
                    #Nintendo PlayStation (cancelled)

                    #Generation 5:
                    #FM Towns Marty (unfound?)

                    #Generation 6:
                    #Panasonic M2 (cancelled)

                    #Generation 8:
                    #Panasonic Jungle (cancelled)

                    #Handhelds with no results:
                    #TurboExpress / PC Engine GT
                    #Watara Supervision
                    #...?

                    if(generation_option == "1"):
                        # Generation 1:
                        add_plat_query("List of Platforms", "Odyssey")
                        add_plat_query("List of Platforms", "PC-50X Family")
                        print("Generation 1 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif(generation_option == "2"):
                        # Generation 2:
                        add_plat_query("List of Platforms", "Atari 2600")
                        add_plat_query("List of Platforms", "Atari 5200")
                        add_plat_query("List of Platforms", "Intellivision")
                        add_plat_query("List of Platforms", "ColecoVision")
                        add_plat_query("List of Platforms", "Odyssey 2 / Videopac G7000")
                        add_plat_query("List of Platforms", "Game & Watch")
                        add_plat_query("List of Platforms", "Fairchild Channel F")
                        add_plat_query("List of Platforms", "Vectrex")
                        add_plat_query("List of Platforms", "Epoch Cassette Vision")
                        add_plat_query("List of Platforms", "1292 Advanced Programmable Video System")
                        add_plat_query("List of Platforms", "VC 4000")
                        add_plat_query("List of Platforms", "Bally Astrocade")
                        add_plat_query("List of Platforms", "Microvision")
                        print("Generation 2 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "3"):
                        # Generation 3:
                        add_plat_query("List of Platforms", "Nintendo Entertainment System")
                        add_plat_query("List of Platforms", "Family Computer")
                        add_plat_query("List of Platforms", "Family Computer Disk System")
                        add_plat_query("List of Platforms", "Sega Master System/Mark III")
                        add_plat_query("List of Platforms", "SG-1000")
                        add_plat_query("List of Platforms", "Atari 7800")
                        add_plat_query("List of Platforms", "Epoch Super Cassette Vision")
                        print("Generation 3 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "4"):
                        # Generation 4:
                        add_plat_query("List of Platforms", "Super Nintendo Entertainment System")
                        add_plat_query("List of Platforms", "Super Famicom")
                        add_plat_query("List of Platforms", "Satellaview")
                        add_plat_query("List of Platforms", "Game Boy")
                        add_plat_query("List of Platforms", "Sega Mega Drive/Genesis")
                        add_plat_query("List of Platforms", "Sega CD")
                        add_plat_query("List of Platforms", "Sega 32X")
                        add_plat_query("List of Platforms", "Sega Game Gear")
                        add_plat_query("List of Platforms", "Sega Pico")
                        add_plat_query("List of Platforms", "TurboGrafx-16/PC Engine")
                        add_plat_query("List of Platforms", "TurboGrafx-16/PC Engine CD")
                        add_plat_query("List of Platforms", "PC Engine SuperGrafx")
                        add_plat_query("List of Platforms", "Neo Geo AES")
                        add_plat_query("List of Platforms", "Neo Geo CD")
                        add_plat_query("List of Platforms", "Atari Lynx")
                        add_plat_query("List of Platforms", "Philips CD-i")
                        add_plat_query("List of Platforms", "Gamate")
                        print("Generation 4 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "5"):
                        # Generation 5:
                        add_plat_query("List of Platforms", "Nintendo 64")
                        add_plat_query("List of Platforms", "Nintendo 64DD")
                        add_plat_query("List of Platforms", "Game Boy Color")
                        add_plat_query("List of Platforms", "Virtual Boy")
                        add_plat_query("List of Platforms", "Sega Saturn")
                        add_plat_query("List of Platforms", "PlayStation")
                        add_plat_query("List of Platforms", "PocketStation")
                        add_plat_query("List of Platforms", "PC-FX")
                        add_plat_query("List of Platforms", "Neo Geo Pocket")
                        add_plat_query("List of Platforms", "Neo Geo Pocket Color")
                        add_plat_query("List of Platforms", "Atari Jaguar")
                        add_plat_query("List of Platforms", "Atari Jaguar CD")
                        add_plat_query("List of Platforms", "3DO Interactive Multiplayer")
                        add_plat_query("List of Platforms", "Amiga CD32")
                        add_plat_query("List of Platforms", "WonderSwan")
                        add_plat_query("List of Platforms", "WonderSwan Color")
                        add_plat_query("List of Platforms", "Apple Pippin")
                        add_plat_query("List of Platforms", "Playdia")
                        print("Generation 5 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "6"):
                        # Generation 6:
                        add_plat_query("List of Platforms", "Nintendo GameCube")
                        add_plat_query("List of Platforms", "Game Boy Advance")
                        add_plat_query("List of Platforms", "Dreamcast")
                        add_plat_query("List of Platforms", "Visual Memory Unit / Visual Memory System")
                        add_plat_query("List of Platforms", "PlayStation 2")
                        add_plat_query("List of Platforms", "Xbox")
                        add_plat_query("List of Platforms", "N-Gage")
                        add_plat_query("List of Platforms", "Leapster")
                        add_plat_query("List of Platforms", "V.Smile")
                        print("Generation 6 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "7"):
                        # Generation 7:
                        add_plat_query("List of Platforms", "Wii")
                        add_plat_query("List of Platforms", "Nintendo DS")
                        add_plat_query("List of Platforms", "Nintendo DSi")
                        add_plat_query("List of Platforms", "PlayStation 3")
                        add_plat_query("List of Platforms", "PlayStation Portable")
                        add_plat_query("List of Platforms", "Xbox 360")
                        add_plat_query("List of Platforms", "Zeebo")
                        add_plat_query("List of Platforms", "HyperScan")
                        add_plat_query("List of Platforms", "Leapster Explorer/LeadPad Explorer")
                        add_plat_query("List of Platforms", "Digiblast")
                        add_plat_query("List of Platforms", "Gizmondo")
                        print("Generation 7 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "8"):
                        # Generation 8:
                        add_plat_query("List of Platforms", "Wii U")
                        add_plat_query("List of Platforms", "Nintendo Switch")
                        add_plat_query("List of Platforms", "Nintendo 3DS")
                        add_plat_query("List of Platforms", "New Nintendo 3DS")
                        add_plat_query("List of Platforms", "PlayStation 4")
                        add_plat_query("List of Platforms", "PlayStation Vita")
                        add_plat_query("List of Platforms", "PlayStation VR")
                        add_plat_query("List of Platforms", "Xbox One")
                        add_plat_query("List of Platforms", "Ouya")
                        add_plat_query("List of Platforms", "Evercade")
                        add_plat_query("List of Platforms", "LeapTV")
                        print("Generation 8 consoles added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (generation_option == "9"):
                        #Generation 9:
                        add_plat_query("List of Platforms", "PlayStation 5")
                        add_plat_query("List of Platforms", "PlayStation VR2")
                        add_plat_query("List of Platforms", "Xbox Series X|S")
                        add_plat_query("List of Platforms", "Meta Quest 3")
                        add_plat_query("List of Platforms", "Playdate")
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
                        print("Grabbing console platforms")
                        print()
                        add_plat_query("List of Platforms", "Atari 2600")
                        add_plat_query("List of Platforms", "Atari 5200")
                        add_plat_query("List of Platforms", "Atari 7800")
                        add_plat_query("List of Platforms", "Atari Jaguar")
                        add_plat_query("List of Platforms", "Atari Jaguar CD")
                        add_plat_query("List of Platforms", "Nintendo Entertainment System")
                        add_plat_query("List of Platforms", "Family Computer")
                        add_plat_query("List of Platforms", "Family Computer Disk System")
                        add_plat_query("List of Platforms", "Super Nintendo Entertainment System")
                        add_plat_query("List of Platforms", "Super Famicom")
                        add_plat_query("List of Platforms", "Nintendo 64")
                        add_plat_query("List of Platforms", "Nintendo 64DD")
                        add_plat_query("List of Platforms", "Nintendo GameCube")
                        add_plat_query("List of Platforms", "Wii")
                        add_plat_query("List of Platforms", "Wii U")
                        add_plat_query("List of Platforms", "Nintendo Switch")
                        add_plat_query("List of Platforms", "Nintendo PlayStation")
                        add_plat_query("List of Platforms", "SG-1000")
                        add_plat_query("List of Platforms", "Sega Master System/Mark III")
                        add_plat_query("List of Platforms", "Sega Mega Drive/Genesis")
                        add_plat_query("List of Platforms", "Sega CD")
                        add_plat_query("List of Platforms", "Sega 32X")
                        add_plat_query("List of Platforms", "Sega Saturn")
                        add_plat_query("List of Platforms", "Dreamcast")
                        add_plat_query("List of Platforms", "Sega Pico")
                        add_plat_query("List of Platforms", "PlayStation")
                        add_plat_query("List of Platforms", "PlayStation 2")
                        add_plat_query("List of Platforms", "PlayStation 3")
                        add_plat_query("List of Platforms", "PlayStation 4")
                        add_plat_query("List of Platforms", "PlayStation 5")
                        add_plat_query("List of Platforms", "Xbox")
                        add_plat_query("List of Platforms", "Xbox 360")
                        add_plat_query("List of Platforms", "Xbox One")
                        add_plat_query("List of Platforms", "Xbox Series X|S")
                        add_plat_query("List of Platforms", "TurboGrafx-16/PC Engine")
                        add_plat_query("List of Platforms", "Turbografx-16/PC Engine CD")
                        add_plat_query("List of Platforms", "PC Engine SuperGrafx")
                        add_plat_query("List of Platforms", "PC-FX")
                        add_plat_query("List of Platforms", "Neo Geo AES")
                        add_plat_query("List of Platforms", "Neo Geo CD")
                        add_plat_query("List of Platforms", "Intellivision")
                        add_plat_query("List of Platforms", "Intellivision Amico") # (unreleased?)
                        add_plat_query("List of Platforms", "ColecoVision")
                        add_plat_query("List of Platforms", "3DO Interactive Multiplayer")
                        add_plat_query("List of Platforms", "Philips CD-i")
                        add_plat_query("List of Platforms", "Vectrex")
                        add_plat_query("List of Platforms", "Odyssey")
                        add_plat_query("List of Platforms", "Odyssey 2 / Videopac G7000")
                        add_plat_query("List of Platforms", "Amiga CD32")
                        add_plat_query("List of Platforms", "Ouya")
                        add_plat_query("List of Platforms", "Fairchild Channel F")
                        add_plat_query("List of Platforms", "Bally Astrocade")
                        add_plat_query("List of Platforms", "VC 4000")
                        add_plat_query("List of Platforms", "1292 Advanced Programmable Video System")
                        add_plat_query("List of Platforms", "PC-50X Family")
                        add_plat_query("List of Platforms", "Zeebo")
                        add_plat_query("List of Platforms", "Playdia")
                        add_plat_query("List of Platforms", "Epoch Cassette Vision")
                        add_plat_query("List of Platforms", "Epoch Super Cassette Vision")
                        add_plat_query("List of Platforms", "HyperScan")
                        add_plat_query("List of Platforms", "LeapTV")
                        add_plat_query("List of Platforms", "V.Smile")
                        add_plat_query("List of Platforms", "Apple Pippin")
                        add_plat_query("List of Platforms", "Nuon")
                        add_plat_query("List of Platforms", "Casio Loopy")
                        add_plat_query("List of Platforms", "AY-3-8760")
                        add_plat_query("List of Platforms", "AY-3-8710")
                        add_plat_query("List of Platforms", "AY-3-8603")
                        add_plat_query("List of Platforms", "AY-3-8605")
                        add_plat_query("List of Platforms", "AY-3-8606")
                        add_plat_query("List of Platforms", "AY-3-8607")
                        add_plat_query("List of Platforms", "DVD Player") # (does this seem fitting?)
                        add_plat_query("List of Platforms", "Panasonic M2") # (cancelled)
                        print("Console platforms added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "2"):
                        #Handheld
                        print()
                        print("Grabbing handheld platforms")
                        print()
                        add_plat_query("List of Platforms", "Game & Watch")
                        add_plat_query("List of Platforms", "Game Boy")
                        add_plat_query("List of Platforms", "Game Boy Color")
                        add_plat_query("List of Platforms", "Virtual Boy")
                        add_plat_query("List of Platforms", "Game Boy Advance")
                        add_plat_query("List of Platforms", "Nintendo DS")
                        add_plat_query("List of Platforms", "Nintendo DSi")
                        add_plat_query("List of Platforms", "Nintendo 3DS")
                        add_plat_query("List of Platforms", "New Nintendo 3DS")
                        add_plat_query("List of Platforms", "Nintendo Switch")
                        add_plat_query("List of Platforms", "Pokémon mini")
                        add_plat_query("List of Platforms", "Sega Game Gear")
                        add_plat_query("List of Platforms", "Visual Memory Unit / Visual Memory System")
                        add_plat_query("List of Platforms", "PocketStation")
                        add_plat_query("List of Platforms", "PlayStation Portable")
                        add_plat_query("List of Platforms", "PlayStation Vita")
                        add_plat_query("List of Platforms", "Atari Lynx")
                        add_plat_query("List of Platforms", "Neo Geo Pocket")
                        add_plat_query("List of Platforms", "Neo Geo Pocket Color")
                        add_plat_query("List of Platforms", "WonderSwan")
                        add_plat_query("List of Platforms", "WonderSwan Color")
                        add_plat_query("List of Platforms", "SwanCrystal")
                        add_plat_query("List of Platforms", "Leapster")
                        add_plat_query("List of Platforms", "Leapster Explorer/LeadPad Explorer")
                        add_plat_query("List of Platforms", "N-Gage")
                        add_plat_query("List of Platforms", "Game.com")
                        add_plat_query("List of Platforms", "Microvision")
                        add_plat_query("List of Platforms", "Tapwave Zodiac")
                        add_plat_query("List of Platforms", "Evercade")
                        add_plat_query("List of Platforms", "Gamate")
                        add_plat_query("List of Platforms", "Playdate")
                        add_plat_query("List of Platforms", "Digiblast")
                        add_plat_query("List of Platforms", "Gizmondo")
                        add_plat_query("List of Platforms", "Handheld Electronic LCD")
                        add_plat_query("List of Platforms", "Panasonic Jungle")
                        print("Handheld platforms added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "3"):
                        #Computer / Desktop OS
                        print()
                        print("Grabbing computer and desktop OS platforms")
                        print()
                        add_plat_query("List of Platforms", "DOS")
                        add_plat_query("List of Platforms", "PC (Microsoft Windows)")
                        add_plat_query("List of Platforms", "MSX")
                        add_plat_query("List of Platforms", "MSX2")
                        add_plat_query("List of Platforms", "Apple II")
                        add_plat_query("List of Platforms", "Apple IIGS")
                        add_plat_query("List of Platforms", "Mac")
                        add_plat_query("List of Platforms", "Linux")
                        add_plat_query("List of Platforms", "SteamOS")
                        add_plat_query("List of Platforms", "Commodore C64/128/MAX")
                        add_plat_query("List of Platforms", "Commodore VIC-20")
                        add_plat_query("List of Platforms", "Commodore 16")
                        add_plat_query("List of Platforms", "Commodore CDTV") # (seems a bit like a console?)
                        add_plat_query("List of Platforms", "Amiga")
                        add_plat_query("List of Platforms", "Commodore PET")
                        add_plat_query("List of Platforms", "Commodore Plus/4")
                        add_plat_query("List of Platforms", "Atari ST/STE")
                        add_plat_query("List of Platforms", "Atari 8-bit")
                        add_plat_query("List of Platforms", "PC-9800 Series")
                        add_plat_query("List of Platforms", "PC-8800 Series")
                        add_plat_query("List of Platforms", "NEC PC-6000 Series")
                        add_plat_query("List of Platforms", "FM Towns")
                        add_plat_query("List of Platforms", "FM-7")
                        add_plat_query("List of Platforms", "Sharp X1")
                        add_plat_query("List of Platforms", "Sharp X68000")
                        add_plat_query("List of Platforms", "Sharp MZ-2200")
                        add_plat_query("List of Platforms", "ZX Spectrum")
                        add_plat_query("List of Platforms", "Amstrad CPC")
                        add_plat_query("List of Platforms", "Amstrad PCW")
                        add_plat_query("List of Platforms", "BBC Microcomputer System")
                        add_plat_query("List of Platforms", "Texas Instruments TI-99")
                        add_plat_query("List of Platforms", "Donner Model 30")
                        add_plat_query("List of Platforms", "PDP-1")
                        add_plat_query("List of Platforms", "PDP-10")
                        add_plat_query("List of Platforms", "PDP-8")
                        add_plat_query("List of Platforms", "PDP-7")
                        add_plat_query("List of Platforms", "PDP-11")
                        add_plat_query("List of Platforms", "DEC GT40")
                        add_plat_query("List of Platforms", "Ferranti Nimrod Computer")
                        add_plat_query("List of Platforms", "EDSAC")
                        add_plat_query("List of Platforms", "HP 2100")
                        add_plat_query("List of Platforms", "HP 3000")
                        add_plat_query("List of Platforms", "SDS Sigma 7")
                        add_plat_query("List of Platforms", "Call-A-Computer time-shared mainframe computer system")
                        add_plat_query("List of Platforms", "CDC Cyber 70")
                        add_plat_query("List of Platforms", "PLATO")
                        add_plat_query("List of Platforms", "Imlac PDS-1")
                        add_plat_query("List of Platforms", "Microcomputer")
                        add_plat_query("List of Platforms", "Acorn Archimedes")
                        add_plat_query("List of Platforms", "Acorn Electron")
                        add_plat_query("List of Platforms", "TRS-80")
                        add_plat_query("List of Platforms", "TRS-80 Color Computer")
                        add_plat_query("List of Platforms", "AY-3-8500") # (seems more like console to me?)
                        add_plat_query("List of Platforms", "AY-3-8610") # (seems more like console to me?)
                        add_plat_query("List of Platforms", "Dragon 32/64")
                        add_plat_query("List of Platforms", "Tatung Einstein")
                        add_plat_query("List of Platforms", "Thomson MO5")
                        print("Computer / Desktop OS platforms added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "4"):
                        #Arcade
                        print()
                        print("Grabbing arcade platforms")
                        print()
                        add_plat_query("List of Platforms", "Arcade")
                        add_plat_query("List of Platforms", "Neo Geo MVS")
                        add_plat_query("List of Platforms", "Hyper Neo Geo 64")
                        add_plat_query("List of Platforms", "Analogue electronics") # (?, should be misc maybe?)
                        print("Arcade platforms added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "5"):
                        #Mobile Phone
                        print()
                        print("Grabbing mobile phone platforms")
                        print()
                        add_plat_query("List of Platforms", "iOS")
                        add_plat_query("List of Platforms", "Android")
                        add_plat_query("List of Platforms", "BlackBerry OS")
                        add_plat_query("List of Platforms", "Windows Mobile")
                        add_plat_query("List of Platforms", "Windows Phone")
                        add_plat_query("List of Platforms", "Palm OS")
                        add_plat_query("List of Platforms", "Legacy Mobile Device")
                        print("Mobile phone platforms added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "6"):
                        #Virtual Reality
                        print()
                        print("Grabbing VR platforms")
                        print()
                        add_plat_query("List of Platforms", "PlayStation VR")
                        add_plat_query("List of Platforms", "PlayStation VR2")
                        add_plat_query("List of Platforms", "Windows Mixed Reality")
                        add_plat_query("List of Platforms", "Oculus Rift")
                        add_plat_query("List of Platforms", "Oculus VR")
                        add_plat_query("List of Platforms", "Oculus Quest")
                        add_plat_query("List of Platforms", "Meta Quest 2")
                        add_plat_query("List of Platforms", "Meta Quest 3")
                        add_plat_query("List of Platforms", "SteamVR")
                        add_plat_query("List of Platforms", "Daydream")
                        print("VR platforms added to querying!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (platform_format == "7"):
                        #Platform
                        print()
                        print("Grabbing platform-style platforms")
                        print()
                        add_plat_query("List of Platforms", "Web browser")
                        add_plat_query("List of Platforms", "Satellaview") # (?)
                        add_plat_query("List of Platforms", "Virtual Console") # (?)
                        #add_plat_query("List of Platforms", "WiiWare") # (?, removed?)
                        #add_plat_query("List of Platforms", "Nintendo eShop") #  (?, removed?)
                        add_plat_query("List of Platforms", "PlayStation Network") #  (?)
                        add_plat_query("List of Platforms", "Xbox Live Arcade") #  (?)
                        add_plat_query("List of Platforms", "Google Stadia") # (?)
                        add_plat_query("List of Platforms", "Amazon Fire TV")
                        add_plat_query("List of Platforms", "OnLive Game System")
                        add_plat_query("List of Platforms", "OOParts")
                        add_plat_query("List of Platforms", "Plug & Play") #  (seems more like console)
                        print("Platform-style platforms added to querying!")
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
                #print()
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
        print_platforms()
        print("Which platform would you like to include?")
        # have function to check if number or text just given was one of the valid options? reject if invalid, loop it
        # going to go off of IGDB ID's for now, need to keep adding more
        platform_selection = input()
        add_plat_query("Main Platform", platform_selection)
        print("Returning back to main menu")
        print()
    elif (filter_category == '3'):
        print()
        print("You have selected 3. Release Date")
        print()
        while True:
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
                """
                new_query = {"Release Date": filter_date}
                queries.append(new_query)
                """
                add_misc_query("Release Date", filter_date)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif (time_style_option == '2'):
                while True:
                    print("Here are the time range options to choose from")
                    print("1. Specific year")
                    print("2. Specific decade")
                    print("3. Before a date")
                    print("4. After a date")
                    print("5. In between two dates")
                    print("6. 20th Century")
                    print("7. 21st Century")
                    time_range_option = input()
                    if (time_range_option == '1'):
                        #fix these and others to use datetime?
                        #give prompts to return to main menu
                        print("You have selected 1. Specific year")
                        print()
                        print("Please enter the year you would like to query for")
                        year_input = input()
                        #{ "address": { "$gt": "S" } }
                        value = { "$gte": f"{year_input}-01-01", "$lt": f"{str(int(year_input)+1)}-01-01" }
                        add_misc_query("Release Date", value)
                        #check to make sure this works?
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (time_range_option == '2'):
                        print("You have selected 2. Specific decade")
                        print()
                        print("Please enter the decade you would like to query for (ex. 199)")
                        decade_input = input()
                        value = {"$gte": f"{decade_input}0-01-01", "$lt": f"{str(int(decade_input) + 1)}0-01-01"}
                        add_misc_query("Release Date", value)
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (time_range_option == '3'):
                        print("You have selected 3. Before a date")
                        print()
                        print("Please select the date you would like to query for earlier than")
                        print("First type in the year, then the month, then the day")
                        date_year = int(input())
                        date_month = int(input())
                        date_day = int(input())
                        filter_date = datetime.datetime(date_year, date_month, date_day)
                        print(filter_date)
                        value = {"$lt": f"{filter_date}"}
                        add_misc_query("Release Date", value)
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (time_range_option == '4'):
                        print("You have selected 4. After a date")
                        print()
                        print("Please select the date you would like to query for later than")
                        print("First type in the year, then the month, then the day")
                        date_year = int(input())
                        date_month = int(input())
                        date_day = int(input())
                        filter_date = datetime.datetime(date_year, date_month, date_day+1) #+1 so can gte after the day
                        print(filter_date)
                        value = {"$gte": f"{filter_date}"}
                        add_misc_query("Release Date", value)
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (time_range_option == '5'):
                        print("You have selected 5. In between two dates")
                        print()
                        print("First, please select the date you would like to query for later than")
                        print("First type in the year, then the month, then the day")
                        date_year_1 = int(input())
                        date_month_1 = int(input())
                        date_day_1 = int(input())
                        filter_date_1 = datetime.datetime(date_year_1, date_month_1, date_day_1 + 1)  # +1 so can gte after the day
                        print(filter_date_1)
                        print("Now, please select the date you would like to query for earlier than")
                        print("First type in the year, then the month, then the day")
                        date_year_2 = int(input())
                        date_month_2 = int(input())
                        date_day_2 = int(input())
                        filter_date_2 = datetime.datetime(date_year_2, date_month_2, date_day_2)  # +1 so can gte after the day
                        print(filter_date_2)
                        value = {"$gte": f"{filter_date_1}", "$lt": f"{filter_date_2}"}
                        add_misc_query("Release Date", value)
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (time_range_option == '6'):
                        print("You have selected 6. 20th Century")
                        print()
                        value = {"$gte": datetime.datetime(1970, 1, 1), "$lt": datetime.datetime(2000, 1, 1)}
                        add_misc_query("Release Date", value)
                        print("20th century query added")
                        print()
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (time_range_option == '7'):
                        print("You have selected 7. 21st Century")
                        print()
                        value = {"$gte": datetime.datetime(2000, 1, 1), "$lt": datetime.datetime.now()}
                        add_misc_query("Release Date", value)
                        print("21st century query added")
                        print()
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.\n")
                        print()
                        continue
                break
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                print()
                continue
        print("Returning back to main menu")
        print()
    elif (filter_category == '4'):
        print()
        print("You have selected 4. Completion Status")
        print()
        while True:
            print("Would you like games you have completed? Or games you haven't completed?")
            print("1. Completed")
            print("2. Uncompleted")
            completed_option = input()
            if(completed_option == '1'):
                print("Including games you have completed")
                add_misc_query("Completed", True)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif(completed_option == '2'):
                print("Including games you have not completed")
                add_misc_query("Completed", False)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                print()
                continue
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
        #put in an add_misc_query here when figure out proper formatting?
        print("Returning back to main menu")
        print()
    elif (filter_category == '6'):
        print()
        print("You have selected 6. Ranked Score")
        print()
        while True:
            print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
            print("1. Minimum threshold score")
            print("2. Maximum threshold score")
            print("3. Target score")
            score_option = input()
            if (score_option == '1'):
                print("You have selected 1. Minimum threshold score")
                print()
                target_score = input("Set your target minimum score: ")
                value = {"$gte": int(target_score)}
                add_misc_query("Ranked Score", value)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif (score_option == '2'):
                print("You have selected 2. Maximum threshold score")
                print()
                target_score = input("Set your target maximum score: ")
                value = {"$lte": int(target_score)}
                add_misc_query("Ranked Score", value)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif (score_option == '3'):
                print("You have selected 3. Target score")
                print()
                target_score = input("Set your target score: ")
                """
                new_query = {"Ranked Score": target_score}
                queries.append(new_query)
                """
                add_misc_query("Ranked Score", target_score)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                print()
                continue
        print("Returning back to main menu")
        print()
    elif (filter_category == '7'):
        print()
        print("You have selected 7. Inclusion Score")
        print()
        while True:
            print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
            print("1. Minimum threshold score")
            print("2. Maximum threshold score")
            print("3. Target score")
            score_option = input()
            if (score_option == '1'):
                print("You have selected 1. Minimum threshold score")
                print()
                target_score = input("Set your target minimum score: ")
                value = {"$gte": int(target_score)}
                add_misc_query("Inclusion Score", value)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif (score_option == '2'):
                print("You have selected 2. Maximum threshold score")
                print()
                target_score = input("Set your target maximum score: ")
                value = {"$lte": int(target_score)}
                add_misc_query("Inclusion Score", value)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif (score_option == '3'):
                print("You have selected 3. Target score")
                print()
                target_score = input("Set your target score: ")
                """
                new_query = {"Inclusion Score": target_score}
                queries.append(new_query)
                """
                add_misc_query("Inclusion Score", target_score)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                print()
                continue
        print("Returning back to main menu")
        print()
    elif (filter_category == '8'):
        print()
        print("You have selected 8. Average Score")
        print()
        while True:
            print("Would you like to set a minimum threshold score? A maximum one? Or a target score value?")
            print("1. Minimum threshold score")
            print("2. Maximum threshold score")
            print("3. Target score")
            score_option = input()
            if (score_option == '1'):
                print("You have selected 1. Minimum threshold score")
                print()
                target_score = input("Set your target minimum score: ")
                value = {"$gte": int(target_score)}
                add_misc_query("Average Score", value)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif (score_option == '2'):
                print("You have selected 2. Maximum threshold score")
                print()
                target_score = input("Set your target maximum score: ")
                value = {"$lte": int(target_score)}
                add_misc_query("Average Score", value)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            elif (score_option == '3'):
                print("You have selected 3. Target score")
                print()
                target_score = input("Set your target score: ")
                """
                new_query = {"Average Score": target_score}
                queries.append(new_query)
                """
                add_misc_query("Average Score", target_score)
                print("Query added!")
                input("When you are ready, press Enter to go back to the main print menu\n")
                break
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                print()
                continue
        print("Returning back to main menu")
        print()
    elif (filter_category == '9'):
        print()
        print("You have selected 9. Player Count")
        print()
        while True:
            print("Would you like to select whether you want singleplayer or multiplayer?")
            print("Or select one-by-one which player counts you would like to include?")
            print("1. Singleplayer or Multiplayer")
            print("2. Pick player counts individually")
            player_type_option = input()
            if (player_type_option == '1'):
                print("You have selected 1. Singleplayer or Multiplayer")
                print()
                while True:
                    print("Which of the two would you like?")
                    print("1. Singleplayer")
                    print("2. Multiplayer")
                    sm_option = input()
                    if(sm_option == '1'):
                        add_playcount_query("Player Count", "Single player")
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif(sm_option == '2'):
                        add_playcount_query("Player Count", "Multiplayer")
                        add_playcount_query("Player Count", "Co-operative")
                        add_playcount_query("Player Count", "Split screen")
                        add_playcount_query("Player Count", "Massively Multiplayer Online (MMO)")
                        add_playcount_query("Player Count", "Battle Royale")
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                        print()
                        continue
                break
            elif(player_type_option == '2'):
                print("You have selected 2. Pick player counts individually")
                print()
                while True:
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
                        continue
                    """
                    new_query = {"Player Count": target_count}
                    queries.append(new_query)
                    player_count_queries.append(new_query)
                    """
                    add_playcount_query("Player Count", target_count)
                    print("Query added!")
                    input("When you are ready, press Enter to go back to the main print menu\n")
                    break
                break
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                print()
                continue
        print("Returning back to main menu")
        print()
    elif (filter_category == '10'):
        print()
        print("You have selected 10. Developers")
        print()
        while True:
            #print("Are you planning on selecting filters for developers or publishers right now?")
            print("For developers, are you looking for true Developers, Publishers, or just any company that worked on a game?")
            print("1. True Developers")
            print("2. Publishers")
            print("3. Any company that worked on a game")
            dev_company_option = input()
            if(dev_company_option == '1'):
                while True:
                    print("Would you like to try entering in a name for the developer you are looking for? Or trying by their IGDB ID?")
                    print("1. Search by name")
                    print("2. Search by ID [NOT IMPLEMENTED! MAY BECOME DEPRECATED!]")
                    dev_type_option = input()
                    if (dev_type_option == '1'):
                        print("Which developer are you wanting to filter for? For now you'll want to be pretty exact.")
                        dev_search = input()
                        add_dev_query("Developers", dev_search)
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (dev_type_option == '2'):
                        #print("Enter the ID of the developer you are looking for")
                        #dev_ID = input()
                        # would have to query IGDB API for this? unless started treating developers as tuples that contain IGDB as well
                        #add_dev_query("Developers", dev_search)  # wrong?
                        print("I was initially intending this feature, but I'm not sure anymore")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                        print()
                        continue
                break
            elif(dev_company_option == '2'):
                while True:
                    print("Would you like to try entering in a name for the publisher you are looking for? Or trying by their IGDB ID?")
                    print("1. Search by name")
                    print("2. Search by ID [NOT IMPLEMENTED! MAY BECOME DEPRECATED!]")
                    pub_type_option = input()
                    if (pub_type_option == '1'):
                        print("Which publisher are you wanting to filter for? For now you'll want to be pretty exact.")
                        dev_search = input()
                        add_dev_query("Publishers", dev_search)
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (pub_type_option == '2'):
                        print("I was initially intending this feature, but I'm not sure anymore")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                        print()
                        continue
                break
            elif (dev_company_option == '3'):
                while True:
                    print("Would you like to try entering in a name for the company you are looking for? Or trying by their IGDB ID?")
                    print("1. Search by name")
                    print("2. Search by ID [NOT IMPLEMENTED! MAY BECOME DEPRECATED!]")
                    comp_type_option = input()
                    if (comp_type_option == '1'):
                        print("Which company are you wanting to filter for? For now you'll want to be pretty exact.")
                        dev_search = input()
                        add_dev_query("Companies", dev_search)
                        print("Query added!")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    elif (comp_type_option == '2'):
                        print("I was initially intending this feature, but I'm not sure anymore")
                        input("When you are ready, press Enter to go back to the main print menu\n")
                        break
                    else:
                        print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                        print()
                        continue
                break
            else:
                print("I'm sorry, I don't understand that selection. You'll have to choose one of the valid options.")
                print()
                continue
            #going to be using involvedcompany and company?
        print("Returning back to main menu")
        print()
    elif (filter_category == '11'):
        #GENRE
        print()
        print("You have selected 11. Gameplay Genre")
        print()
        print("Now we are going to list all of the options of genres (gameplay) you can choose from")
        print("Note that the numbers are listed as so because they are the platform ID's listed in IGDB's API")
        input("Whenever you are ready, the platform options will be listed in full (For now use the text version)\n")
        print_platforms()  # Used to have all the info listed here
        print("Which platform would you like to include?")
        # have function to check if number just given was one of the valid options?
        # going to go off of IGDB ID's for now, need to keep adding more
        platform_selection = input()
        add_plat_query("List of Platforms", platform_selection)
        input("When you are ready, press Enter to go back to the main print menu\n")
        #...
    elif (filter_category == '12'):
        #THEME
        print()
        print("You have selected 12. Thematic Genre")
        print()
        #...
    elif (filter_category == '13'):
        print()
        print("You have selected 13. Miscellaneous")
        print()
        print("This is for miscellaneous filter options that don't fit easily anywhere else")
        print("As of now, we haven't really thought of anything, but that could change!")
        print()
        #Fill this if anything comes to mind that I'd like to filter for that doesn't fit in one of the other options
        print("Returning back to main menu")
        print()
    elif(filter_category == '14'):
        print()
        #answer_check_main = True
        #print all the queries used at the top of the file for posterity?
        if(len(queries) == 0):
            print("Hey, there's nothing here! We have to go back to have something to work with")
            input("When you are ready, press Enter to go back to the main print menu\n")
            continue
        else:
            print("Alright! Let's generate the report with the options selected!")
            custom_query = {}
            print(queries)
            #for query, value in queries.items():
            # Check if mongo connection was tested yet
            if (mon_connected == False):
                print("First we have to do a little test now to make sure we can connect to the cluster")
                print("Just hold a second while we verify this, press Enter when you are ready to test")
                mon_wait = input()
                mon_client = pymongo.MongoClient(mon_connect, server_api=ServerApi('1'))
                mon_db = mon_client["GameSorting"]
                try:
                    mon_client.admin.command('ping')
                    print("Pinged your deployment. You successfully connected to MongoDB!")
                except Exception as e:
                    print(e)
                mon_col = mon_db["games"]
                list_col = mon_db["lists"]
                mon_connected = True
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
                if (and_or_type != '1' or and_or_type != '2' or and_or_type != '3'):
                    print("Please try again with valid input")
                    continue
                else:
                    print(f"Your choice of {and_or_type} has been noted")
                    break
            while True:
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
                    elif (sort_type == '4'):
                        games_pulled = mon_col.find({'$and': queries}).sort("Title", 1)
                        #consider a sorting name field so we can disregard words like "the"? use regex?
                        break
                    elif (sort_type == '5'):
                        games_pulled = mon_col.find({'$and': queries}).sort("Release Date", 1)
                        break
                    elif (sort_type == '6'):
                        games_pulled = mon_col.find({'$and': queries}).sort("Release Date", -1)
                        break
                    else:
                        print("Sorry, I don't understand")
                        print()
                        continue
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
                    elif (sort_type == '4'):
                        games_pulled = mon_col.find({'$or': queries}).sort("Title", 1)
                        break
                    elif (sort_type == '5'):
                        games_pulled = mon_col.find({'$or': queries}).sort("Release Date", 1)
                        break
                    elif (sort_type == '6'):
                        games_pulled = mon_col.find({'$or': queries}).sort("Release Date", -1)
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
                    elif (sort_type == '4'):
                        games_pulled = mon_col.find(natural_queries).sort("Title", 1)
                        break
                    elif (sort_type == '5'):
                        games_pulled = mon_col.find(natural_queries).sort("Release Date", 1)
                        break
                    elif (sort_type == '6'):
                        games_pulled = mon_col.find(natural_queries).sort("Release Date", -1)
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
How to query for specific year among datetime: https://stackoverflow.com/questions/49174399/mongodb-find-query-by-year
"""