from models.models import PatternConfig, DrawingConfig, ShapeConfig, SplineConfig
from point import Point


class Draw():
    def __init__(self):
        pass

    def draw_points(self, points: list[Point]):
        content = ""
        for p in points:
            content += f'''<circle cx="{0}" cy="{0}" r="1" fill="black" />'''
        return content