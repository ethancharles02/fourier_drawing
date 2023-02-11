"""Module for the Renderer and Window"""

from tkinter import Tk, Canvas, Frame, BOTH
from time import monotonic
from typing import Callable

# Local imports
from .arrow_circle import ArrowCircle
from .resultant_line import ResultantLine

class Renderer(Frame):
    """The Renderer is used to draw arrow circles to the screen"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.master.title("Fourier Series Drawing")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

    def draw_arrow_circle(self, arrow_circle: ArrowCircle):
        """Draws an arrow circle to the screen. Assign the IDs for the drawn
        arrow and circle if they haven't been assigned yet, otherwise it uses
        the IDs to update the circle

        Arguments:
            arrow_circle {ArrowCircle} -- Arrow circle to draw or update
        """
        if arrow_circle.circle_id is None:
            arrow_circle.circle_id = self.canvas.create_oval(arrow_circle.x0, arrow_circle.y0, arrow_circle.x1, arrow_circle.y1)
        else:
            if not arrow_circle.is_hidden:
                self._update_circle(arrow_circle)
                
        if arrow_circle.arrow_id is None:
            arrow_circle.arrow_id = self.canvas.create_line(arrow_circle.x, arrow_circle.y, arrow_circle.arrow_x1, arrow_circle.arrow_y1, arrow="last")
        else:
            if not arrow_circle.is_hidden:
                self._update_arrow(arrow_circle)

    def _update_circle(self, arrow_circle: ArrowCircle):
        self.canvas.moveto(arrow_circle.circle_id, arrow_circle.x0, arrow_circle.y0)
    def _update_arrow(self, arrow_circle: ArrowCircle):
        self.canvas.coords(arrow_circle.arrow_id, arrow_circle.x, arrow_circle.y, arrow_circle.arrow_x1, arrow_circle.arrow_y1)
    
    def draw_line(self, resultant_line: ResultantLine, **kwargs):
        """Draws a line to the screen, also assigns an ID to the resultant line if
        it isn't already assigned, otherwise it updates the line

        Arguments:
            resultant_line {ResultantLine} -- Line object
        """
        if resultant_line.line_id is None:
            if resultant_line.has_valid_line():
                resultant_line.line_id = self.canvas.create_line(*resultant_line.line_points, **kwargs, smooth=1, fill="red")
        else:
            if resultant_line.has_even_number_points():
                self._update_line(resultant_line)

    def _update_line(self, resultant_line: ResultantLine):
        self.canvas.coords(resultant_line.line_id, *resultant_line.line_points)

    def update_circle_hidden_state(self, arrow_circle: ArrowCircle):
        """Updates the state of the drawn arrow circle based on its attribute

        Arguments:
            arrow_circle {ArrowCircle} -- Arrow circle object
        """
        self.canvas.itemconfigure(arrow_circle.circle_id, state="hidden" if arrow_circle.is_hidden else "normal")
        self.canvas.itemconfigure(arrow_circle.arrow_id, state="hidden" if arrow_circle.is_hidden else "normal")     


class Window:
    """Creates a window to draw to and update"""
    
    def __init__(self, renderer: Renderer, update_func: Callable = None, canvas_width: int = 800, canvas_height: int = 600, update_delay_ms: float = 0):
        """Init Method

        Arguments:
            renderer {Renderer} -- Renderer object

        Keyword Arguments:
            update_func {Callable} -- Function to run on each update frame (default: {None})
            canvas_width {int} -- Width of the canvas (default: {800})
            canvas_height {int} -- Height of the canvas (default: {600})
            update_delay_ms {float} -- Delay for each update (may be longer since the update function can take time to complete) (default: {0})
        """
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
        """Starts the main update loop"""
        self.root.mainloop()

    def update(self):
        """Update function to run with each update"""
        time = monotonic()
        dtime = time - self.old_time
        self.old_time = time
        if self.update_func is not None:
            self.update_func(time - self.start_time, dtime)
        self.root.after(self.update_delay, self.update)