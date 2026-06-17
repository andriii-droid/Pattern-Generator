from nicegui import ui, events
from ui.components.pattern_manager import PatternManagerPage
from ui.components.line_manager import LineManagerPage
from pattern_coordinator import PatternCoordinator
from models.models import FileConfig, DrawingConfig, CenterConfig
from point import Point
import urllib.parse
from json_config import JSONConfig


class DashboardPage():
    '''handles the dashboard'''
    def __init__(self):
        self.pattern_page = PatternManagerPage(self.update_ui)
        self.line_page = LineManagerPage(self.pattern_page.id.active_ids)
        self.coordinator = PatternCoordinator(self.pattern_page.update_centers)

    def build(self):
        '''builds the dashboard'''
        ui.query('body').classes('bg-slate-100')

        # Main layout split into a 2-column grid (Left: Controls, Right: PDF Viewer)
        with ui.grid(columns='1fr 1fr').classes('w-full max-w-6xl mx-auto my-10 gap-6 p-4'):
    
    # LEFT COLUMN: Controls Card
            with ui.card().classes('p-6 shadow-lg rounded-xl bg-white h-fit'):
                with ui.row().classes('w-full items-center justify-between'):
                    ui.label('Pattern Generator').classes('text-2xl font-bold text-slate-800 mb-2')
                    ui.button('Reset', icon='refresh',
                        on_click=lambda: self.config.save_config()
                        ).props('flat color=red size=md')
                with ui.row().classes('w-full items-center'):
                    ui.button('Generate Pattern', icon='picture_as_pdf', 
                            on_click=lambda: self.coordinator.calculate_and_render(pattern_config=self.pattern_page.get_config(),
                                                                                drawing_config=self.get_drawing_config(),
                                                                                center_config=self.get_center_config())
                            ).classes('w-full').props('color=primary size=md')
                    ui.label('Config').classes('text-lg font-semibold text-slate-700')
                    ui.button('Save', icon='save',
                        on_click=lambda: self.config.save_config()
                        ).props('flat color=orange size=md')
                    ui.button('Download', icon='file_download',
                        on_click=lambda: self.config.save_config()
                        ).props('flat color=orange size=md')
                    ui.button('Upload', icon='file_upload',
                        on_click=lambda: self.config.save_config()
                        ).props('flat color=orange size=md')
                    ui.separator().classes('my-2')
                    self.filename_input = ui.input(label='Filename', placeholder='output', suffix='.pdf/.gcode').classes('w-full mb-4')
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    self.cord = ui.switch('Coordinates', value=False, on_change=lambda e: self.coordinator.draw_cords(bool(e.value)))
                    self.gcode_x = ui.number(label='GCODE X Offset', value=self.coordinator.gcode_offset_x, min=0, step=0.1, on_change=lambda e: setattr(self.coordinator, 'gcode_offset', (e.value, self.gcode_y.value))).classes('w-24')
                    self.gcode_y = ui.number(label='GCODE Y Offset', value=self.coordinator.gcode_offset_y, min=0, step=0.1, on_change=lambda e: setattr(self.coordinator, 'gcode_offset', (self.gcode_x.value, e.value))).classes('w-24')
                
                ui.separator().classes('my-2')
                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Center').classes('text-lg font-semibold text-slate-700')
                    self.num_center_points = ui.number(label='Points', value=1, min=0, step=1).classes('w-24')
                    self.snap = ui.switch('Snap', value=True)
                    self.define_center = ui.switch('Define Center', value=False, on_change=self.define_center)
                ui.separator().classes('my-2')

                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Patterns').classes('text-lg font-semibold text-slate-700')
                    self.points = ui.switch('Points', value=True)
                    self.lines = ui.switch('Lines', value=True)
                    self.sketch = ui.switch('Sketch', value=False)
                ui.separator().classes('my-2')
                
                with ui.row().classes('w-full items-left mb-2'):
                    self.pattern_page.build()
                ui.separator().classes('my-2')

                with ui.row().classes('w-full justify-between items-center mb-2'):
                    ui.label('Lines').classes('text-lg font-semibold text-slate-700')
                ui.separator().classes('my-2')
                with ui.row().classes('w-full items-left mb-2'):
                    self.line_page.build()

                        # RIGHT COLUMN: Preview Card
            with ui.card().classes('p-6 shadow-lg rounded-xl bg-white h-[860px] items-center'):
                
                # Header and Actions row
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label('Preview').classes('text-2xl font-bold text-slate-800')
                    with ui.row().classes('gap-2'):
                        ui.button('Save PDF', icon='save',
                                on_click=lambda: self.coordinator.export_to_pdf(file_config=self.get_file_config())
                                ).props('flat color=green size=md')
                        ui.button('Save GCODE', icon='playlist_add',
                                on_click=lambda: self.coordinator.export_to_gcode(file_config=self.get_file_config())
                                ).props('flat color=blue size=md')      
                with ui.row().classes('w-full justify-between items-center mb-4'):
                        string_len = ui.label('String').classes('text-slate-800')   
                        string_len.bind_text_from(self.coordinator, 'string_length')    

                raw_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 105 148" width="100%"></svg>'
                blank_bg = f'data:image/svg+xml;utf8,{urllib.parse.quote(raw_svg)}'
                    
                # 2. Assign the click function directly to on_mouse
                self.ii = ui.interactive_image(
                    blank_bg, 
                    cross=False,
                    on_mouse=lambda e: self.coordinator.handle_center((e.image_x, e.image_y), self.num_center_points.value, bool(self.snap.value))).classes('h-full w-auto max-h-[700px] object-contain shadow-md rounded-lg bg-white')
                self.ii.on('loaded', lambda e: self.coordinator.set_canvas_dimensions(e.args))
                self.ii.bind_content_from(self.coordinator, 'canvas_content')

        self.config = JSONConfig(self)
        self.config.load_config()

    def get_drawing_config(self):
        '''collects drawing config data'''
        return DrawingConfig(
            draw_points=bool(self.points.value),
            draw_lines=bool(self.lines.value),
            draw_sketch=bool(self.sketch.value),
            line_configs=self.line_page.get_config()
        )

    def get_file_config(self):
        '''collects file config data'''
        return FileConfig(
            filename=self.filename_input.value,
            gcode_offset_x=float(self.gcode_x.value),
            gcode_offset_y=float(self.gcode_y.value)
        )
    
    def get_center_config(self):
        '''collects setting config data'''
        return CenterConfig(
            center_points=self.coordinator.center.center_points
        )
    
    def update_ui(self):
        self.line_page.update_active_patterns()

    def define_center(self):
        '''enables the crossair'''
        if self.define_center.value:
            self.ii.props('cross="black"')
            self.coordinator.define_center = True
        else:
            self.ii.props(remove='cross')
            self.coordinator.define_center = False


