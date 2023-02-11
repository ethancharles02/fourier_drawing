# TODO Stress test different integration options
# Find out how to analyze images and get the contours, preferably as bezier curves
# Try moving the rendering to a different module (manim)
# Draw out the expected shape from a list of points? or use the drawing function directly with marching squares
# Add comments to code
from src.renderer import Renderer, Window
from src.arrow_circle_handler import ArrowCircleHandler
from src.arrow_circle_list import ArrowCircleList

import numpy
def drawing_func(x):
    # return numpy.array([complex(-300*num, 0) for num in x])
    # points = numpy.array((0 + 100j, 60 + 80j, 50 - 60j, -50 - 60j, -60 + 80j))
    points = numpy.array((150 + 100j, 150 - 100j, -50 - 100j, -50 + 100j))
    # points = numpy.array((150 + 100j, 150 - 100j, -50 - 100j))
    # points = numpy.array((100 + 100j, -50j, 50j))
    num_points = len(points)
    point_multiplier = x * num_points
    remainder = (point_multiplier) % 1
    selection = (numpy.floor(point_multiplier).astype(int) + 1) % num_points
    return (points[selection] - points[selection - 1]) * remainder + points[selection - 1]
    # return numpy.exp(2*numpy.pi*1j*x) * 100 + 100
    # return x*100 + (numpy.array([complex(0, num**2) for num in x]))*100

def drawing_func2(x):
    # return numpy.array([complex(-300*num, 0) for num in x])
    # points = numpy.array((150 + 100j, -50 + 100j, -50 - 100j))
    points = numpy.array((0 + 100j, 60 + 80j, 50 - 60j, -50 - 60j, -60 + 80j))
    # points = numpy.array((150 + 100j, 150 - 100j, -50 - 100j, -50 + 100j))
    # points = numpy.array((100 + 100j, -50j, 50j))
    num_points = len(points)
    point_multiplier = x * num_points
    remainder = (point_multiplier) % 1
    selection = (numpy.floor(point_multiplier).astype(int) + 1) % num_points
    return (points[selection] - points[selection - 1]) * remainder + points[selection - 1]
    # return numpy.exp(2*numpy.pi*1j*x) * 100 + 100
    # return x*100 + (numpy.array([complex(0, num**2) for num in x]))*100

def main():
    canvas_width, canvas_height = 800, 600
    middle_x, middle_y = canvas_width / 2, canvas_height / 2

    window = Window(renderer=Renderer, canvas_width=canvas_width, canvas_height=canvas_height, update_delay_ms=1)
    
    cycle_time = 10
    # arrow_circle_lists = []
    # for i in range(10):
        # arrow_circle_lists.append(ArrowCircleList.generate(drawing_func=drawing_func, num_arrow_circle_pairs=20, arrow_circle_x=i * 50, arrow_circle_y=middle_y, cycle_time=cycle_time))
    arrow_circle_lists = [ArrowCircleList.generate(drawing_func=drawing_func, num_arrow_circle_pairs=20, arrow_circle_x=middle_x, arrow_circle_y=middle_y, cycle_time=cycle_time),
                          ArrowCircleList.generate(drawing_func=drawing_func2, num_arrow_circle_pairs=20, arrow_circle_x=middle_x, arrow_circle_y=middle_y, cycle_time=cycle_time)]
    # arrow_circle_lists = [ArrowCircleList.generate(drawing_func=drawing_func, num_arrow_circle_pairs=20, arrow_circle_x=middle_x, arrow_circle_y=middle_y, cycle_time=cycle_time)]
    arrow_circle_handler = ArrowCircleHandler(
        renderer=window.renderer, arrow_circle_lists=arrow_circle_lists,
        line_duration=5, line_update_time=0.01, min_radius=1, optimize=True)
    
    window.update_func = arrow_circle_handler.update
    window.mainloop()

if __name__ == "__main__":
    main()