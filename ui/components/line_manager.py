from nicegui import ui


class LineManagerPage():
    def __init__(self):
        pass

    def build(self):
        ui.button(icon='add', on_click=self.add_line_selector).props('round color=blue size=md').classes('i')

        self.container = ui.row().classes('w-full gap-2')

    def add_line_selector(self):
        with self.container:
            ui.label('label')