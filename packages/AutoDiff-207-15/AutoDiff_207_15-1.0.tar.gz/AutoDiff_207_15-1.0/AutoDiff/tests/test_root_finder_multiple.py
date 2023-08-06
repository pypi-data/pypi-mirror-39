import pytest 
import math
import numpy as np
from AutoDiff.ad import DiffObj, Variable, VectorFunction
from AutoDiff.ad import MathOps as mo
from AutoDiff.root_finder import ThreadWithReturnValue, vectorNewton
from AutoDiff.root_finder_multiple import root_finder_multiple
TOL=0.1

class TestRootFinder_multi():
    def test_no_roots(self):        
        x = Variable('x') 
        y = Variable('y')
        z = Variable('z')
        f_1 = (x-1)**2*(x-2)*2
        f_2 = (x-3)**3*(x-4)*4
        f_3 = (x-5)**3*(x-5)*4
        roots=root_finder_multiple([f_1,f_2,f_3])
        assert(len(roots)==0)

    def test_single_root(self):
        x = Variable('x') 
        y = Variable('y')
        z = Variable('z')
        f_1 = (x-1)**2*(x-2)*2
        f_2 = (x-2)**3*(x-4)*4
        f_3 = (x-5)**3*(x-2)*4
        roots=root_finder_multiple([f_1,f_2,f_3])
        assert(len(roots)==1)
        assert(abs(roots[0]-2)<TOL)

    def test_multiple_roots(self):
        x = Variable('x') 
        y = Variable('y')
        z = Variable('z')
        f_1 = (x-1)**3*(x-2)
        f_2 = (x-1)**4*(x-2)
        f_3 = (x-1)**5*(x-2)
        roots=root_finder_multiple([f_1,f_2,f_3])
        assert(len(roots)==2)
        assert((((abs(roots[0]-2)<TOL) and (abs(roots[1]-1)<TOL)) or ((abs(roots[0]-1)<TOL) and (abs(roots[1]-2)<TOL))))