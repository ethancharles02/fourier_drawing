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
    def __init__(self, renderer: Renderer = None, function_analyzer = None,
                 resultant_lines: list[ResultantLine] = None, line_duration: float = 5, line_update_time: float = 0.1,
                 arrow_circle_lists: list[ArrowCircleList] = None, min_radius: float = 1) -> None:
        self.renderer = Renderer() if renderer is None else renderer
        self.function_analyzer = FunctionAnalyzer() if function_analyzer is None else function_analyzer
        
        self.line_duration = line_duration
        self.line_update_time = line_update_time
        max_line_points = self.line_duration // self.line_update_time

        self.cur_line_time = 0
        self.total_runtime = 0
        self.cur_fps_time = 0
        self.frame_count = 0
        self.fps_update_time = 5
        
        self.min_radius = min_radius

        if arrow_circle_lists is None:
            self.arrow_circle_lists = [ArrowCircleList()]
        else:
            self.arrow_circle_lists = arrow_circle_lists
        for arrow_circle_list in self.arrow_circle_lists:
            for arrow_circle in arrow_circle_list:
                arrow_circle.is_hidden_update_func = self.renderer.update_circle_hidden_state
                self.renderer.draw_arrow_circle(arrow_circle)
                if arrow_circle.radius < self.min_radius:
                    arrow_circle.is_hidden = True

        if resultant_lines is None:
            self.resultant_lines = []
            for i in range(len(self.arrow_circle_lists)):
                self.resultant_lines.append(ResultantLine(self.arrow_circle_lists[i][-1], max_line_points))
        else:
            self.resultant_lines = resultant_lines

    def update_lines(self):
        for i in range(len(self.arrow_circle_lists)):
            if self.arrow_circle_lists[i]:
                self.resultant_lines[i].update_line()
                if self.resultant_lines[i].line_id is not None:
                    if self.resultant_lines[i].has_even_number_points():
                        self.renderer.update_line(self.resultant_lines[i].line_id, self.resultant_lines[i].line_points)
                elif self.resultant_lines[i].has_valid_line():
                    self.resultant_lines[i].line_id = self.renderer.draw_line(self.resultant_lines[i].line_points)
    
    def update(self, time: float, dtime: float):
        self.total_runtime += dtime
        self.cur_fps_time += dtime
        self.frame_count += 1
        self.cur_line_time += dtime
        self.update_circles(time)
        if self.cur_line_time >= self.line_update_time:
            self.cur_line_time = 0
            self.update_lines()
        if self.cur_fps_time >= self.fps_update_time:
            print(f"FPS: {self.frame_count / self.cur_fps_time}")
            self.cur_fps_time = 0
            self.frame_count = 0

    def update_circles(self, time: float = 0):
        for arrow_circle_list in self.arrow_circle_lists:
            arrow_circle_list.update_circles(time, self.renderer.update_circle)