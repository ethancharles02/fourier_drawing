"""Module for the ArrowCircle"""

from math import sin, cos
from typing import Callable

class ArrowCircle:
    """The ArrowCircle holds information on a circle which has one arrow in it"""
    
    def __init__(self, x: int = 0, y: int = 0, radius: float = 0, arrow_dir: float = 0, arrow_ddir: float = 0, circle_id: int = None, arrow_id: int = None, is_hidden_update_func: Callable = None):
        """Init method

        Keyword Arguments:
            x {int} -- X position representing the center of the circle (default: {0})
            y {int} -- Y position representing the center of the circle (default: {0})
            radius {int} -- Radius of the circle (default: {0})
            arrow_dir {int} -- Initial arrow direction in radians (default: {0})
            arrow_ddir {int} -- Directional velocity in radians (default: {0})
            circle_id {int} -- ID of the circle as assigned by the renderer (default: {None})
            arrow_id {int} -- ID of the arrow as assigned by the renderer (default: {None})
            is_hidden_update_func {Callable} -- Function to run when the hidden attribute is changed (default: {None})
        """
        self.x0 = 0
        """{int} -- Left x for the circle, should not be edited. Changed through the x and radius attributes"""
        self.x1 = 0
        """{int} -- Right x for the circle, should not be edited. Changed through the x and radius attributes"""
        self.y0 = 0
        """{int} -- Top y for the circle, should not be edited. Changed through the y and radius attributes"""
        self.y1 = 0
        """{int} -- Bottom y for the circle, should not be edited. Changed through the y and radius attributes"""
        self.arrow_x1 = 0
        """{int} -- End x position of the arrow, should not be edited. Changed through the x, radius, and arrow_dir attributes"""
        self.arrow_y1 = 0
        """{int} -- End y position of the arrow, should not be edited. Changed through the y, radius, and arrow_dir attributes"""

        self._x = 0
        self._y = 0

        self._radius = None

        self._arrow_dir = 0

        self.circle_id = circle_id
        self.arrow_id = arrow_id

        self.radius = radius
        self.initial_dir = arrow_dir
        self.arrow_dir = arrow_dir
        self.arrow_ddir = arrow_ddir

        self._is_hidden = False
        self.is_hidden_update_func = is_hidden_update_func
        """Update function that gets run when the is_hidden attribute is changed"""
        
        self.x = x
        self.y = y

    def update(self, time: float):
        """Updates the direction of the arrow

        Arguments:
            time {float} -- Absolute time in seconds to update the arrow to
        """
        if self.arrow_ddir != 0:
            self.arrow_dir = self.initial_dir + self.arrow_ddir * time

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self._update_xy()

    @property
    def is_hidden(self):
        return self._is_hidden
    @is_hidden.setter
    def is_hidden(self, value):
        self._is_hidden = value
        if self.is_hidden_update_func is not None:
            self.is_hidden_update_func(self)
        
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        self._update_x()

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        self._update_y()

    @property
    def arrow_dir(self):
        return self._arrow_dir
    @arrow_dir.setter
    def arrow_dir(self, value):
        self._arrow_dir = value
        self._update_arrow_xy()

    def _update_x(self):
        self.x0 = self.x - self.radius
        self.x1 = self.x + self.radius
        self._update_arrow_x()

    def _update_y(self):
        self.y0 = self.y - self.radius
        self.y1 = self.y + self.radius
        self._update_arrow_y()

    def _update_xy(self):
        self._update_x()
        self._update_y()
    
    def _update_arrow_x(self):
        self.arrow_x1 = self.x + self.radius * cos(self.arrow_dir)

    def _update_arrow_y(self):
        self.arrow_y1 = self.y + self.radius * -sin(self.arrow_dir)

    def _update_arrow_xy(self):
        self._update_arrow_x()
        self._update_arrow_y()

if __name__ == "__main__":
    test_arrow_circle = ArrowCircle(0, 0, 10, 0, 0, 0)
    print(f"{test_arrow_circle.x1=}, {test_arrow_circle.y1=}, {test_arrow_circle.arrow_x1=}, {test_arrow_circle.arrow_y1=}")