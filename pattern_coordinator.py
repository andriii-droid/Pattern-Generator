from models.models import PatternConfig, DrawingConfig, FileConfig, SettingsConfig, ShapeConfig, SplineConfig
from point import Point
from shape import Shape
from spline import Spline
from gcode import GCODE
from draw import Draw
from pdf import PDF
from nicegui import ui, events


class PatternCoordinator():
    '''exposes functions to the dashboard manipulate patterns '''
    def __init__(self):
        self.patterns: list[Shape | Spline] = []
        self.gcode = GCODE(self)
        self.draw = Draw()
        self.pdf = PDF()
        self._canvas_content = ''''''

    def calculate_and_render(self, pattern_config: PatternConfig, 
                             drawing_config: DrawingConfig, 
                             settings_config: SettingsConfig):
        '''calculates and then draws the patterns to the ui'''
        self._calculate(pattern_config=pattern_config, settings_config=settings_config)
        self._render_to_ui(drawing_config=drawing_config)

    def _calculate(self, pattern_config: PatternConfig, 
                   settings_config: SettingsConfig):
        '''calculates the specified patterns and stores the patterns'''
        self.patterns = []

        #create center points
        c = Shape(ShapeConfig(
            shape_type=int(settings_config.num_center_points),
            num_shapes=1,
            size=float(settings_config.center_point_radius),
            hex_color="", 
            offset=1,
            line_points=0,
            center=Point(0,0),
            id=-1
            ))
        c.generate()
        center_points = c.points
        if settings_config.keep_center and len(center_points) != 1:
            center_points.append(Point(0,0))

        #for each center point create one pattern
        for cp in center_points:
            for pattern in pattern_config.patterns:
                pattern.center = cp
                if isinstance(pattern, ShapeConfig):
                    s = Shape(pattern)
                    s.generate()
                    self.patterns.append(s)
                elif isinstance(pattern, SplineConfig):
                    s = Spline(pattern)
                    s.generate()
                    self.patterns.append(s)
                

    def _render_to_ui(self, drawing_config: DrawingConfig):
        '''draws points and lines to the ui'''
        self._canvas_content = ''''''
        if drawing_config.draw_points: #Draws Points if configured
            for pat in self.patterns:
                self._canvas_content += self.draw.draw_points(pat)

        for pat in self.patterns:
            self._canvas_content += self.draw.draw_lines(drawing_config, pat)

        if drawing_config.draw_coordinates:
            self._canvas_content += self.draw.draw_cords()


    def export_to_pdf(self, file_config: FileConfig):
        if file_config.filename == "":
            ui.notify("Provide a Filename!", type='warning')
        else:
            pdf_bytes = self.pdf.generate_pdf(self.canvas_content)
            ui.download(pdf_bytes, filename=file_config.filename+".pdf")

    def export_to_gcode(self, file_config: FileConfig):
        if file_config.filename == "":
            ui.notify("Provide a Filename!", type='warning')
        else:
            ui.download.content(self.gcode.generate_gcode(self.patterns), file_config.filename+".gcode")

    def optimize(self):
        pass

    @property
    def gcode_offset(self):
        return self.gcode.read_gcode_offset_from_file()
    
    @gcode_offset.setter
    def gcode_offset(self, value):
        self.gcode.save_gcode_offset_file(value)

    @property
    def gcode_offset_x(self):
        return self.gcode.read_gcode_offset_from_file()[0]
    
    @property
    def gcode_offset_y(self):
        return self.gcode.read_gcode_offset_from_file()[1]
    
    @property
    def string_length(self):
        return 0
    
    @property
    def canvas_content(self):
        return self._canvas_content
    
    @property
    def string_length(self):
        '''Returns a string containing the adjusted length in meters'''
        value = round((self.draw.string_length / 1000)*1.1, 2)
        if value:
            return f"Required string length: {value}m"
        else:
            return None
    
    def canvas_dimensions(self, dim):
        self._canvas_dim = (dim['width'], dim['height'])
        self.draw.set_canvas_dim(self._canvas_dim)