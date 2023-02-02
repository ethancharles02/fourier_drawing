# TODO Docstrings
import numpy
import quadpy

class FunctionAnalyzer:
    def __init__(self):
        pass
    
    def quad(self, func, a, b, **kwargs):
        return quadpy.c1.integrate_adaptive(func, [a, b], **kwargs)

    def function_factory(self, drawing_func, n):
        def test_func(x):
            return drawing_func(x) * numpy.exp(-n*2*numpy.pi*1j*x)
        return test_func

    def get_complex_constant(self, drawing_func, n, a=0, b=1):
        return self.quad(self.function_factory(drawing_func, n), a, b)[0]