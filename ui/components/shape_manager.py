from nicegui import ui, app
from ui.components.shape_row import ShapeRow
from ui.components.spline_row import SplineRow


class ShapeManagerPage:
    def __init__(self):
        # Store instances of PatternRow objects rather than dictionaries
        self.shape_list: list[ShapeRow] = []
        self.spline_list: list[SplineRow] = []

    def build(self):
        ui.button('Add Shape', icon='add', on_click=self.add_shape_row).props('outline size=sm color=primary')
        ui.button('Add Spline', icon='add', on_click=self.add_spline_row).props('outline size=sm color=primary')

        self.container = ui.column().classes('w-full gap-2')

    def add_shape_row(self):
        with self.container:
            # Create a new row, and pass our delete method as the callback
            new_row = ShapeRow(on_delete_callback=self.remove_row)
            self.shape_list.append(new_row)

    def add_spline_row(self):
        with self.container:
            # Create a new row, and pass our delete method as the callback
            new_row = SplineRow(on_delete_callback=self.remove_row)
            self.spline_list.append(new_row)

    def remove_row(self, row_instance):
        """Triggered by the child row."""
        # 1. Remove the HTML elements from the browser screen
        self.container.remove(row_instance.row)
        # 2. Remove the row object from our tracking list
        if isinstance(row_instance, ShapeRow):
            self.shape_list.remove(row_instance)
        elif isinstance(row_instance, SplineRow):
            self.spline_list.remove(row_instance)

    def process_all_shapes(self): # TODO
        """Example: Grab data from all rows when a 'Submit' button is clicked."""
        for row in self.patterns_list:
            data = row.get_data()
            print(f"Processing shape {data['shape']} with color {data['hex']}")