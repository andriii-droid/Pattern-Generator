import json
from ui.pages.Dashboard import DashboardPage

class JSONConfig():
    def __init__(self, page: DashboardPage):
        '''loads starting config'''
        self.global_settings = []



    def save_config(self):
        '''Saves current config as json to file'''
        config = {"key1": "value1", "key2": "value2"}

        with open('config1.json', 'w') as f:
            json.dump(config, f)


