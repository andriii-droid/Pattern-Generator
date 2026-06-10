from point import Point

class CenterPoint():
    def __init__(self, coordinator):
        self._canvas_content = ''''''
        self.coordinator = coordinator
        self.center_points = []

    def calculate_center_points(self, num_points, canvas_point: Point):
        self.center_points = self.calc_shape(canvas_point, num_points)
        
        self._canvas_content = self.draw_points(self.center_points)

    def calc_shape(self, startpoint: Point, num_points):
        points = []
        points.append(startpoint)
        dist = startpoint.polar[1]
        angle_start = startpoint.polar[0]
        for angle in range(0, 360, int(360 / num_points)):
            points.append(Point.from_polar(distance=dist, angle_degrees=angle + angle_start))
        return points
        
    def draw_points(self, points: list[Point]):
        content = ""
        for p in points:
            x = p.x + self.coordinator.canvas_dimensions[0]/2
            y = p.y + self.coordinator.canvas_dimensions[1]/2
            content += f'''<circle cx="{x}" cy="{y}" r="1" fill="black" />'''
        return content