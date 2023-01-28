# TODO Connect circles to ends of arrows and have them rotate, stress test
# Add dtime and base stuff off of degrees/radians per second
# Test modulus for degree count
from tkinter import Tk, Canvas, Frame, BOTH
from time import monotonic
from random import randint, choice

# Local imports
from arrow_circle import ArrowCircle
from arrow_circle_list import ArrowCircleList

class Test(Frame):
    def __init__(self):
        super().__init__()
        self.arrow_circles: ArrowCircleList = ArrowCircleList()
        self.line_points: list[int] = []
        self.initUI()
    
    def initUI(self):
        self.master.title("Test")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        # self.ovalitemid = self.canvas.create_oval(15, 25, 200, 100)
        # print(self.ovalitemid)
        self.line_id = None

        self.canvas.pack(fill=BOTH, expand=1)
    
    def create_arrow_circle(self,
            circle_x: float, circle_y: float,
            circle_radius: float, arrow_dir: float, arrow_ddir: float
        ) -> int:
        arrow_circle = ArrowCircle(circle_x, circle_y, circle_radius, arrow_dir, arrow_ddir)

        circle_id = self.canvas.create_oval(arrow_circle.x0, arrow_circle.y0, arrow_circle.x1, arrow_circle.y1)
        arrow_id = self.canvas.create_line(arrow_circle.x, arrow_circle.y, arrow_circle.arrow_x1, arrow_circle.arrow_y1, arrow="last")

        arrow_circle.circle_id = circle_id
        arrow_circle.arrow_id = arrow_id

        self.arrow_circles.append(arrow_circle)
        return len(self.arrow_circles) - 1
    
    def rotate_arrow(self, index, amount):
        self.set_arrow_dir(index, self.arrow_circles[index].arrow_dir + amount)

    def update_line(self):
        if self.arrow_circles:
            self.line_points.append(self.arrow_circles[-1].arrow_x1)
            self.line_points.append(self.arrow_circles[-1].arrow_y1)
            if self.line_id is not None:
                if len(self.line_points) % 4 == 0:
                    self.canvas.coords(self.line_id, *self.line_points)
            elif len(self.line_points) >= 4:
                self.line_id = self.canvas.create_line(*self.line_points, smooth=1, fill="red")

    def set_arrow_dir(self, index, dir):
        self.arrow_circles[index].arrow_dir = dir
        self._update_arrow(index)
    
    def update_circles(self, dtime: float):
        self.arrow_circles.update_circles(dtime, self._update_circle)

    def _update_arrow(self, index):
        self.canvas.coords(self.arrow_circles[index].arrow_id, self.arrow_circles[index].x, self.arrow_circles[index].y, self.arrow_circles[index].arrow_x1, self.arrow_circles[index].arrow_y1)
        # self.canvas.delete(self.arrow_circles[index].arrow_id)
        # self._generate_arrow_at_index(index)

    def set_circle_pos(self, index, x, y):
        self.arrow_circles[index].x = x
        self.arrow_circles[index].y = y
        self._update_circle(index)
    
    def _update_circle(self, index):
        self.canvas.moveto(self.arrow_circles[index].circle_id, self.arrow_circles[index].x0, self.arrow_circles[index].y0)
        self._update_arrow(index)

    def _generate_arrow_at_index(self, index):
        arrow_circle = self.arrow_circles[index]
        arrow_id = self.canvas.create_line(arrow_circle.x, arrow_circle.y, arrow_circle.arrow_x1, arrow_circle.arrow_y1, arrow="last")
        arrow_circle.arrow_id = arrow_id
    
    # def _rotate_circle(self, index):
    #     arrow_id = self.arrow_circles[index][1]


def main():
    old_time = monotonic()
    # Time between each line point update
    line_time = 0.1
    cur_line_time = 0
    def update():
        nonlocal old_time, line_time, cur_line_time
        dtime = monotonic() - old_time
        cur_line_time += dtime
        old_time = monotonic()
        ex.update_circles(dtime)
        if cur_line_time >= line_time:
            cur_line_time = 0
            ex.update_line()
        root.after(10, update)
    root = Tk()
    
    ex = Test()
    canvas_width = 800
    canvas_height = 600
    canvas_x = int(ex.winfo_screenwidth() / 2 - canvas_width / 2)
    canvas_y = int(ex.winfo_screenheight() / 2 - canvas_height / 2)
    root.geometry(f"{canvas_width}x{canvas_height}+{canvas_x}+{canvas_y}")
    root.after(1000, update)
    x, y = canvas_width / 2, canvas_height / 2
    for i in range(60, 0, -2):
        index = ex.create_arrow_circle(x, y, i, randint(0, 359), choice([i for i in range(-359, 360, 1) if i != 0]))
        # print(ex.arrow_circles[index])
        x = ex.arrow_circles[index].arrow_x1
        y = ex.arrow_circles[index].arrow_y1
    # ex.create_arrow_circle(ex.winfo_width() / 2, ex.winfo_height() / 2, 100, 270)
    root.mainloop()

if __name__ == "__main__":
    main()