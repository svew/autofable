from pathlib import Path
import os
from quest import Quest

RESOURCE_PATH = Path('resources')
QUESTS_PATH = RESOURCE_PATH / 'quests'
IMAGES_PATH = RESOURCE_PATH / 'images'
BATTLEPLANS_PATH = RESOURCE_PATH / 'battleplans'

class AutoFable:
    def __init__(self):
        self.quests = []

    def load(self):
        """Loads the resources found in the resource folder
        """
        if len(self.quests) > 0:
            raise 'AutoFable has already been loaded'
        for root, dirs, files in os.walk(QUESTS_PATH):
            for name in files:
                if os.path.splitext(name)[1] == '.yaml':
                    file_path = os.path.join(root, name)
                    quest = Quest.load(file_path)
                    self.quests.append(quest)
