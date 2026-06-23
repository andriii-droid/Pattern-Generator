from dataclasses import dataclass
from point import Point

@dataclass
class CenterConfig:
    '''Data contract for centerpoints'''
    center_points: list[Point]
    center_offset: bool

@dataclass
class FileConfig:
    '''Data contract for Filesettings'''
    filename: str
    gcode_offset_x: float
    gcode_offset_y: float
    
@dataclass
class LineConfig:
    """Datacontract for Lines between patterns"""
    pat_id: list[int]
    offset: int

@dataclass
class DrawingConfig:
    '''Data contract for drawing settings'''
    draw_points: bool
    draw_lines: bool
    draw_sketch: bool
    line_configs: list[LineConfig]


@dataclass
class ShapeConfig:
    """Data contract for shapes"""
    shape_type: int
    num_shapes: int
    size: float
    hex_color: str
    offset: float
    line_points: int
    center: Point
    id: int
    center_points: list[int]

@dataclass
class SplineConfig:
    """Data contract for complex spline tracks."""
    num_points: int
    start_point: Point
    control_point: Point
    end_point: Point
    center: Point
    id: int
    center_points: int

@dataclass
class PatternConfig:
    """Data contract for patterns."""
    patterns: list[SplineConfig | ShapeConfig]

