from models.models import PatternConfig, DrawingConfig, ShapeConfig, SplineConfig
from point import Point


class Draw():
    def __init__(self):
        self._canvas_width_in_mm = 105
        self._canvas_height_in_mm = 148
        self._center_point = Point(self._canvas_width_in_mm / 2, self._canvas_height_in_mm / 2)
        self._scale_factor = 1

    def set_canvas_dim(self, dim):
        self._scale_factor = dim[0] / self._canvas_width_in_mm

    def draw_points(self, points: list[Point]):
        content = ""
        for p in points:
            x = p.x + self._center_point.x
            y = p.y + self._center_point.y
            content += f'''<circle cx="{x*self._scale_factor}" cy="{y*self._scale_factor}" r="1" fill="black" />'''
        return content