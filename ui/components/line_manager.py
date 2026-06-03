from nicegui import ui
from ui.components.line_selector import LineSelector


class LineManagerPage():
    def __init__(self, active_ids):
        self.selector_list = []
        self.active_ids = active_ids

    def build(self):
        ui.button(icon='add', on_click=self.add_line_selector).props('round color=blue size=md').classes('i')
        self.container = ui.column().classes('w-full gap-2')

    def add_line_selector(self):
        with self.container:
            line_sel = LineSelector()
        self.selector_list.append(line_sel)
        self.update_active_patterns()
        

    def update_active_patterns(self):
        '''update the line selector with available patterns'''
        for sel in self.selector_list:
            options = []
            for id, str in self.active_ids.items():
                options.append(f"{str} {id}")
            sel.label_input.options = options
            sel.label_input.update()



