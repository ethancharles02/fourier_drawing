from math import sin, cos, radians

class ArrowCircle:
    def __init__(self, x, y, radius, arrow_dir, arrow_ddir, circle_id=None, arrow_id=None):
        self.x0 = 0
        self.x1 = 0
        self.y0 = 0
        self.y1 = 0
        self.arrow_x1 = 0
        self.arrow_y1 = 0

        self._x = 0
        self._y = 0

        self._radius = None

        self._arrow_dir = 0

        self.circle_id = circle_id
        self.arrow_id = arrow_id

        self.radius = radius
        self.arrow_dir = arrow_dir
        self.arrow_ddir = arrow_ddir

        self.x = x
        self.y = y

    def update(self, dtime: float):
        self.arrow_dir += self.arrow_ddir * dtime

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self._update_xy()

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        self._update_x()

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        self._update_y()

    @property
    def arrow_dir(self):
        return self._arrow_dir
    @arrow_dir.setter
    def arrow_dir(self, value):
        self._arrow_dir = value
        self._update_arrow_xy()

    def _update_x(self):
        self.x0 = self.x - self.radius
        self.x1 = self.x + self.radius
        self._update_arrow_x()

    def _update_y(self):
        self.y0 = self.y - self.radius
        self.y1 = self.y + self.radius
        self._update_arrow_y()

    def _update_xy(self):
        self._update_x()
        self._update_y()
    
    def _update_arrow_x(self):
        self.arrow_x1 = self.x + self.radius * cos(radians(self.arrow_dir))

    def _update_arrow_y(self):
        self.arrow_y1 = self.y + self.radius * -sin(radians(self.arrow_dir))

    def _update_arrow_xy(self):
        self._update_arrow_x()
        self._update_arrow_y()

if __name__ == "__main__":
    test_arrow_circle = ArrowCircle(0, 0, 10, 0, 0, 0)
    print(f"{test_arrow_circle.x1=}, {test_arrow_circle.y1=}, {test_arrow_circle.arrow_x1=}, {test_arrow_circle.arrow_y1=}")