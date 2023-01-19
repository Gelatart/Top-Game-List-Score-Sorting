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
        public string Franchise;
        public string Subfranchise;
        public DateTime ReleaseDate;
        //list of Lists on
        public string SpecialNotes;
        //public bool Discontinued;

        public Game(string BaseInput, int RankInput, string TitleInput, string CompletionInput, string FranchiseInput, string SubInput, DateTime ReleaseInput, string NotesInput, bool DiscInput)
        {
            BaseGame = BaseInput;
            Title = TitleInput;
            CompletionStatus = CompletionInput;
            RankedScore = RankInput;
            InclusionScore = 1;
            Franchise = FranchiseInput;
            Subfranchise = SubInput;
            ReleaseDate = ReleaseInput;
            SpecialNotes = NotesInput;
            //Discontinued = DiscInput;
        }
        public Game()
        {
            BaseGame = "";
            Title = "";
            CompletionStatus = "";
            RankedScore = 0;
            InclusionScore = 0;
            Franchise = "";
            Subfranchise = "";
            ReleaseDate = new DateTime(0,0,0);
            SpecialNotes = "";
            //Discontinued = true;
        }
    }
}
