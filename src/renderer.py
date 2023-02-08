# TODO Docstring, only update a circle if it actually got changed

from tkinter import Tk, Canvas, Frame, BOTH
from time import monotonic

# Local imports
from .arrow_circle import ArrowCircle

class Renderer(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.master.title("Fourier Series Drawing")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

    def draw_arrow_circle(self, arrow_circle: ArrowCircle):
        circle_id = self.canvas.create_oval(arrow_circle.x0, arrow_circle.y0, arrow_circle.x1, arrow_circle.y1)
        arrow_id = self.canvas.create_line(arrow_circle.x, arrow_circle.y, arrow_circle.arrow_x1, arrow_circle.arrow_y1, arrow="last")

        arrow_circle.circle_id = circle_id
        arrow_circle.arrow_id = arrow_id

    def draw_line(self, line_points, **kwargs):
        return self.canvas.create_line(*line_points, **kwargs, smooth=1, fill="red")
    
    def update_line(self, line_id, line_points):
        self.canvas.coords(line_id, *line_points)

    def update_arrow(self, arrow_circle: ArrowCircle):
        self.canvas.coords(arrow_circle.arrow_id, arrow_circle.x, arrow_circle.y, arrow_circle.arrow_x1, arrow_circle.arrow_y1)
    
    def update_circle_hidden_state(self, arrow_circle: ArrowCircle):
        if arrow_circle.is_hidden:
            self.canvas.itemconfigure(arrow_circle.circle_id, state="hidden")
            self.canvas.itemconfigure(arrow_circle.arrow_id, state="hidden")
        else:
            self.canvas.itemconfigure(arrow_circle.circle_id, state="normal")
            self.canvas.itemconfigure(arrow_circle.arrow_id, state="normal")
    
    def update_circle(self, arrow_circle: ArrowCircle):
        if not arrow_circle.is_hidden:
            self.canvas.moveto(arrow_circle.circle_id, arrow_circle.x0, arrow_circle.y0)
            self.update_arrow(arrow_circle)


class Window:
    def __init__(self, renderer, update_func=None, canvas_width=800, canvas_height=600, update_delay_ms=0):
        self.old_time = monotonic()
        self.start_time = self.old_time
        self.update_delay = update_delay_ms
        self.root = Tk()
        self.update_func = update_func
        
        self.renderer = renderer()

        canvas_width = canvas_width
        canvas_height = canvas_height
        canvas_x = int(self.renderer.winfo_screenwidth() / 2 - canvas_width / 2)
        canvas_y = int(self.renderer.winfo_screenheight() / 2 - canvas_height / 2)
        self.root.geometry(f"{canvas_width}x{canvas_height}+{canvas_x}+{canvas_y}")

        self.root.after(self.update_delay, self.update)

    def mainloop(self):
        self.root.mainloop()

    def update(self):
        time = monotonic()
        dtime = time - self.old_time
        self.old_time = time
        if self.update_func is not None:
            self.update_func(time - self.start_time, dtime)
        self.root.after(self.update_delay, self.update)