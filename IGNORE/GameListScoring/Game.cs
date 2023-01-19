using System;

namespace DefaultNamespace
{
    public class Game
    {
        public string BaseGame;
        public string Title;
        public string CompletionStatus;
        public int RankedScore;
        public int InclusionScore;
        public float AverageScore;
        public string Franchise;
        public string Subfranchise;
        public DateTime ReleaseDate;
        //list of Lists on?
        public string SpecialNotes;
        //public bool Discontinued;

        public Game(string BaseInput, int RankInput, string TitleInput, string CompletionInput, string FranchiseInput, string SubInput, DateTime ReleaseInput, string NotesInput)
        {
            BaseGame = BaseInput;
            Title = TitleInput;
            CompletionStatus = CompletionInput;
            RankedScore = RankInput;
            InclusionScore = 1;
            AverageScore = RankInput;
            Franchise = FranchiseInput;
            Subfranchise = SubInput;
            ReleaseDate = ReleaseInput;
            SpecialNotes = NotesInput;
            //Discontinued = DiscInput;
        }

        public Game()
        {
            BaseGame = "N/A";
            Title = "N/A";
            CompletionStatus = "N/A";
            RankedScore = 0;
            InclusionScore = 0;
            AverageScore = 0;
            Franchise = "N/A";
            Subfranchise = "N/A";
            ReleaseDate = new DateTime(0, 0, 0);
            SpecialNotes = "N/A";
            //Discontinued = false;
        }
    }
}