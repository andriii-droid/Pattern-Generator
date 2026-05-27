from models.models import PatternConfig, DrawingConfig, FileConfig, SettingsConfig, ShapeConfig, SplineConfig
from point import Point
from shape import Shape
from spline import Spline
from gcode import GCODE

class PatternCoordinator():
    '''exposes functions to the dashboard manipulate patterns '''
    def __init__(self):
        self.patterns: list[Shape | Spline] = []
        self.gcode = GCODE()

    def calculate_and_render(self, pattern_config: PatternConfig, 
                             drawing_config: DrawingConfig, 
                             settings_config: SettingsConfig):
        '''calculates and then draws the patterns to the ui'''
        self._calculate(pattern_config=pattern_config, settings_config=settings_config)
        self._render_to_ui(drawing_config=drawing_config, pattern_config=pattern_config)

    def _calculate(self, pattern_config: PatternConfig, 
                   settings_config: SettingsConfig):
        '''calculates the specified patterns and stores the patterns'''
        self.patterns = []

        #create center points
        c = Shape(ShapeConfig(
            shape_type=int(settings_config.num_center_points),
            num_shapes=1,
            size=float(settings_config.center_point_radius*2),
            hex_color="", #hex is wrong config
            offset=1,
            line_points=0,
            center=Point(0,0) 
            ))
        c.generate()
        [center_points] = c.points

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
                

    def _render_to_ui(self, drawing_config: DrawingConfig, 
                      pattern_config: PatternConfig):
        '''draws points and lines to the ui'''
        print(self.patterns)

    def export_to_pdf(self, file_config: FileConfig):
        pass

    def export_to_gcode(self, file_config: FileConfig):
        pass

    def optimize(self):
        pass

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
        return '''
                    <line x1="50" y1="50" x2="250" y2="50" stroke="red" stroke-width="4" />

                    <path d="M 50,200 C 100,100 200,300 300,200" fill="transparent" stroke="blue" stroke-width="4" />

                    <circle cx="50" cy="200" r="6" fill="black" />
                    <circle cx="100" cy="100" r="6" fill="green" />
                    <circle cx="200" cy="300" r="6" fill="green" />
                    <circle cx="300" cy="200" r="6" fill="black" />
                '''