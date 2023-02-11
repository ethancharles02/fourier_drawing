"""Module for the ResultantLine"""

from .arrow_circle import ArrowCircle

class ResultantLine:
    """The resultant line represents the line drawn out from an arrow circle"""
    
    def __init__(self, tracking_arrow_circle: ArrowCircle, max_line_points: int, line_id: int = None, line_points: list[int] = None):
        """Init method

        Arguments:
            tracking_arrow_circle {ArrowCircle} -- The arrow circle to track, this is used to update the lines points with update_line
            max_line_points {int} -- Maximum number of points before it starts to remove the oldest points

        Keyword Arguments:
            line_id {int} -- ID of the line for use by the renderer (default: {None})
            line_points {list[int]} -- List of points, ie. [1, 2, 3, 4] where (1, 2) and (3, 4) are points (default: {None})
        """
        self.tracking_arrow_circle = tracking_arrow_circle
        self.max_line_points = int(max_line_points + (4 - max_line_points % 4))
        self.line_id = line_id
        self.line_points = line_points if line_points is not None else []
    
    def update_line(self):
        """Updates the line with the tracked circles points"""
        self.line_points.append(self.tracking_arrow_circle.arrow_x1)
        self.line_points.append(self.tracking_arrow_circle.arrow_y1)
        if len(self.line_points) >= self.max_line_points:
            for _ in range(4):
                self.line_points.pop(0)
    
    def has_even_number_points(self):
        return len(self.line_points) % 4 == 0
    
    def has_valid_line(self):
        return len(self.line_points) >= 4 and self.has_even_number_points()