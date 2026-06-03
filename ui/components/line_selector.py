from nicegui import ui

class LineSelector():
    def __init__(self):
        self.chips_list = []

        with ui.row().classes('items-center') as self.chips:
            self.label_input = ui.select(with_input=True,options=[]).on('keydown.enter', self.add_line_chip).classes('w-50')
            with self.label_input.add_slot('append'):
                ui.button(icon='add', on_click=self.add_line_chip).props('round dense flat')

    def add_line_chip(self):
        if len(self.chips_list) == 2:
            ui.notify('Only two patterns can be defined!', type='warning')
        elif self.label_input.value is None:
            ui.notify('Choose a pattern from the dropdown', type='warning')
        elif self.label_input.value.startswith("Spline"):
            with self.chips:
                chip = ui.chip(self.label_input.value, icon='label', color='green', removable=True)
                chip.on('remove', lambda: self.handle_chip_removal(chip))
                self.chips_list.append(chip)   
        else:
            with self.chips:
                chip = ui.chip(self.label_input.value, icon='label', color='blue', removable=True)
                chip.on('remove', lambda: self.handle_chip_removal(chip))
                self.chips_list.append(chip)        
        self.label_input.value = ''

    def handle_chip_removal(self, chip_instance):
        """Safely extracts the deleted chip out of your tracking list."""
        if chip_instance in self.chips:
            self.chips_list.remove(chip_instance)
