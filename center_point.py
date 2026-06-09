from shape import Shape
from models.models import ShapeConfig
from point import Point

class CenterPoint():
    def __init__(self):
        self.shape = Shape(ShapeConfig(
            num_shapes=1,
            size=100,
            hex_color="#000000",
            offset=1,
            line_points=0,
            center=Point(0,0),
            id = None,
            shape_type=None
        ))
        self._canvas_content = ''''''

    def calculate_center_points(self, num_points, canvas_point: Point):
        self.shape.config.size = 0#canvas_point.polar[1]
        self.center_points = self.shape._calculate(center=Point(0,0),
                                                    angle=canvas_point.polar[0],
                                                    num_points=num_points)
        
        print(canvas_point)
        self._canvas_content = self.draw_points([canvas_point])
        print(self._canvas_content)

    def draw_points(self, points: list[Point]):
        content = ""
        for p in points:
            content += f'''<circle cx="{p.x}" cy="{p.y}" r="1" fill="black" />'''
        return content