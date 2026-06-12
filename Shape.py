import math
from point import Point
from models.models import ShapeConfig
import numpy as np


class Shape():
    '''generetes N-Ecks'''
    def __init__(self, config: ShapeConfig):
        self.config = config
        self._points: list[Point] = []

    def generate(self):
        '''calls the _calculate function with specified number of corners, a specified number of times with an angle offset'''  
        self._points = []
        for angle in np.linspace(0, 360, (self.config.num_shapes * self.config.shape_type), endpoint=False):
            self._points.append(Point.from_polar(angle, self.config.size))
    
    def _generate_points_on_shape(self, points, num_points):
        """
        Generates a list of Point objects evenly spaced between each two points in the given points list
        """
        new_points = []
        for p1, p2 in zip(points, points[1:]+[points[0]]):
            new_points.append(p1)
            for i in range(num_points+1)[1:]:
                t = i / (num_points + 1)
                x1, y1 = p1.cartesian
                x2, y2 = p2.cartesian
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                new_points.append(Point(x,y))
        return new_points
    
    def _new_point(self, start_point, length, angle_degrees):
        '''calculates a new Point with a given startpoint lenght and and angle in degrees'''
        x1, y1 = start_point.cartesian
        
        angle_radians = math.radians(angle_degrees)
        
        dx = length * math.cos(angle_radians)
        dy = length * math.sin(angle_radians)
        
        x2 = x1 + dx
        y2 = y1 + dy
        
        return Point(x2, y2)
    
    @property
    def points(self):
        rearranged_list = []
        for i in range(self.config.num_shapes):
            rearranged_list.extend(self._points[i::self.config.num_shapes])     
        return rearranged_list
    
    @property
    def sketch_points(self):
        if self.config.line_points:
            return [self._points[0]] + [self._points[self.config.line_points+2]]
        else:
            return self._points[0:self.config.shape_type]
        
    @property
    def points_along_circle(self):
        return self._points