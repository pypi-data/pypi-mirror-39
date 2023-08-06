from AutoDiff.ad import DiffObj, Variable, VectorFunction
from AutoDiff.ad import MathOps as mo
import random
import numpy as np
import math
from AutoDiff import root_finder

TOL=0.1

# add on denoise for single root finder
def denoise_root_finder(f):
	roots=[item[f.name_list[0]] for item in root_finder.vectorNewton(VectorFunction([f]), verbose=False)]
	real_root=[]
	for i in roots:
		if len(real_root)==0:
			real_root.append(i)
		else:
			count=0
			for j in real_root:
				if abs(i-j)<TOL:
					count+=1
			if count==0:
				real_root.append(i)
	return real_root

def root_finder_multiple(list_of_f):
	final_list=[]
	root_list=[denoise_root_finder(f) for f in list_of_f]
	# print(root_list)
	for candidates in root_list[0]:
		count=0
		for compare_group in root_list[1:]:
			for compare_item in compare_group:
				if abs(compare_item-candidates)<TOL:
					count+=1
					break
		if count==len(list_of_f)-1:
			final_list.append(candidates)
	return final_list

# quasi newton method

if __name__=='__main__':
	x = Variable('x') 
	y = Variable('y')
	z = Variable('z')
	f_1 = (x-1)**3*(x-2)
	f_2 = (x-1)**4*(x-2)
	f_3 = (x-1)**5*(x-2)
	# print(root_finder.vectorNewton(VectorFunction([f_1]), verbose=False))
	roots=root_finder_multiple([f_1,f_2,f_3])
	print(roots)
	# assert(len(roots)==2)
 	# assert((((abs(roots[0]-2)<TOL) and (abs(roots[1]-3)<TOL)) or ((abs(roots[0]-3)<TOL) and (abs(roots[1]-2)<TOL))))