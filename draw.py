from models.models import PatternConfig, DrawingConfig, ShapeConfig, SplineConfig
from point import Point


class Draw():
    def __init__(self):
        self._canvas_width_in_mm = 105
        self._canvas_height_in_mm = 148
        self._scale_factor = 1

    def set_canvas_dim(self, dim):
        self._scale_factor = dim[0] / self._canvas_width_in_mm

    def draw_points(self, points: list[Point]):
        content = ""
        for p in points:
            content += f'''<circle cx="{p.x*self._scale_factor}" cy="{p.y*self._scale_factor}" r="1" fill="black" />'''
        return content