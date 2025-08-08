import json
import os

#Give the user the option to clear this local cache and start fresh if they want?
#to allow us to start fresh if we want to

"""
Optional Improvements Later (chatgpt recommendations)
-Add expiration (e.g., refresh after 1 month)
-Store by IGDB ID as a secondary key
-Convert to SQLite if the cache gets large
"""

class CacheManager:
    def __init__(self, cache_file="igdb_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_cache(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)

    #def get(self, key):
        #return self.cache.get(key)
    def get(self, igdb_id):
        return self.cache.get(str(igdb_id))

    #def set(self, key, value):
        #self.cache[key] = value
        #self.save_cache()

    def set(self, igdb_id, data):
        self.cache[str(igdb_id)] = data
        self.save_cache()