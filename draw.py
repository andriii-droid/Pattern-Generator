from models.models import PatternConfig, DrawingConfig, ShapeConfig, SplineConfig
from point import Point
from shape import Shape
from spline import Spline

class Draw():
    def __init__(self):
        self._canvas_width_in_mm = 105
        self._canvas_height_in_mm = 148
        self._control_point = Point(self._canvas_width_in_mm / 2, self._canvas_height_in_mm / 2)
        self._scale_factor = 1
        self._canvas_content = ''''''
        self._string_length = 0

    def set_canvas_dim(self, dim):
        self._scale_factor = dim[0] / self._canvas_width_in_mm

    def draw_points(self, pat: Shape | Spline):
        content = ""
        for i, p in enumerate(pat.points):
            if i == 0:
                col = "red"
            else: col = "black"
            x = (p.x + self._control_point.x) * self._scale_factor
            y = (p.y + self._control_point.y) * self._scale_factor
            content += f'''<circle cx="{x}" cy="{y}" r="1" fill="{col}" />'''
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
            self.draw_shape_lines(pat, sketch=True)
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
                self._string_length += p1.distance(p2)
                p1 = (p1 + self._control_point) * self._scale_factor
                p2 = (p2 + self._control_point)  * self._scale_factor
                self._canvas_content += f'''<line x1="{p1.x}" y1="{p1.y}" 
                x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{col}" stroke-width="{stroke_width}" />'''
    
    def draw_lines_between_line_points(self, shape: Shape, sketch=False):
        '''draws lines between linepoints'''
        if sketch:
            col = "#ff0000"
            stroke_width = 0.8
            points_list = shape.sketch_points
        else:
            col = shape.config.hex_color
            stroke_width = 0.2
            points_list = shape.points
        
        shape_points_list = self._split_list(points_list, shape.config.num_shapes) #needs to be used, when multiple Num_shapes is greater then 1 with linepoints is defined
        for points in shape_points_list:
            for (p1, p2) in zip(points, points[shape.config.line_points+2:]+points[0:shape.config.line_points+2]):
                self._string_length += p1.distance(p2)
                p1 = (p1 + self._control_point) * self._scale_factor
                p2 = (p2 + self._control_point)  * self._scale_factor
                self._canvas_content += f'''<line x1="{p1.x}" y1="{p1.y}" 
                x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{col}" stroke-width="{stroke_width}" />'''

    def draw_lines_between_patterns(self, xpat: Shape | Spline, ypat: Shape | Spline, config):
        self._canvas_content = ''''''
        if isinstance(xpat, Spline) and isinstance(ypat, Spline):
            self.draw_lines_between_splines(xpat, ypat)
        elif isinstance(xpat, Shape) and isinstance(ypat, Shape):
            self.draw_lines_between_shapes(xpat, ypat, config)

        return self._canvas_content  
    
    def draw_lines_between_splines(self, xspline: Spline, yspline: Spline, sketch=False):
        if sketch:
            col = "#ff0000"
            stroke_width = 0.8
            xpat_points = xspline.sketch_points
            ypat_points = yspline.sketch_points
        else:
            # col = xpat.config.hex_color TODO
            col = "#000000"
            stroke_width = 0.2
            xpat_points = xspline.points
            ypat_points = yspline.points

        for (p1, p2) in zip(xpat_points, ypat_points[::-1]):
            p1 = (p1 + self._control_point) * self._scale_factor
            p2 = (p2 + self._control_point)  * self._scale_factor
            self._canvas_content += f'''<line x1="{p1.x}" y1="{p1.y}" 
            x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{col}" stroke-width="{stroke_width}" />'''  

    def draw_lines_between_shapes(self, xshape: Shape, yshape: Shape, config, sketch=False):
        if sketch:
            col = "#ff0000"
            stroke_width = 0.8
            xpat_points = xshape.sketch_points #TODO
            ypat_points = yshape.sketch_points
        else:
            # col = xpat.config.hex_color TODO
            col = "#000000"
            stroke_width = 0.2
            xpat_points = xshape.points_along_circle
            ypat_points = yshape.points_along_circle

        for (p1, p2) in zip(xpat_points, ypat_points[config.offset:]+ypat_points[:config.offset]):
            p1 = (p1 + self._control_point) * self._scale_factor
            p2 = (p2 + self._control_point)  * self._scale_factor
            self._canvas_content += f'''<line x1="{p1.x}" y1="{p1.y}" 
            x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{col}" stroke-width="{stroke_width}" />'''  

        for (p1, p2) in zip(xpat_points, ypat_points[-config.offset:]+ypat_points[:-config.offset]):
            p1 = (p1 + self._control_point) * self._scale_factor
            p2 = (p2 + self._control_point)  * self._scale_factor
            self._canvas_content += f'''<line x1="{p1.x}" y1="{p1.y}" 
            x2="{p2.x}" y2="{p2.y}" fill="none" stroke="{col}" stroke-width="{stroke_width}" />'''  
            
    def draw_cords(self):  
        '''draws the coordinatesystem onto the canvas'''
        p = (Point(0,0) + self._control_point) * self._scale_factor
        content = f'''<circle cx="{p.x}" cy="{p.y}" r="{40 * self._scale_factor}" fill="none" stroke="#000000" stroke-width=".1" />'''
        content += f'''<circle cx="{p.x}" cy="{p.y}" r="{15 * self._scale_factor}" fill="none" stroke="#000000" stroke-width=".1" />'''
        content += f'''<line x1="{0}" y1="{p.y}" x2="{p.x*2}" y2="{p.y}" fill="none" stroke="#000000" stroke-width=".1" />'''
        content += f'''<line x1="{p.x}" y1="{0}" x2="{p.x}" y2="{p.y*2}" fill="none" stroke="#000000" stroke-width=".1" />'''
        return content
    
    def _split_list(self, lst, num):
        '''split a list evenly into num lists'''
        k, m = divmod(len(lst), num)
        return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(num)]
    
    @property
    def string_length(self):
        '''returns string length in mm'''
        return self._string_length

if __name__ == '__main__':
    draw = Draw()
    print(draw._split_list([1,1,1,1], 1))