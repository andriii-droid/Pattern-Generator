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
                    "Center Offset":page.offset_center,
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
        ui.notify("Default config loaded!", type="positive")

    def download_current_config(self):
        '''downloads current config'''
        ui.notify('Current config downloaded!', type='positive')
        ui.download.file('config/current_config.json')

    async def upload_config(self, e: events.UploadEventArguments):
        '''loads a config to the ui'''
        try:
            file_content = await e.file.text()

            config_data = json.loads(file_content)
            global_settings = config_data["global_settings"]
            print(global_settings)

            for control in self.global_controls_list:
                control.value = global_settings[control.config_id]
                control.update()

        except json.JSONDecodeError:
            ui.notify("Error: Invalid JSON format.", type="negative")
        except Exception as ex:
            ui.notify(f"An error occurred: {ex}", type="negative")
        finally:
            e.sender.reset()
            ui.notify("Config loaded!", type="positive")

    def _load_config(self, file):
        '''loads specified config'''
        global_settings = {}
        with open(file, 'r') as f:
            config = json.load(f)
            global_settings = config["global_settings"]
        
        for control in self.global_controls_list:
            control.value = global_settings[control.config_id]
            control.update()
            

