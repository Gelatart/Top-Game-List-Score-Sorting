using System.IO;

namespace DefaultNamespace
{
    public class Main
    {
        static void Main(string[] args)
        {
            // Display the number of command line arguments:
            //Source for how to read files in this way: https://stackoverflow.com/questions/5840443/how-to-read-all-files-inside-particular-folder
            foreach (string file in Directory.EnumerateFiles(folderPath, "*.txt")) 
            {
                string contents = File.ReadAllText(file);
            }
        }
    }
}