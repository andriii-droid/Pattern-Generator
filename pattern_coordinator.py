from models.models import PatternConfig
from point import Point

class PatternCoordinator():
    def __init__(self):
        #initialize pattern classes
        #and file classes etc
        pass

    def calculate_and_render(self, config: PatternConfig):
        pass

    def _calculate(self, config: PatternConfig):
        pass

    def _render_to_ui(self):
        pass

    def export_to_pdf(self):
        pass

    def export_to_gcode(self):
        pass

    def optimize(self):
        pass

    @property
    def gcode_offset_x(self):
        return 0

    @property
    def gcode_offset_y(self):
        return 0
    
    @property
    def string_length(self):
        return 0