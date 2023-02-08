# TODO cleanup and docstrings
from typing import Callable

# Local imports
from .arrow_circle import ArrowCircle

class ArrowCircleList(list[ArrowCircle]):
    def __init__(self, arrow_circle_list: list[ArrowCircle] = []):
        super().__init__(arrow_circle_list)
        self.update_circles()
    
    def __setitem__(self, index, item):
        super().__setitem__(index, item)
        self.update_circles()

    def update_circles(self, time: float = 0, post_update_lambda_func: Callable[[int], None] = None):
        if self:
            for i, arrow_circle in enumerate(self, -1):
                if i != -1:
                    arrow_circle.x = self[i].arrow_x1
                    arrow_circle.y = self[i].arrow_y1
                arrow_circle.update(time)
                if post_update_lambda_func is not None:
                    post_update_lambda_func(arrow_circle)