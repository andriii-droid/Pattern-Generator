from shape import Shape
from models.models import ShapeConfig
from point import Point

class CenterPoint():
    def __init__(self, coordinator):
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
        self.coordinator = coordinator

    def calculate_center_points(self, num_points, canvas_point: Point):
        print(canvas_point)
        self.shape.config.size = canvas_point.polar[1]
        self.center_points = self.shape._calculate(center=Point(0,0),   #Todo function does not map first point to the canvas point like i wanted
                                                    angle=canvas_point.polar[0],
                                                    num_points=num_points)
        
        print(self.center_points)
        self._canvas_content = self.draw_points(self.center_points)
        print(self._canvas_content)

    def draw_points(self, points: list[Point]):
        content = ""
        for p in points:
            x = p.x + self.coordinator.canvas_dimensions[0]/2
            y = p.y + self.coordinator.canvas_dimensions[1]/2
            content += f'''<circle cx="{x}" cy="{y}" r="1" fill="black" />'''
        return content