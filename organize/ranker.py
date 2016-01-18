import os
import json


class Ranker:
    def __init__(self, rank_file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../files/rank.json')):
        self._rank = {}
        self.rank_file_path = rank_file_path
        self._setup()

    def _setup(self):
        with open(self.rank_file_path, 'r') as rank_file:
            ranked_names = json.load(rank_file)
        rank_file.close()
        for i in range(len(ranked_names)):
            self._rank[ranked_names[i]] = i
        return None

    def rank(self, names):
        if len(names) == 0:
            return None
        name_rank = {}
        for name in names:
            if name in self._rank:
                name_rank[self._rank[name]] = name
        if len(name_rank) == 0:
            return None
        name_keys = sorted(list(name_rank.keys()))
        return name_rank[name_keys[0]]
