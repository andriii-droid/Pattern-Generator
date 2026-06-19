import json
from nicegui import ui, events


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

    def download_current_config(self):
        '''downloads current config'''
        ui.notify('Current config downloaded!', type='positive')
        ui.download.file('config/current_config.json')

    def upload_config(self, e: events.UploadEventArguments):
        try:

            raw_bytes = e.file.read()
            

            # Parse the bytes directly into your dictionary
            data = json.loads(raw_bytes)

            # Access your nested configuration data smoothly!
            global_settings = data.get("global_settings", {})
            snap_value = global_settings.get("Snap", False)

            ui.notify(f"Config Loaded! Snap is set to: {snap_value}")
            print(data)
        except Exception as err:
            ui.notify(f"Failed to process file: {err}", type="negative")

    def _load_config(self, file):
        '''loads specified config'''
        global_settings = {}
        with open(file, 'r') as f:
            config = json.load(f)
            global_settings = config["global_settings"]
        
        for control in self.global_controls_list:
            control.value = global_settings[control.config_id]
            control.update()
            

