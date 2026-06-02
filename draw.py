from models.models import PatternConfig, DrawingConfig, ShapeConfig, SplineConfig
from point import Point
from shape import Shape
from spline import Spline

class Draw():
    def __init__(self):
        self._canvas_width_in_mm = 105
        self._canvas_height_in_mm = 148
        self._center_point = Point(self._canvas_width_in_mm / 2, self._canvas_height_in_mm / 2)
        self._scale_factor = 1
        self._canvas_content = ''''''

    def set_canvas_dim(self, dim):
        self._scale_factor = dim[0] / self._canvas_width_in_mm

    def draw_points(self, pat: Shape | Spline):
        content = ""
        for p in pat.points:
            x = (p.x + self._center_point.x) * self._scale_factor
            y = (p.y + self._center_point.y) * self._scale_factor
            content += f'''<circle cx="{x}" cy="{y}" r="1" fill="black" />'''
        return content
    
    def draw_lines(self, drawing_config: DrawingConfig, pat: Shape | Spline):
        '''calls correct line drawing functions'''
        self._canvas_content = ''''''

        #Draw Lines
        if not drawing_config.draw_lines:
            pass
        elif isinstance(pat, Spline):
            pass
        elif isinstance(pat, Shape) and not pat.config.line_points:
            self.draw_shape_lines(pat)
        elif isinstance(pat, Shape) and pat.config.line_points:
            self.draw_lines_between_line_points(pat)

        #Draw Sketch Lines
        if not drawing_config.draw_sketch:
            pass
        elif isinstance(pat, Spline):
            pass
        elif isinstance(pat, Shape) and not pat.config.line_points:
            self.draw_shape_lines(pat, sketch=True)
        elif isinstance(pat, Shape) and pat.config.line_points:
            self.draw_shape_lines(pat,  sketch=True)
        return self._canvas_content

    
    def draw_shape_lines(self, shape: Shape, sketch=False):
        '''draws the lines between edges of generated shapes'''
        if sketch:
            col = "#ff0000"
            stroke_width = 0.8
            points = shape.sketch_points
        else:
            col = shape.config.hex_color
            stroke_width = 0.2
            points = shape.points

        point_lists = [points[i:i + shape.config.shape_type] for i in range(0, len(points), shape.config.shape_type)]
        for point_shape in point_lists:
            for (p1, p2) in zip(point_shape, point_shape[1:]+[point_shape[0]]):
                p1 = (p1 + self._center_point) * self._scale_factor
                p2 = (p2 + self._center_point)  * self._scale_factor
                self._canvas_content += f'''<line x1="{p1.x}" y1="{p1.y}" 
                x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{col}" stroke-width="{stroke_width}" />'''
    
    def draw_lines_between_line_points(self, shape: Shape, sketch=False):
        '''draws lines between linepoints'''
        if sketch:
            col = "#ff0000"
            stroke_width = 0.8
            points = shape.sketch_points
        else:
            col = shape.config.hex_color
            stroke_width = 0.2
            points = shape.points

        for (p1, p2) in zip(points, points[shape.config.line_points+2:]+points[0:shape.config.line_points+2]):
            p1 = (p1 + self._center_point) * self._scale_factor
            p2 = (p2 + self._center_point)  * self._scale_factor
            self._canvas_content += f'''<line x1="{p1.x}" y1="{p1.y}" 
            x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{col}" stroke-width="{stroke_width}" />'''

    def draw_cords(self):  
        '''draws the coordinatesystem onto the canvas'''
        p = (Point(0,0) + self._center_point) * self._scale_factor
        content = f'''<circle cx="{p.x}" cy="{p.y}" r="{40 * self._scale_factor}" fill="none" stroke="#000000" stroke-width=".1" />'''
        content += f'''<circle cx="{p.x}" cy="{p.y}" r="{15 * self._scale_factor}" fill="none" stroke="#000000" stroke-width=".1" />'''
        content += f'''<line x1="{0}" y1="{p.y}" x2="{p.x*2}" y2="{p.y}" fill="none" stroke="#000000" stroke-width=".1" />'''
        content += f'''<line x1="{p.x}" y1="{0}" x2="{p.x}" y2="{p.y*2}" fill="none" stroke="#000000" stroke-width=".1" />'''
        return content
