import json
from nicegui import ui


class JSONConfig():
    def __init__(self, page):
        '''loads starting config'''
        self.global_controls_list = []
        controls = {"Coordinates":page.cord,
                    "Gcode X":page.gcode_x,
                    "Gcode Y":page.gcode_y,
                    "Number Centerpoints":page.num_center_points,
                    "Snap":page.snap,
                    "Define Center":page.define_center,
                    "Draw points":page.points,
                    "Draw lines":page.lines,
                    "Draw sketch lines":page.sketch}
        
        for id, control in controls.items():
            control.config_id = id
            self.global_controls_list.append(control)
           

    def save_current_config(self):
        '''Saves current config as json to file'''
        ui.notify('Config has been saved!', type="positive")

        global_config = {"global_settings":{control.config_id:control.value for control in self.global_controls_list}}
        with open('config/current_config.json', 'w') as f:
            json.dump(global_config, f, indent=4)

    def load_current_config(self):
        '''loads current config to UI'''
        self._load_config("config/current_config.json")


    def load_default_config(self):
        '''load default config'''
        self._load_config("config/default_config.json")

    def _load_config(self, file):
        '''loads specified config'''
        global_settings = {}
        with open(file, 'r') as f:
            config = json.load(f)
            global_settings = config["global_settings"]
        
        for control in self.global_controls_list:
            control.value = global_settings[control.config_id]
            control.update()
            

