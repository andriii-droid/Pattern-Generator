from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import math


class Pattern:
    def __init__(self, filename='output', circles=False, lines=False, sketch=False):
        self.circles = circles
        self.lines = lines
        self.sketch = sketch
        self.c = canvas.Canvas(filename, pagesize=A6)
        self.width, self.height = A6
        self.center = (self.width / 2 , self.height / 2)
        self.size = 200
        self.offset = 1

        if self.circles:
            self.c.circle(*self.center, r=3, stroke=0, fill=1)

    def generate_shape(self, shape="rect", num_shapes=1,  col='#000000',  size=100, offset=1, line_points=0):
        self.col = col
        self.size = size
        self.offset = offset
        self.c.setFillColor(col)
        angle = 0
        step = 360 / num_shapes
        for _ in range(num_shapes):
            if angle == 0 and self.sketch:
                self.c.setLineWidth(1)
                self.c.setStrokeColor(colors.red)
            else:
                self.c.setLineWidth(.2)
                self.c.setStrokeColor(col)

            points = self.calc_shape(angle=angle, num_points=shape, center=self.center)
            if line_points:
                points = self.generate_points_on_shape(points=points, num_points=line_points)

            self.draw_points(points)
            self.draw_lines(points, angle, line_points)

            angle += step   

    def savePDF(self):
        self.c.showPage()
        self.c.save()

    def new_point(self, start_point, length, angle_degrees):
        x1, y1 = start_point
        
        angle_radians = math.radians(angle_degrees)
        
        dx = length * math.cos(angle_radians)
        dy = length * math.sin(angle_radians)
        
        x2 = x1 + dx
        y2 = y1 + dy
        
        return (x2, y2)
    
    def calc_shape(self, center, angle=0, num_points=1):
        points = []
        points.append(self.new_point(center, (self.size/2)*self.offset, 90+angle))
        rotation_angle = -360/num_points/2 + angle
        for _ in range(num_points - 1):
            points.append(self.new_point(points[-1], self.size*math.sin(math.pi/num_points), rotation_angle)) #TODO
            rotation_angle -= 360/num_points
        return points
    
    def generate_points_on_shape(self, points, num_points):
        """
        Generates a list of (x, y) coordinates evenly spaced between each two points in the given points list
        """
        new_points = []
        for p1, p2 in zip(points, points[1:]+[points[0]]):
            new_points.append(p1)
            for i in range(num_points+1)[1:]:
                t = i / (num_points + 1)
                x = p1[0] + t * (p2[0] - p1[0])
                y = p1[1] + t * (p2[1] - p1[1])
                new_points.append((x,y))
        return new_points

    def draw_points(self, points):
        for p1, p2 in zip(points, points[1:]+[points[0]]):
            if self.circles:
                self.c.circle(*p1, r=1, stroke=0, fill=1)

    def draw_lines(self, points, angle, offset):
        print(not offset)
        for count, (p1, p2) in enumerate(zip(points, points[offset+2:]+points[0:offset+2])):
            if self.lines or (self.sketch and angle == 0 and not (offset)) or (offset and count == 0):
                self.c.line(*p1, *p2)