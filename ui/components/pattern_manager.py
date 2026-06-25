from nicegui import ui, app
from ui.components.shape_row import ShapeRow
from ui.components.spline_row import SplineRow
from models.models import PatternConfig
from helpers.id import ID
from json_config import JSONConfig


class PatternManagerPage:
    '''handles shape and spline rows'''
    def __init__(self, update_callback, config):
        # Store instances of PatternRow objects rather than dictionaries
        self.shape_list: list[ShapeRow] = []
        self.spline_list: list[SplineRow] = []
        self.id = ID()
        self.update_callback = update_callback
        self.collapsed = False
        self.options = [0]
        self.config = config

    def build(self):
        '''build the rows'''
        ui.button('Add Shape', icon='add', on_click=self.add_shape_row).props('outline size=sm color=primary')
        ui.button('Add Spline', icon='add', on_click=self.add_spline_row).props('outline size=sm color=primary')
        self.expand = ui.button('Collapse', on_click=self.expand_collapse_rows).props('outline size=sm color=primary')
        ui.button('Remove All', icon='delete', on_click=self.remove_all_rows).props('outline size=sm color=red')

        self.container = ui.column().classes('w-full gap-2')
        self.add_shape_row()

    def add_shape_row(self):
        '''add shape row'''
        with self.container:
            # Create a new row, and pass our delete method as the callback
            new_row = ShapeRow(on_delete_callback=self.remove_row, id=self.id.new_shape_id, cp_options=self.options)
        self.shape_list.append(new_row)
        self.config.add_shape(new_row)
        self.update_callback()

    def add_spline_row(self):
        '''Add a spline row'''
        with self.container:
            # Create a new row, and pass our delete method as the callback
            new_row = SplineRow(on_delete_callback=self.remove_row, id=self.id.new_spline_id, cp_options=self.options)
        self.spline_list.append(new_row)
        self.update_callback()

    def remove_row(self, row_instance):
        """Removes the specified row instance"""
        self.container.remove(row_instance.row)
        self.id.return_id(row_instance.id)
        self.update_callback()
        if isinstance(row_instance, ShapeRow):
            self.shape_list.remove(row_instance)
            self.config.remove_shape(row_instance)
        elif isinstance(row_instance, SplineRow):
            self.spline_list.remove(row_instance)

    def remove_all_rows(self):
        row_list = self.shape_list.copy() + self.spline_list.copy()
        for row in row_list:
            self.remove_row(row)
        
    def get_config(self):
        '''Collect all the data from the splines and shapes and return it as an PatternConfig'''
        pattern_config = PatternConfig([])
        for shape in self.shape_list:
            pattern_config.patterns.append(shape.get_config())
        for spline in self.spline_list:
            pattern_config.patterns.append(spline.get_config())
        return pattern_config
    

    def expand_collapse_rows(self):
        row_list = self.shape_list + self.spline_list
        for row in row_list:
            row.expand.value = self.collapsed
        if self.collapsed:
            self.expand.set_text("collapse")
        else: 
            self.expand.set_text("expand")
        self.collapsed = not self.collapsed

    def update_centers(self, options):
        self.options = options
        for shape_row in self.shape_list:
            shape_row.centers.options = options
            shape_row.centers.update()

        for spline_row in self.spline_list:
            spline_row.centers.options = options
            spline_row.centers.update()

