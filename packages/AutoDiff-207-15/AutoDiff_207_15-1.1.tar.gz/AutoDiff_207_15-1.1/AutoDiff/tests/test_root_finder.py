import pytest 
import math
import numpy as np
from AutoDiff.ad import DiffObj, Variable, VectorFunction
from AutoDiff.ad import MathOps as mo
from AutoDiff.root_finder import ThreadWithReturnValue, vectorNewton

TOL = 1e-6

class TestRootFinder():
    def test_no_roots(self):        
        c5 = 5
        c5_v = VectorFunction([c5])

        x = Variable('x')
        sin_x = mo.sin(x)
        sin_x_c5 = sin_x + c5
        sin_x_c5_v = VectorFunction([sin_x_c5])

        x_sq = x ** 2
        x_sq_c5 = x_sq + c5
        x_sq_c5_v = VectorFunction([x_sq_c5])

        vector_list = [c5_v, sin_x_c5_v, x_sq_c5_v]

        for i in range(len(vector_list)):
            vector = vector_list[i]
            print(i)
            roots = vectorNewton(vector, verbose=False)
            assert len(roots) == 0

    def test_single_root(self):
        c3 = 3
        x = Variable('x')

        x_cubed = x ** c3
        x_cubed_roots = vectorNewton(VectorFunction([x_cubed]), verbose=False, tolerance=TOL**4)
        print(x_cubed_roots)
        assert len(x_cubed_roots) == 1
        assert len(x_cubed_roots[0]) == 1
        assert abs(x_cubed_roots[0]['x'] ** 3) < TOL

        x3 = c3 * x
        x3_roots = vectorNewton(VectorFunction([x3]), verbose=False)
        assert len(x3_roots) == 1
        assert len(x3_roots[0]) == 1
        assert abs(3 * x3_roots[0]['x']) < TOL

        x9 = c3 * c3 * x
        x9_roots = vectorNewton(VectorFunction([x9]), verbose=False)
        assert len(x9_roots) == 1
        assert len(x9_roots[0]) == 1
        assert abs(9 * x9_roots[0]['x']) < TOL

    def test_multiple_roots(self):
        x = Variable('x')
        c1 = 1
        c2 = 2
        c3 = 5
        c4 = 10
        f = c3**(c1 + mo.sin(mo.log(c3 + x**c2))) - c4
        roots = vectorNewton(VectorFunction([f]), verbose=False)
        for root in roots:
            assert abs(5**(1+ np.sin(np.log(5 + root['x']**2))) - 10) < TOL
    def test_print(self):
        c3 = 3
        x = Variable('x')

        x_cubed = x ** c3
        x_cubed_roots = vectorNewton(VectorFunction([x_cubed]), verbose=True, tolerance=TOL**4)



