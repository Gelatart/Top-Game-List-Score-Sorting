using System.IO;

namespace DefaultNamespace
{
    public class Main
    {
        Dictionary<string, Game> GameIndex = new Dictionary<string, Game>();

        //Make a dictionary for the lists that have been logged?
        Dictionary<string, bool> ListIndex = new Dictionary<string, bool>();

        static void Main(string[] args)
        {
            // Display the number of command line arguments:
            //Source for how to read files in this way: https://stackoverflow.com/questions/5840443/how-to-read-all-files-inside-particular-folder
            foreach (string file in Directory.EnumerateFiles(folderPath, "*.txt"))
            {
                string contents = File.ReadAllText(file);
                string line;
                string ListTag; //figure out how to assign ListTag to list
                string ListTitle; //figure out how to get the filename
                while ((line = Console.ReadLine()) != null)
                {
                    //Read each variable and put it in an array based on how lines formatted
                    string[] attributes = line.Split(';');
                    string BaseGame = attributes[0];
                    int Rank = attributes[1];
                    string Title = attributes[2];
                    string CompletionStatus = attributes[3];
                    string Franchise = attributes[4];
                    string Subfranchise = attributes[5];
                    string ReleaseDate = attributes[6];
                    string SpecialNotes = attributes[7];
                    bool Discontinued = attributes[8];
                    Game temp = searchDatabase(BaseGame);
                    if (ListTag != "standardRed" && ListTag != "standardBlue")
                    {
                        SpecialCases();
                    }

                    Game Entry = Game(BaseGame, Rank, Title, CompletionStatus, Franchise, Subfranchise, ReleaseDate,
                        SpecialNotes, Discontinued); //instantiate with new values
                    Entry.RankedScore += Rank;
                    if (temp.BaseGame == null)
                    {
                        GameIndex.add(BaseGame, Entry); //do an if/else check to see if already in dictionary first
                    }
                    else
                    {
                        //found a match, replace entry in database when updated (if list logged == false, inclusionscore++, logged = true?)
                        //add to lists on
                        if (ListIndex[ListTitle] == false) //fix how it checks?
                        {
                            //inclusionscore goes up
                        }

                        GameIndex[BaseGame] = Entry; //should update Entry value, with the now increased rank score
                    }
                }
            }
            //while reading all the entries in the database
            //compare ranked score to sort, then use alphabetical and release date for franchise
            //use the cases of completion status to inform formatting
            //print to row, move to the next entry (print score, titles in base game)

            //while reading all the entries in the database
            //compare inclusion score to sort, then use alphabetical and release date for franchise
            //use the cases of completion status to inform formatting
            //print to row, move to the next entry (print score, titles in base game)
        }
        foreach(var entry in GameIndex.OrderBy(i <= i.RankedScore))
        { 
            
            //if ranked score is the same, compare by alphabetical franchise, then subfranchise, then release date
        }
        //Could try the reorderdictionary function, similar to stackoverflow?
        //Could  put into a list?
        //Could use comparative functions?
        //Find way to iterate through whole dictionary?

        //Inspiration: https://www.dotnetperls.com/sort-dictionary
        printRankedDatabase();
            foreach(var entry in GameIndex.OrderBy(i <= i.InclusionScore))
        {
            //do similar thing but with for inclusionscore
        }
        printInclusionDatabase();
    }

    public void SpecialCases()
    {
    //FILL OUT, FIGURE OUT WHAT TO DO HERE    
    }
    public Game searchDatabase(string checker) {
    Game temp;
    temp.BaseGame = null;
    //if found then return, otherwise return an empty game file with a null basegame
    foreach(KeyValuePair<string, Game> entry in GameIndex)
    {
        if (entry.Key == checker)
        {
            temp = entry.Value;
            break;
        }
    }
    return temp;
    }
    public void printRankedDatabase() {
    //iterate through entire database, printing it all to a text file
    List<string> linesList = new List<string>();
        foreach(KeyValuePair<string, Game> entry in GameIndex) {
        //print out all the attributes into a string
        string BaseGame = entry.BaseGame;
        //string Title = entry.Title;
        //string CompletionStatus = entry.CompletionStatus;
        int RankedScore = entry.RankedScore;
        int InclusionScore = entry.InclusionScore;
        //string Franchise = entry.Franchise;
        //string Subfranchise = entry.Subfranchise;
        //string ReleaseDate = entry.ReleaseDate;
        string SpecialNotes = entry.SpecialNotes;
        //bool Discontinued = entry.Discontinued;
        //extract values from game entry
        string line = RankedScore + "," + InclusionScore + "," + BaseGame + "," + SpecialNotes;
        //use completionstatus for formatting? Include all potential titles?
        //find a way to get these sorted by score, franchise, releasedate, etc.
        linesList.Add(line);
        }
    string[] lines = linesList.ToArray();
    System.IO.File.WriteAllLines(@"C:\Users\Gamer\Documents\Top-Game-List-Score-Sorting\RankedDatabase.txt", lines);
    //create a text file they all go into? create another one for ranked by inclusionscore?
    //Took inspiration from https://stackoverflow.com/questions/202813/adding-values-to-a-c-sharp-array
    //as well as https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/file-system/how-to-write-to-a-text-file

    }
    public void printInclusionDatabase() {
    //iterate through entire database, printing it all to a text file
    List<string> linesList = new List<string>();
        foreach(KeyValuePair<string, Game> entry in GameIndex) {
        //print out all the attributes into a string
        string BaseGame = entry.BaseGame;
        //string Title = entry.Title;
        //string CompletionStatus = entry.CompletionStatus;
        int RankedScore = entry.RankedScore;
        int InclusionScore = entry.InclusionScore;
        //string Franchise = entry.Franchise;
        //string Subfranchise = entry.Subfranchise;
        //string ReleaseDate = entry.ReleaseDate;
        string SpecialNotes = entry.SpecialNotes;
        //bool Discontinued = entry.Discontinued;
        //extract values from game entry
        string line = InclusionScore + "," + RankedScore + "," + BaseGame + "," + SpecialNotes;
        //use completionstatus for formatting? Include all potential titles?
        //find a way to get these sorted by score, franchise, releasedate, etc.
        linesList.Add(line);
    }
    string[] lines = linesList.ToArray();
    System.IO.File.WriteAllLines(@"C:\Users\Gamer\Documents\Top-Game-List-Score-Sorting\InclusionDatabase.txt", lines);
    //create a text file they all go into? create another one for ranked by inclusionscore?
    //Took inspiration from https://stackoverflow.com/questions/202813/adding-values-to-a-c-sharp-array
    //as well as https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/file-system/how-to-write-to-a-text-file

    }
}