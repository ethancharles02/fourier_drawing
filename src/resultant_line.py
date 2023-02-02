# TODO Docstring
from .arrow_circle import ArrowCircle

class ResultantLine:
    def __init__(self, tracking_arrow_circle: ArrowCircle, max_line_points: int, line_id: int = None, line_points: list[int] = []):
        self.tracking_arrow_circle = tracking_arrow_circle
        self.max_line_points = max_line_points
        self.line_id = line_id
        self.line_points = line_points
    
    def update_line(self):
        self.line_points.append(self.tracking_arrow_circle.arrow_x1)
        self.line_points.append(self.tracking_arrow_circle.arrow_y1)
        if len(self.line_points) >= self.max_line_points:
            self.line_points.pop(0)
            self.line_points.pop(0)
    
    def has_even_number_points(self):
        return len(self.line_points) % 4 == 0
    
    def has_valid_line(self):
        return len(self.line_points) >= 4 and self.has_even_number_points()