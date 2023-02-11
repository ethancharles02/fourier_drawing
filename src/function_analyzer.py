"""Module for the FunctionAnalyzer"""

import numpy
import quadpy
from typing import Callable

class FunctionAnalyzer:
    """The function analyzer is used for integrating complex functions for the
    sake of getting the complex constant for the drawing function.
    """
    def quad(self, func: Callable[[float], complex], a: float, b: float, **kwargs):
        """Integrate a function from a to b

        Arguments:
            func {Callable[[float], complex]} -- Function that may return complex numbers
            a {float} -- Start number
            b {float} -- End number

        Returns:
            complex -- Possibly complex number
        """
        return quadpy.c1.integrate_adaptive(func, [a, b], **kwargs)

    def function_factory(self, drawing_func: Callable[[float], complex], n: int):
        """Generates a function where the given n of the arrow circle has a
        halted direction velocity

        Arguments:
            drawing_func {Callable[[float], complex]} -- Function that may return complex numbers
            n {int} -- Index of the arrow circle (can be negative)
        
        Returns:
            Callable[[x], y] -- New function
        """
        def function(x):
            return drawing_func(x) * numpy.exp(-n*2*numpy.pi*1j*x)
        return function

    def get_complex_constant(self, drawing_func: Callable[[float], complex], n: int, a: float = 0, b: float = 1):
        """Gets the complex constant of a given drawing function
        
        This number represents the radius and initial direction of the arrow circle.
        For instance, a complex constant of (1 + 2i) indicates that the arrow circle
        should be pointing at the coordinates (1, 2) if the center of the circle
        is (0, 0). Running cmath.polar will extract the radius and direction

        Arguments:
            drawing_func {Callable[[float], complex]} -- Function that may return complex numbers
            n {int} -- Index of the given arrow circle

        Keyword Arguments:
            a {float} -- Start position of the integral (default: {0})
            b {float} -- End position of the integral (default: {1})

        Returns:
            complex -- Complex constant
        """
        return self.quad(self.function_factory(drawing_func, n), a, b)[0]