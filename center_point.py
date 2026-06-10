from point import Point

class CenterPoint():
    def __init__(self, coordinator):
        self._canvas_content = ''''''
        self.coordinator = coordinator
        self._center_points = []
        self._canvas_width_in_mm = 105
        self._canvas_height_in_mm = 148
        self._scale_factor = 1


    def calculate_center_points(self, num_points, canvas_point: Point):
        self._center_points = self.calc_shape(canvas_point, num_points)
        
        self._canvas_content = self.draw_points(self._center_points)

    def calc_shape(self, startpoint: Point, num_points):
        points = []
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
    
    def set_canvas_dim(self, dim):
        self._scale_factor = dim[0] / self._canvas_width_in_mm
    
    @property
    def center_points(self):
        if len(self._center_points) == 0:
            self._center_points.append(Point(0,0))
        print(self._center_points)
        return [point / self._scale_factor for point in self._center_points]