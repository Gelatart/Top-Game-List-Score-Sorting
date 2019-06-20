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
                    Game entry;
                    string Title;
                    GameIndex.add(entry, Title); //do an if/else check to see if already in dictionary first
                }
            }
        }
    }
}