from arrow_circle import ArrowCircle
from typing import Callable

class ArrowCircleList(list[ArrowCircle]):
    def __init__(self, arrow_circle_list: list[ArrowCircle] = []):
        super().__init__(arrow_circle_list)
        # self._arrow_circle_list = arrow_circle_list
        self.update_circles()
    
    def __setitem__(self, index, item):
        super().__setitem__(index, item)
        self.update_circles()

    # def update_circles(self, lambda_func: Callable[[ArrowCircle], None] = None):
    def update_circles(self, dtime: float = 0, post_update_lambda_func: Callable[[int], None] = None):
        if self:
            # self[0].update(dtime)
            # if post_update_lambda_func is not None:
            #     post_update_lambda_func(0)
            # iterator = iter(self)
            # next(iterator)
            for i, arrow_circle in enumerate(self, -1):
                # print(i, arrow_circle)
                if i != -1:
                    arrow_circle.x = self[i].arrow_x1
                    arrow_circle.y = self[i].arrow_y1
                arrow_circle.update(dtime)
                if post_update_lambda_func is not None:
                    post_update_lambda_func(i + 1)