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
           

    def save_config(self):
        '''Saves current config as json to file'''
        ui.notify('Config has been saved!', type="positive")

        global_config = {"global_settings":{control.config_id:control.value for control in self.global_controls_list}}
        with open('config1.json', 'w') as f:
            json.dump(global_config, f, indent=4)

    def load_config(self):
        '''loads config to UI'''
        global_settings = {}
        with open('config1.json', 'r') as f:
            config = json.load(f)
            global_settings = config["global_settings"]
        
        for control in self.global_controls_list:
            control.value = global_settings[control.config_id]
            control.update()

            

