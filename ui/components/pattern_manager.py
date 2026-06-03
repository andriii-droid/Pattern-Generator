from nicegui import ui, app
from ui.components.shape_row import ShapeRow
from ui.components.spline_row import SplineRow
from models.models import PatternConfig
from helpers.id import ID


class PatternManagerPage:
    '''handles shape and spline rows'''
    def __init__(self, update_callback):
        # Store instances of PatternRow objects rather than dictionaries
        self.shape_list: list[ShapeRow] = []
        self.spline_list: list[SplineRow] = []
        self.id = ID()
        self.update_callback = update_callback

    def build(self):
        '''build the rows'''
        ui.button('Add Shape', icon='add', on_click=self.add_shape_row).props('outline size=sm color=primary')
        ui.button('Add Spline', icon='add', on_click=self.add_spline_row).props('outline size=sm color=primary')

        self.container = ui.column().classes('w-full gap-2')
        self.add_shape_row()

    def add_shape_row(self):
        '''add shape row'''
        with self.container:
            # Create a new row, and pass our delete method as the callback
            new_row = ShapeRow(on_delete_callback=self.remove_row, id=self.id.new_id)
        self.shape_list.append(new_row)
        self.update_callback()

    def add_spline_row(self):
        '''Add a spline row'''
        with self.container:
            # Create a new row, and pass our delete method as the callback
            new_row = SplineRow(on_delete_callback=self.remove_row, id=self.id.new_id)
        self.spline_list.append(new_row)
        self.update_callback()

    def remove_row(self, row_instance):
        """Removes the specified row instance"""
        self.container.remove(row_instance.row)
        self.id.return_id(row_instance.id)
        self.update_callback()
        if isinstance(row_instance, ShapeRow):
            self.shape_list.remove(row_instance)
        elif isinstance(row_instance, SplineRow):
            self.spline_list.remove(row_instance)

    def get_config(self): # TODO
        '''Collect all the data from the splines and shapes and return it as an PatternConfig'''
        pattern_config = PatternConfig([])
        for shape in self.shape_list:
            pattern_config.patterns.append(shape.get_config())
        for spline in self.spline_list:
            pattern_config.patterns.append(spline.get_config())
        return pattern_config
