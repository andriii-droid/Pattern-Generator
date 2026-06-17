import json
from ui.pages.Dashboard import DashboardPage

class JSONConfig():
    def __init__(self, page: DashboardPage):
        '''loads starting config'''
        self.global_controls = []
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
            self.global_controls.append(control)
           

    def save_config(self):
        '''Saves current config as json to file'''

        global_config = {"global_settings":{control.config_id:control.value for control in self.global_controls}}
        with open('config1.json', 'w') as f:
            json.dump(global_config, f, indent=4)


