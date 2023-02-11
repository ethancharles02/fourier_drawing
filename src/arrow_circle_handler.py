"""Module for the ArrowCircleHandler which interfaces between arrow circles and the renderer"""
from math import isclose

# Local imports
from .arrow_circle_list import ArrowCircleList
from .resultant_line import ResultantLine
from .renderer import Renderer

class ArrowCircleHandler:
    """Interfaces between arrow circles and the renderer"""
    
    def __init__(self, renderer: Renderer = None, resultant_lines: list[ResultantLine] = None,
                 line_duration: float = 5, line_update_time: float = 0.1,
                 arrow_circle_lists: list[ArrowCircleList] = None, min_radius: float = 1, optimize: bool = True) -> None:
        """Init method

        Keyword Arguments:
            renderer {Renderer} -- Class which draws out the circles and lines on screen (default: {None})
            resultant_lines {list[ResultantLine]} -- Lines which draw out the results of the arrow circles (default: {None})
            line_duration {float} -- How long each segment of a line persists in seconds (default: {5})
            line_update_time {float} -- Time between each update for a line in seconds (default: {0.1})
            arrow_circle_lists {list[ArrowCircleList]} -- List of ArrowCircleList objects (default: {None})
            min_radius {float} -- Minimum radius that will render the arrow circle on the screen in pixels (default: {1})
            optimize {bool} -- Optimizes the arrow circle lists. From minimal testing, this has no impact on quality (default: {True})
        """
        self.renderer = Renderer() if renderer is None else renderer
        
        self.line_duration = line_duration
        self.line_update_time = line_update_time
        # Finds number of points that correspond to the given duration
        # This makes the assumption that the line update time is absolute
        # In the event that frames take too long to produce and the line
        #   update time isn't closely followed, the actual duration will be longer
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
            
        if optimize:
            self._optimize_arrow_circle_lists()
            
        for arrow_circle_list in self.arrow_circle_lists:
            for arrow_circle in arrow_circle_list:
                # Assigns renderer specific functions and draws the initial arrow circles to the screen
                arrow_circle.is_hidden_update_func = self.renderer.update_circle_hidden_state
                self.renderer.draw_arrow_circle(arrow_circle)
                # Hides circles that are too small (this only hides them from drawing, math is still done with them)
                if arrow_circle.radius < self.min_radius:
                    arrow_circle.is_hidden = True

        # Assigns resultant lines such that they follow the very last arrow circle in each list
        if resultant_lines is None:
            self.resultant_lines = []
            for i in range(len(self.arrow_circle_lists)):
                self.resultant_lines.append(ResultantLine(self.arrow_circle_lists[i][-1], max_line_points))
        else:
            self.resultant_lines = resultant_lines

    def update_lines(self):
        """Updates the points in resultant lines and renders the updated lines"""
        for line in self.resultant_lines:
            line.update_line()
            self.renderer.draw_line(line)
    
    def update(self, time: float, dtime: float):
        """Updates all circles and lines based on a given time and a change in time

        Arguments:
            time {float} -- Absolute time in seconds
            dtime {float} -- Change in time from last frame in seconds
        """
        self.total_runtime += dtime
        self.cur_fps_time += dtime
        self.frame_count += 1
        self.cur_line_time += dtime
        self.update_circles(time)
        # TODO A better way of implementing these timer like statements would be optimal
        # maybe setting the expected update time in the future and comparing against that
        # (ie. current time is 1, update needs to happen in one second, set expected to 2 and check for that)
        if self.cur_line_time >= self.line_update_time:
            self.cur_line_time = 0
            self.update_lines()
        if self.cur_fps_time >= self.fps_update_time:
            print(f"FPS: {self.frame_count / self.cur_fps_time}")
            self.cur_fps_time = 0
            self.frame_count = 0

    def update_circles(self, time: float = 0):
        """Updates each circle in the list

        Keyword Arguments:
            time {float} -- Absolute time (default: {0})
        """
        for arrow_circle_list in self.arrow_circle_lists:
            arrow_circle_list.update_circles(time, self.renderer.draw_arrow_circle)
    
    def _optimize_arrow_circle_lists(self):
        # Optimizes by iterating backwards in the list and removing any arrow circles within the tolerance given
        for arrow_circle_list in self.arrow_circle_lists:
            for i in range(len(arrow_circle_list) - 1, -1, -1):
                if isclose(arrow_circle_list[i].radius, 0, abs_tol=1e-10):
                    arrow_circle_list.pop(i)