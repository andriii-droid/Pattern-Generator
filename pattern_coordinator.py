from models.models import PatternConfig, DrawingConfig, FileConfig, CenterConfig, ShapeConfig, SplineConfig, LineConfig, CenterConfig
from point import Point
from shape import Shape
from spline import Spline
from gcode import GCODE
from draw import Draw
from pdf import PDF
from nicegui import ui
from center_point import CenterPoint



class PatternCoordinator():
    '''exposes functions to the dashboard manipulate patterns '''
    def __init__(self):
        self.patterns: list[Shape | Spline] = []
        self.gcode = GCODE(self)
        self.draw = Draw()
        self.pdf = PDF()
        self.center = CenterPoint()
        self.define_center = False

        self._canvas_content = ''''''

    def calculate_and_render(self, pattern_config: PatternConfig, 
                             drawing_config: DrawingConfig, 
                             center_config: CenterConfig,
                             ):
        '''checks input values and calculates and then draws the patterns to the ui'''
        try:
            if not len(pattern_config.patterns):
                raise ValueError("Define at least one pattern")
            
            self._check_line_config(drawing_config.line_configs)

            self._calculate(pattern_config=pattern_config, center_config=center_config)
        except Exception as e:
            ui.notify(e, type="negative")
        self._render_to_ui(drawing_config=drawing_config)



    def _calculate(self, pattern_config: PatternConfig, 
                   center_config: CenterConfig):
        '''calculates the specified patterns and stores the patterns'''
        self.patterns = []

        #for each center point create one pattern
        for cp in center_config.center_points:
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
        self.draw._string_length = 0
        if drawing_config.draw_points: #Draws Points if configured
            for pat in self.patterns:
                self._canvas_content += self.draw.draw_points(pat)

        for pat in self.patterns:
            if not pat.config.id in [pat_id for config in drawing_config.line_configs for pat_id in config.pat_id]:
                self._canvas_content += self.draw.draw_lines(drawing_config, pat)
        
        line_combinations = []
        for id_pair in drawing_config.line_configs:
            for pat in self.patterns:
                if pat.config.id == id_pair.pat_id[0]:
                    xpat = pat
                elif pat.config.id == id_pair.pat_id[1]:
                    ypat = pat
            if len(xpat.points) != len(ypat.points):
                self._canvas_content = ""
                raise ValueError("The patterns must have the same number of points!")
            line_combinations.append((xpat, ypat))

        for line_com, config in zip(line_combinations, drawing_config.line_configs):
            self._canvas_content += self.draw.draw_lines_between_patterns(*line_com, config)

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

    def handle_center(self, args, num_points):
        '''generates centerpoints according to the mouse location'''
        if not self.define_center:
            return
        
        point = Point(args[0] - self.canvas_dimensions[0]/2,
                      args[1] - self.canvas_dimensions[1]/2)        

        self.center.calculate_center_points(num_points=int(num_points), canvas_point=point)

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
    def canvas_content(self):
        return self._canvas_content
    
    @property
    def canvas_dimensions(self):
        return self._canvas_dim
    
    @property
    def string_length(self):
        '''Returns a string containing the adjusted length in meters'''
        value = round((self.draw.string_length / 1000)*1.1, 2)
        if value:
            return f"Required string length: {value}m"
        else:
            return None
    
    def set_canvas_dimensions(self, dim):
        self._canvas_dim = (dim['width'], dim['height'])
        self.draw.set_canvas_dim(self._canvas_dim)

    def _check_line_config(self, config_list: list[LineConfig]):
        id_list = [pat_id for config in config_list for pat_id in config.pat_id]
        if len(id_list) != 2 * len(config_list):
            raise ValueError("Always two patterns for line config needed")
        seen = set()
        for item in id_list:
            if item in seen:
                raise ValueError(f"Pattern {item} is defined more than once!")
            else:
                seen.add(item)
