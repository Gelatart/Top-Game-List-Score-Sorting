using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using DefaultNamespace;

namespace GameListScoring
{
    public class MainFunction
    {
        static Dictionary<string, Game> GameIndex = new Dictionary<string, Game>();

        //Need the static?
        //Make a dictionary for the lists that have been logged?
        static Dictionary<string, bool> ListIndex = new Dictionary<string, bool>();
        //static Dictionary<int, Game> RankedGameIndex = new Dictionary<int, Game>();
        //static Dictionary<int, Game> InclusionGameIndex = new Dictionary<int, Game>();
        //Dictionary for AverageScoreIndex?

        //Need the static?
        public static void Main(string[] args)
        {
            // Display the number of command line arguments:
            //Source for how to read files in this way: https://stackoverflow.com/questions/5840443/how-to-read-all-files-inside-particular-folder
            string folderPath = @"C:\Users\Gamer\Documents\Top-Game-List-Score-Sorting\GameListScoring";
            foreach (string file in Directory.GetFiles(folderPath, "*.txt"))
            {
                string contents = File.ReadAllText(file);
                string line;
                string ListTag = Console.ReadLine(); //Have the list tag on the firstline
                string ListTitle = Console.ReadLine(); //Have the list title on the second line
                while ((line = Console.ReadLine()) != null)
                {
                    //Read each variable and put it in an array based on how lines formatted
                    string[] attributes = line.Split(';');
                    string BaseGame = attributes[0];
                    int Rank = Convert.ToInt32(attributes[1]);
                    string Title = attributes[2];
                    string CompletionStatus = attributes[3];
                    string Franchise = attributes[4];
                    string Subfranchise = attributes[5];
                    DateTime ReleaseDate = DateTime.Parse(attributes[6]);
                    string SpecialNotes = attributes[7];
                    //bool Discontinued = Convert.ToBoolean(attributes[8]);
                    Game temp = SearchDatabase(BaseGame);
                    /*if (ListTag != "standardRed" && ListTag != "standardBlue")
                    {
                        SpecialCases();
                    }*/

                    
                    if (temp.BaseGame == null)
                    {
                        Game Entry = new Game(BaseGame, Rank, Title, CompletionStatus, Franchise, Subfranchise, ReleaseDate, SpecialNotes); //instantiate with new values
                        //Entry.RankedScore += Rank; //Rank is already set by the extended game instantiation
                        GameIndex.Add(BaseGame, Entry); 
                    }
                    else
                    {
                        //found a match, replace entry in database when updated (if list logged == false, inclusionscore++, logged = true?)
                        //add to lists on
                        if (ListIndex[ListTitle] == false) //fix how it checks?
                        {
                            //inclusionscore goes up
                            temp.InclusionScore++;
                            temp.RankedScore += Rank;
                            temp.AverageScore = temp.RankedScore / temp.InclusionScore;
                        }

                        GameIndex[BaseGame] = temp; //should update Entry value, with the now increased rank score
                    }
                }
                ListIndex[ListTitle] = true;
            }
            //while reading all the entries in the database
            //compare ranked score to sort, then use alphabetical and release date for franchise
            //use the cases of completion status to inform formatting
            //print to row, move to the next entry (print score, titles in base game)

            //SortedDictionary<int, Game> RankedGameIndex = new SortedDictionary<int, Game>(GameIndex);
            SortedDictionary<int, Game> RankedGameIndex = new SortedDictionary<int, Game>();
                //Inspiration: https://docs.microsoft.com/en-us/dotnet/api/system.collections.generic.sorteddictionary-2.-ctor?view=netframework-4.8#System_Collections_Generic_SortedDictionary_2__ctor_System_Collections_Generic_IDictionary__0__1__
                //Need to properly convert GameIndex format? Need to specify the way keys will be ordered?

            foreach (KeyValuePair<string, Game> entry in GameIndex) {
                Game rankedItem = entry.Value;
                RankedGameIndex.Add(rankedItem.RankedScore, rankedItem);
            }
            //IOrderedEnumerable<KeyValuePair<int, Game>> query = RankedGameIndex.OrderBy(RankedGameIndex <= RankedGameIndex.Key);
            //Inspiration: https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable.orderby?view=netframework-4.8
            
            //while reading all the entries in the database
            //compare inclusion score to sort, then use alphabetical and release date for franchise
            //use the cases of completion status to inform formatting
            //print to row, move to the next entry (print score, titles in base game        
            foreach (var entry in RankedGameIndex.OrderBy(entry <= entry.RankedScore))
            {
                //if ranked score is the same, compare by alphabetical franchise, then subfranchise, then release date
            }
            /*for (int index = 0; index < GameIndex.Count; index++)  {
                int lastIndex;
                if (index == 0) {
                    lastIndex = 0
                } else {
                    lastIndex = index;
                    var lastItem = GameIndex.ElementAt(lastIndex);
                    var lastItemKey = lastItem.Key;
                    var lastItemValue = lastItem.Value;
                    var item = GameIndex.ElementAt(index);
                    var itemKey = item.Key;
                    var itemValue = item.Value;
                    if(lastItemValue.RankedScore == itemValue.RankedScore) {
                        if(lastItemValue.Franchise > itemValue.Franchise) {
                            GameIndex.ElementAt(index) = lastItem;
                            GameIndex.ElementAt(lastIndex) = item;
                        } else if (lastItemValue.Franchise == itemValue.Franchise) {
                            if(lastItemValue.Subfranchise > itemValue.Subfranchise) {
                                GameIndex.ElementAt(index) = lastItem;
                                GameIndex.ElementAt(lastIndex) = item;
                            } else if (lastItemValue.Subfranchise == itemValue.Subfranchise) {
                                if(lastItemValue.ReleaseDate > itemValue.ReleaseDate) {
                                    GameIndex.ElementAt(index) = lastItem;
                                    GameIndex.ElementAt(lastIndex) = item;
                                }
                            }
                        }
                    }                    
                } 
            }*/

            //Inspiration: https://www.dotnetperls.com/sort-dictionary
            //Inspiration: https://stackoverflow.com/questions/141088/what-is-the-best-way-to-iterate-over-a-dictionary
            printDatabase(RankedGameIndex, "RankedDatabase");

            //SortedDictionary<int, Game> InclusionGameIndex = new SortedDictionary<int, Game>(GameIndex);
            SortedDictionary<int, Game> InclusionGameIndex = new SortedDictionary<int, Game>();
            //Need to properly convert GameIndex format? Need to specify the way keys will be ordered?

            foreach (KeyValuePair<string, Game> entry in GameIndex) {
                Game inclusionItem = entry.Value;
                InclusionGameIndex.Add(inclusionItem.InclusionScore, inclusionItem);
            }
            
            //IOrderedEnumerable<KeyValuePair<int, Game>> query = InclusionGameIndex.OrderBy(InclusionGameIndex <= InclusionGameIndex.Key);
            
            foreach (var entry in InclusionGameIndex.OrderBy(entry <= entry.InclusionScore))
            {
                //do similar thing but with for inclusionscore
            }

            printDatabase(InclusionGameIndex, "InclusionDatabase");

            //AVERAGE GAME INDEX:

            SortedDictionary<int, Game> AverageGameIndex = new SortedDictionary<int, Game>();
            foreach (KeyValuePair<string, Game> entry in GameIndex)
            {
                Game averageItem = entry.Value;
                int aScore = (int)Math.Round(averageItem.AverageScore, 0);
                AverageGameIndex.Add(aScore, averageItem);
            }
            foreach (var entry in AverageGameIndex.OrderBy(entry <= entry.AverageScore))
            {
                //do similar thing but with for inclusionscore
            }
            printDatabase(AverageGameIndex, "AverageDatabase");
        }


        /*private static void SpecialCases()
        {
            //FILL OUT, FIGURE OUT WHAT TO DO HERE    
        }*/

        private static Game SearchDatabase(string checker)
        {
            Game temp = new Game();
            temp.BaseGame = null;
            //if found then return, otherwise return an empty game file with a null basegame
            foreach (KeyValuePair<string, Game> entry in GameIndex)
            {
                if (entry.Key == checker)
                {
                    temp = entry.Value;
                    break;
                }
            }

            return temp;
        }

        public static void printDatabase(SortedDictionary<int,Game> index, string fileName)
        {
            //iterate through entire database, printing it all to a text file
            List<string> linesList = new List<string>();
            foreach (KeyValuePair<int, Game> entry in index)
            {
                Game temp = entry.Value;
                //print out all the attributes into a string
                string BaseGame = temp.BaseGame;
                //string Title = entry.Title;
                //string CompletionStatus = entry.CompletionStatus;
                int RankedScore = temp.RankedScore;
                int InclusionScore = temp.InclusionScore;
                int AverageScore = (int)Math.Round(temp.AverageScore, 0);
                //string Franchise = entry.Franchise;
                //string Subfranchise = entry.Subfranchise;
                //string ReleaseDate = entry.ReleaseDate;
                string SpecialNotes = temp.SpecialNotes;
                //bool Discontinued = entry.Discontinued;
                //extract values from game entry
                string line = RankedScore + "," + InclusionScore + "," + AverageScore + "," + BaseGame + "," + SpecialNotes;
                //use completionstatus for formatting? Include all potential titles?
                //find a way to get these sorted by score, franchise, releasedate, etc.
                linesList.Add(line);
            }

            string[] lines = linesList.ToArray();
            string path = @"C:\Users\Gamer\Documents\Top-Game-List-Score-Sorting\" + fileName + ".txt";
            System.IO.File.WriteAllLines(path, lines);
            //create a text file they all go into? create another one for ranked by inclusionscore?
            //Took inspiration from https://stackoverflow.com/questions/202813/adding-values-to-a-c-sharp-array
            //as well as https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/file-system/how-to-write-to-a-text-file
        }
    }
}
