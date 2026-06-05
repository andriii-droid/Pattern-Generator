from nicegui import ui
from models.models import LineConfig


class LineSelector():
    def __init__(self, on_delete_callback):
        self.chips_list = []
        self.on_delete = on_delete_callback

        with ui.row().classes('items-center') as self.chips:
            ui.button(icon='delete', on_click=lambda: self.on_delete(self)).props('flat color=red')
            self.label_input = ui.select(with_input=True,options=[]).on('keydown.enter', self.add_line_chip).classes('w-50')
            self.offset = ui.number(label='Offset', value=1, min=0, step=1).classes('w-24')
            with self.label_input.add_slot('append'):
                ui.button(icon='add', on_click=self.add_line_chip).props('round dense flat')

    def add_line_chip(self):
        id = self.label_input.value
        if len(self.chips_list) == 2:
            ui.notify('Only two patterns can be defined!', type='warning')
        elif self.label_input.value is None:
            ui.notify('Choose a pattern from the dropdown', type='warning')
        elif self.label_input.options[id].startswith("Spline"):
            with self.chips:
                chip = ui.chip(self.label_input.options[id], icon='label', color='green', removable=True).props('outline')
                chip.on('remove', lambda: self.handle_chip_removal(chip))
                self.chips_list.append(chip)   
        else:
            with self.chips:
                chip = ui.chip(self.label_input.options[id], icon='label', color='blue', removable=True).props('outline')
                chip.on('remove', lambda: self.handle_chip_removal(chip))
                self.chips_list.append(chip)        
        self.label_input.value = ''

    def handle_chip_removal(self, chip_instance):
        """Safely extracts the deleted chip out of your tracking list."""
        if chip_instance in self.chips:
            self.chips_list.remove(chip_instance)

    def get_config(self):
        """Helper method to extract current UI state """
        return LineConfig(
            pat_id=[int(chip.text[-1]) for chip in self.chips_list],
            offset=int(self.offset.value))
            
            
        