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
        public string ReleaseDate;
        //list of Lists on
        public string SpecialNotes;
        public bool Discontinued;

        public Game(string BaseInput, int RankInput, string TitleInput, string CompletionInput, string FranchiseInput, string SubInput, string ReleaseInput, string NotesInput, bool DiscInput)
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
            Discontinued = DiscInput;
        }
    }
}
