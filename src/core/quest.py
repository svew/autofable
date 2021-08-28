from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class Quest():

    def __init__(self):
        self.name = ""
        self.alt_name = ""
        self.location = ""
        self.prereqs = ""
        self.objective = ""
        self.scaled = False
        self.exp = ""
        self.gold = ""
        self.monsters = []
        self.npcs = []
        self.rewards = {}

    def search_match(self, query):
        """Returns a float denoting how closely the quest object matches the phrase.

        Args:
            query (str): Phrase being searched for

        Returns:
            float: Non-negative number denoting how close the quest object matches the phrase. The
            closer the number is to 0, the closer it matches. This means, given the same search
            phrase, if quest A returns a search_match of 0.7 and quest B returns a search_match of
            1.8, quest A is a closer match for that phrase.
        """
        i = self.name.lower().find(query)
        if i != -1:
            return i
        return float('inf')

    def __str__(self):
        return f'[Quest, Name: {self.name}]'

    @staticmethod
    def load(path):
        """Creates a new Quest object given the path to a corresponding .yaml file

        Args:
            path (str): Path to a .yaml file

        Returns:
            Quest: New quest object containing the information in the .yaml file
        """
        with open(path, 'r') as f:
            obj = load(f, Loader=Loader)

        quest = Quest()

        if 'quest' in obj:
            quest_obj = obj['quest']
            if 'name' in quest_obj:
                quest.name = quest_obj['name']
            if 'alt_name' in quest_obj:
                quest.alt_name = quest_obj['alt_name']
            if 'location' in quest_obj:
                quest.location = quest_obj['location']
            if 'prereqs' in quest_obj:
                quest.prereqs = quest_obj['prereqs']
            if 'objective' in quest_obj:
                quest.objective = quest_obj['objective']
            if 'scaled' in quest_obj:
                quest.scaled = bool(quest_obj['scaled'])
            if 'exp' in quest_obj:
                quest.exp = quest_obj['exp']
            if 'gold' in quest_obj:
                quest.gold = quest_obj['gold']
            if 'monsters' in quest_obj:
                quest.monsters = quest_obj['monsters']
            if 'npcs' in quest_obj:
                quest.npcs = quest_obj['npcs']
            if 'rewards' in quest_obj:
                quest.rewards = quest_obj['rewards']

        return quest


class QuestRunner():

    def __init__(self, quest, fablescreen):
        pass