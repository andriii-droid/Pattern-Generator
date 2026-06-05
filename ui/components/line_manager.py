from nicegui import ui
from ui.components.line_selector import LineSelector
from models.models import LineConfig

class LineManagerPage():
    def __init__(self, active_ids):
        self.selector_list = []
        self.active_ids = active_ids

    def build(self):
        ui.button('add line',icon='add', on_click=self.add_line_selector).props('outline size=sm color=primary')
        ui.button('remove all', icon='delete', on_click=self.delete_all_line_selectors).props('outline size=sm color=red')
        self.container = ui.column().classes('w-full gap-2')

    def add_line_selector(self):
        with self.container:
            line_sel = LineSelector(self.delete_line_selector_row)
        self.selector_list.append(line_sel)
        self.update_active_patterns()
        

    def update_active_patterns(self):
        '''update the line selector with available patterns'''
        for sel in self.selector_list:
            options = {}
            for id, str in self.active_ids.items():
                options[id] = (f"{str} {id}")
            sel.label_input.options = options
            sel.label_input.update()

    def delete_line_selector_row(self, selector_instance):
        self.container.remove(selector_instance.chips)
        self.selector_list.remove(selector_instance)

    def delete_all_line_selectors(self):
        sel_list = self.selector_list.copy()
        for sel in sel_list:
            self.delete_line_selector_row(sel)
        
    def get_config(self):
        '''return the data as LineConfig'''
        config_list = []
        for sel in self.selector_list:
            config_list.append(LineConfig(pat_id=sel.get_config(),
                       offset=0))#TODO
        return config_list
        



