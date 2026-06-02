from nicegui import ui
from ui.components.line_selector import LineSelector


class LineManagerPage():
    def __init__(self):
        pass

    def build(self):
        ui.button(icon='add', on_click=self.add_line_selector).props('round color=blue size=md').classes('i')

        self.container = ui.column().classes('w-full gap-2')

    def add_line_selector(self):
        with self.container:
            line_sel = LineSelector()
