# TODO cleanup and docstrings
from typing import Callable
from cmath import polar
from math import pi

# Local imports
from .arrow_circle import ArrowCircle
from .function_analyzer import FunctionAnalyzer

class ArrowCircleList(list[ArrowCircle]):
    function_analyzer = FunctionAnalyzer()
    
    def __init__(self, arrow_circle_list: list[ArrowCircle] = [], cycle_time: float = 1):
        super().__init__(arrow_circle_list)
        self.cycle_time = cycle_time
        self.speed_multiplier = self.cycle_time ** -1
        self.update_circles()
    
    def __setitem__(self, index, item):
        super().__setitem__(index, item)
        self.update_circles()

    def update_circles(self, time: float = 0, post_update_lambda_func: Callable[[int], None] = None):
        if self:
            time = time % self.cycle_time
            for i, arrow_circle in enumerate(self, -1):
                if i != -1:
                    arrow_circle.x = self[i].arrow_x1
                    arrow_circle.y = self[i].arrow_y1
                arrow_circle.update(time)
                if post_update_lambda_func is not None:
                    post_update_lambda_func(arrow_circle)
    
    @classmethod
    def generate(cls, drawing_func: Callable[[float], float], a: int = 0, b: int = 1,
                 num_arrow_circle_pairs: int = 1, arrow_circle_x: int = 0, arrow_circle_y: int = 0,
                 cycle_time: float = 1):
        arrow_circles = cls(cycle_time=cycle_time)
        speed_multiplier = arrow_circles.speed_multiplier
        n = 0
        a = 0
        b = 1
        radius, direction = polar(cls.function_analyzer.get_complex_constant(drawing_func, n, a, b))
        arrow_circles.append(ArrowCircle(x=arrow_circle_x, y=arrow_circle_y, arrow_ddir=0, radius=radius, arrow_dir=direction))

        for n in range(1, num_arrow_circle_pairs + 1):
            radius, direction = polar(cls.function_analyzer.get_complex_constant(drawing_func, n, a, b))
            arrow_circles.append(ArrowCircle(arrow_ddir=2*pi*speed_multiplier*n, radius=radius, arrow_dir=direction))

            radius, direction = polar(cls.function_analyzer.get_complex_constant(drawing_func, -n, a, b))
            arrow_circles.append(ArrowCircle(arrow_ddir=2*pi*speed_multiplier*-n, radius=radius, arrow_dir=direction))

        arrow_circles.update_circles()
        return arrow_circles