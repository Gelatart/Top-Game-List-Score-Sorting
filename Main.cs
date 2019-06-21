using System.IO;

namespace DefaultNamespace
{
    public class Main
    {
        Dictionary<Game, string> GameIndex = new Dictionary<Game, string>();
        static void Main(string[] args)
        {
            // Display the number of command line arguments:
            //Source for how to read files in this way: https://stackoverflow.com/questions/5840443/how-to-read-all-files-inside-particular-folder
            foreach (string file in Directory.EnumerateFiles(folderPath, "*.txt")) 
            {
                string contents = File.ReadAllText(file);
                string line;
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
                    Game Entry = Game(BaseGame,Rank,Title,CompletionStatus,Franchise,Subfranchise,ReleaseDate,SpecialNotes,Discontinued); //instantiate with new values
                    GameIndex.add(Entry, BaseGame); //do an if/else check to see if already in dictionary first
                }
            }
        }
    }
}