"""Module for the ArrowCircleList which is the singular data unit used for rendering"""

from typing import Callable
from cmath import polar
from math import pi

# Local imports
from .arrow_circle import ArrowCircle
from .function_analyzer import FunctionAnalyzer

class ArrowCircleList(list[ArrowCircle]):
    """List Class which holds data on ArrowCircle objects"""
    # Class for integrating complex functions
    function_analyzer = FunctionAnalyzer()
    
    def __init__(self, arrow_circle_list: list[ArrowCircle] = [], cycle_time: float = 1):
        """Init method

        Keyword Arguments:
            arrow_circle_list {list[ArrowCircle]} -- List of ArrowCircle objects (default: {[]})
            cycle_time {float} -- How long it takes for a cycle to complete in seconds (default: {1})
        """
        super().__init__(arrow_circle_list)
        self.cycle_time = cycle_time
        self.speed_multiplier = self.cycle_time ** -1
        # Updates the circles only to attach them end to end
        self.update_circles()
    
    def __setitem__(self, index, item):
        super().__setitem__(index, item)
        self.update_circles()

    def update_circles(self, time: float = None, post_update_lambda_func: Callable[[ArrowCircle], None] = None):
        """Updates circles by rotating them to the given time and attaching them end to end

        Keyword Arguments:
            time {float} -- Absolute time (default: {None})
            post_update_lambda_func {Callable[[ArrowCircle], None]} -- Function to run at the end of the update, generally a rendering function to update the circles on screen (default: {None})
        """
        if self:
            if time is not None:
                time = time % self.cycle_time
            # Enumerates such that i represents the index of the previous arrow circle
            for i, arrow_circle in enumerate(self, -1):
                if i != -1:
                    arrow_circle.x = self[i].arrow_x1
                    arrow_circle.y = self[i].arrow_y1
                if time is not None:
                    arrow_circle.update(time)
                if post_update_lambda_func is not None:
                    post_update_lambda_func(arrow_circle)
    
    @classmethod
    def generate(cls, drawing_func: Callable[[float], float], a: int = 0, b: int = 1,
                 num_arrow_circle_pairs: int = 1, arrow_circle_x: int = 0, arrow_circle_y: int = 0,
                 cycle_time: float = 1):
        """Generates the list of arrow circles from a drawing function

        Arguments:
            drawing_func {Callable[[float], float]} -- Drawing function where the input represents the time in seconds and the output is coordinates in the complex plane (real is x and imaginary is y)

        Keyword Arguments:
            a {int} -- Start time (default: {0})
            b {int} -- End time (default: {1})
            num_arrow_circle_pairs {int} -- Number of pairs, the actual number of arrow circles is number of pairs * 2 + 1, ie. 2 pairs results in 5 arrow circles (default: {1})
            arrow_circle_x {int} -- X position of the center of the circle (default: {0})
            arrow_circle_y {int} -- Y position of the center of the circle (default: {0})
            cycle_time {float} -- How long it takes to finish a cycle in seconds (default: {1})

        Returns:
            ArrowCircleList
        """
        arrow_circles = cls(cycle_time=cycle_time)
        speed_multiplier = arrow_circles.speed_multiplier
        n = 0
        a = 0
        b = 1
        # The complex constant is a complex number which represents the radius and initial direction of the arrow circle
        radius, direction = polar(cls.function_analyzer.get_complex_constant(drawing_func, n, a, b))
        arrow_circles.append(ArrowCircle(x=arrow_circle_x, y=arrow_circle_y, arrow_ddir=0, radius=radius, arrow_dir=direction))

        for n in range(1, num_arrow_circle_pairs + 1):
            radius, direction = polar(cls.function_analyzer.get_complex_constant(drawing_func, n, a, b))
            arrow_circles.append(ArrowCircle(arrow_ddir=2*pi*speed_multiplier*n, radius=radius, arrow_dir=direction))

            radius, direction = polar(cls.function_analyzer.get_complex_constant(drawing_func, -n, a, b))
            arrow_circles.append(ArrowCircle(arrow_ddir=2*pi*speed_multiplier*-n, radius=radius, arrow_dir=direction))

        arrow_circles.update_circles()
        return arrow_circles