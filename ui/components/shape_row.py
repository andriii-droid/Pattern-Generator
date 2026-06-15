from nicegui import ui
from models.models import ShapeConfig
from point import Point

class ShapeRow:
    def __init__(self, on_delete_callback, id, cp_options):
        """
        Represents a single pattern row UI element.
        :param on_delete_callback: A function to call when the delete button is clicked.
        """
        self.id = id
        self.on_delete = on_delete_callback
        
        shape_options = {0: 'Spline', 2: 'Line', 3: 'Triangle', 4: 'Square', 5: 'Pentagon'}

        def handle_type_change(e):
            if e.value == 'line':
                self.line_points.value = 0
                self.num_shapes.value = 20
            elif e.value == 'dotted':
                self.line_points.value = 5
                self.num_shapes.value = 1

        # Use standard 'self.' attributes so other classes can easily read their values
        with ui.column().classes('items-left w-full bg-slate-50 p-3 rounded-lg shadow-sm') as self.row:
            with ui.expansion(value=True).classes('font-semibold text-s text-slate-500 mt-1 w-full') as self.expand:
                with self.expand.add_slot('header'):
                    with ui.row().classes('w-full items-center justify-between'):
                        with ui.row():
                            ui.label(f"Shape {self.id}").classes('text-lg font-medium')
                            self.label = ui.label().classes('font-semibold text-s text-slate-500 mt-1 self-end justify-start')
                        ui.button(icon='delete', on_click=lambda: self.on_delete(self)).props('flat color=red class=mt-auto').on('click.stop')

                with ui.row().classes('items-center w-full'):
                    ui.label('Center').classes('font-semibold text-xs text-slate-500 mt-1 self-start')
                    self.centers = ui.radio(cp_options, value=0).classes('grow').props('inline')
                    self.label.bind_text_from(
                        target_object=self.centers, 
                        target_name='value', 
                        backward=lambda v: f"Centerpoint {v}")
                with ui.row().classes('items-center w-full'):
                    self.shape = ui.select(label='Shape', options=shape_options, value=3).classes('w-28')
                    self.line_type = ui.select(label="Linetype", options=['line', 'dotted'], value='line').classes('w-26').on_value_change(handle_type_change)
                    self.num_shapes = ui.number(label='Number', value=20, min=1, step=1).classes('w-24') \
                        .bind_visibility_from(self.line_type, 'value', backward=lambda v: v == 'line') 
                    self.size = ui.number(label='Size', value=40, min=1).classes('w-24')
                    
                    # Simple color hex state stored on the class instance
                    self.hex_color = '#000000'
                    with ui.button(icon='colorize') as button:
                        ui.color_picker(on_pick=lambda e: (button.style(f'background-color: {e.color} !important;'), 
                                                        setattr(self, 'hex_color', e.color)))
                    
                    self.offset = ui.slider(min=0, max=1, step=0.01, value=1).classes('w-32')
                    ui.label().bind_text_from(self.offset, 'value').classes('w-6')
                    
                    
                    self.line_points = ui.number(label="Points", value=0, min=-1, step=1).classes('w-24') \
                        .bind_visibility_from(self.line_type, 'value', backward=lambda v: v == 'dotted') 

    def get_config(self):
        """Helper method to export the current UI state as shape config object"""
        return ShapeConfig(
            shape_type=int(self.shape.value),
            num_shapes=int(self.num_shapes.value),
            size=self.size.value,
            hex_color=self.hex_color,
            offset=self.offset.value,
            line_points=int(self.line_points.value),
            center=Point(0,0),
            id=self.id,
            center_points=self.centers.value
        )