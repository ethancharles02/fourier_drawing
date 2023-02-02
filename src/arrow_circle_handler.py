# TODO Docstring
from typing import Callable
from math import pi
from cmath import polar

# Local imports
from .arrow_circle import ArrowCircle
from .arrow_circle_list import ArrowCircleList
from .resultant_line import ResultantLine
from .renderer import Renderer
from .function_analyzer import FunctionAnalyzer


class ArrowCircleHandler:
    def __init__(self, renderer: Renderer = None, function_analyzer = None, resultant_line: ResultantLine = None, line_duration: float = 5, line_update_time: float = 0.1,
            arrow_circle_list: ArrowCircleList = None, num_arrow_circle_pairs: int = 1, arrow_circle_x: int = 0, arrow_circle_y: int = 0, speed_multiplier: float = 1, drawing_func: Callable = None) -> None:
        self.renderer = Renderer() if renderer is None else renderer
        self.function_analyzer = FunctionAnalyzer() if function_analyzer is None else function_analyzer
        
        self.line_duration = line_duration
        self.line_update_time = line_update_time
        max_line_points = self.line_duration // self.line_update_time

        self.cur_line_time = 0

        if arrow_circle_list is None:
            self.create_arrow_circle_list(drawing_func, num_arrow_circle_pairs, arrow_circle_x, arrow_circle_y, speed_multiplier)
        else:
            self.arrow_circles = arrow_circle_list

        if resultant_line is None:
            self.resultant_line = ResultantLine(self.arrow_circles[-1], max_line_points)
        else:
            self.resultant_line = resultant_line
    
    def create_arrow_circle_list(self, drawing_func: Callable, num_arrow_circle_pairs: int, arrow_circle_x: int, arrow_circle_y: int, speed_multiplier: float):
        self.arrow_circles = ArrowCircleList()
        n = 0
        a = 0
        b = 1
        radius, direction = polar(self.function_analyzer.get_complex_constant(drawing_func, n, a, b))
        self.create_arrow_circle(x=arrow_circle_x, y=arrow_circle_y, arrow_ddir=0, radius=radius, arrow_dir=direction)

        for n in range(1, num_arrow_circle_pairs + 1):
            radius, direction = polar(self.function_analyzer.get_complex_constant(drawing_func, n, a, b))
            self.create_arrow_circle(arrow_ddir=2*pi*speed_multiplier*n, radius=radius, arrow_dir=direction)

            radius, direction = polar(self.function_analyzer.get_complex_constant(drawing_func, -n, a, b))
            self.create_arrow_circle(arrow_ddir=2*pi*speed_multiplier*-n, radius=radius, arrow_dir=direction)

        self.arrow_circles.update_circles()

    def update_line(self):
        if self.arrow_circles:
            self.resultant_line.update_line()
            if self.resultant_line.line_id is not None:
                if self.resultant_line.has_even_number_points():
                    self.renderer.update_line(self.resultant_line.line_id, self.resultant_line.line_points)
            elif self.resultant_line.has_valid_line():
                self.resultant_line.line_id = self.renderer.draw_line(self.resultant_line.line_points)

    def create_arrow_circle(self, **kwargs) -> int:
        arrow_circle = ArrowCircle(**kwargs)
        self.renderer.draw_arrow_circle(arrow_circle)
        self.arrow_circles.append(arrow_circle)
        return len(self.arrow_circles) - 1
    
    def update(self, dtime: float):
        self.cur_line_time += dtime
        self.update_circles(dtime)
        if self.cur_line_time >= self.line_update_time:
            self.cur_line_time = 0
            self.update_line()

    def update_circles(self, dtime: float):
        self.arrow_circles.update_circles(dtime, self.renderer._update_circle)