from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GameObject:
    #add seasonal attribute? would have to set manually in its own text file?
    #Attributes without defaults
    title: str
    ranked_score: int #rank input
    total_count: int #total input
    #Attributes with defaults
    igdb_ID: Optional[int] = None
    igdb_found: bool = False
    list_count: int = 1
    lists_referencing: list[str] = field(default_factory=list)
    completed: bool = False
    list_platforms: list[str] = field(default_factory=list)
    #release_date: str = 'Unknown' #can this be a date value?
    #^replacing with a list of dictionaries to better align with IGDB setup and new release_dates table
    release_dates = list[dict]
    player_counts: list[str] = field(default_factory=list)
    #update player_counts to a more fitting name like player_modes? game_modes?
    list_developers: list[str] = field(default_factory=list)
    list_publishers: list[str] = field(default_factory=list)
    list_companies: list[str] = field(default_factory=list)
    genres: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)

    def __post_init__(self):
        #self.lists_referencing.append(self.list_source)
        #Should we put something else here? still have it?
        pass

    def to_dict(self) -> dict:
        #See if this causes issues anywhere where we would still like to keep lists?
        #In that case, bring this functionality more to the part where we export lists to excel
        result = self.__dict__
        for k, v in result.items():
            if isinstance(v, list):
                result[k] = ", ".join(map(str, v))
        return result

"""
OLD GAMEOBJECT IMPLEMENTATION:
class GameObject:
    def __init__(self, rank):
        #Add seasonal attribute? Would have to set manually in my own text files?
        self.igdb_ID = None
        self.igdb_found = False
        self.ranked_score = rank
        self.list_count = 1
        self.lists_referencing = []
        self.total_count = 0
        self.completed = False
        self.list_platforms = []
        self.release_date = 'Unknown' #Can I set this to some date value?
        self.player_counts = []
        self.list_developers = []
        self.list_publishers = []
        self.list_companies = []
        self.genres = []
        self.themes = []

    def __init__(self, rank, list):
        self.igdb_ID = None
        self.igdb_found = False
        self.ranked_score = rank
        self.list_count = 1
        self.lists_referencing = []
        self.lists_referencing.append(list)
        self.total_count = 0
        self.completed = False
        self.list_platforms = []
        self.release_date = 'Unknown'  # Can I set this to some date value?
        self.player_counts = []
        self.list_developers = []
        self.list_publishers = []
        self.list_companies = []
        self.genres = []
        self.themes = []

    def __init__(self, rank, list, total):
        self.igdb_ID = None
        self.igdb_found = False
        self.ranked_score = rank
        self.list_count = 1
        self.lists_referencing = []
        self.lists_referencing.append(list)
        self.total_count = total
        self.completed = False
        self.list_platforms = []
        self.release_date = 'Unknown'
        self.player_counts = []
        self.list_developers = []
        self.list_publishers = []
        self.list_companies = []
        self.genres = []
        self.themes = []
    # CONSIDER MAKING AN EXPORT FUNCTION FOR THE CLASS TO CONVERT TO DICTIONARY?
"""