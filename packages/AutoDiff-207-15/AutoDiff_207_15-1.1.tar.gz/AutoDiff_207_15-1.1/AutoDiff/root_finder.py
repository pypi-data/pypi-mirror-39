import AutoDiff.ad as ad
from threading import Thread
import random
import numpy as np
import math
import logging


# create a thread object that returns the thread results
# adapted from kindall on stackoverflow
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=()):
        Thread.__init__(self, group, target, name, args)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

# multi-dimensional Newton's method
def vectorNewton(input_function,tolerance=1e-5, num_starting_vals = 20, 
	starting_val_range = (-1000,1000), starting_val_dict_list=None, verbose=True):

	logger = logging.getLogger()

	# initialize our list
	if not starting_val_dict_list:
		starting_val_dict_list = []

	# find one root 
	def find_root(vf,starting_val_dict, max_iter,tol):
		val_dict = starting_val_dict

		error_list = []
		fx = vf.get_val(val_dict)
		it = 0
		all_dim_dist = math.inf

		# if we haven't done too many iterations and we're still greater than our tolerance 
		while it < max_iter and all_dim_dist > tol:
			it += 1

			try:
				abs_fx = abs(fx)
			except:
				abs_fx = [abs(val) for val in fx]

			all_dim_dist = np.linalg.norm([fx],ord=2)

			# make a list of errors so we can check Newton's method is working
			error_list += [np.sum(abs_fx)]

			# get jacobian, move to new point
			try:
				dx = vf.dict_list_to_array(vf.get_der(val_dict))

				# need to update all new values of value dictionary
				try:
					delta = np.linalg.solve(np.array(dx),-1*np.array(fx))
				except Exception as e:
					print(e) 

				# update dictionary
				for i,val in enumerate(vf.name_list):
					val_dict[val] = val_dict[val] + delta[i]
				new_fx = vf.get_val(val_dict)
				fx = new_fx

			# avoid dividing by zero 
			except:
				logger.warning("Tried to divide by zero!")
				return
		return_dict = {}
		for var in vf.name_list:
			return_dict[var] = val_dict[var]
		return (return_dict, vf.get_val(val_dict), len(error_list), error_list)

	# function takes value and list, returns true if value is within diff_tol of any value
	# in the list, false otherwise.
	def is_close_vector_lists(v,lst,diff_tol=1e-2):
		for ele in lst:
			for val in list(ele.keys()):
				l = [abs(v[val]-ele[val]) for i in range(len(v))]
			if np.sum(l)<diff_tol:
				return True
		return False

	
	
	# if user doesn't input a vector function, change type here for
	if not isinstance(input_function,ad.VectorFunction):
		input_function = ad.VectorFunction([input_function])

	# check if function is a constant or one component is a constant
	try:
		for f in input_function.list_of_functions:
			if isinstance(f,int):
				return []
	except:
		return []



	# adjust starting value list to agree with number of requested starting values 
	while len(starting_val_dict_list)<num_starting_vals:
		starting_val_dict_to_add = {}
		for var in input_function.name_list:
			starting_val_dict_to_add[var] = random.randint(starting_val_range[0],starting_val_range[1])
		starting_val_dict_list.append(starting_val_dict_to_add)

	max_iter = 100 # maybe user should be able to choose this? 
	results = []
	roots = []

	# check that we can actually perform Newtons-- same number of equations as 
	# variables 

	if len(input_function.name_list) > len(input_function.list_of_functions):
		raise TypeError("Cannot find a root if the number of variables is more than vector dimensions. Please specify values for {} variable(s) and try again.".format(
			len(input_function.name_list)-len(input_function.list_of_functions)))

	# start threads 
	threads = []
	for i in range(len(starting_val_dict_list)):
		thread = ThreadWithReturnValue(target=find_root, 
			args=(input_function,starting_val_dict_list[i],max_iter,tolerance))
		thread.start()
		threads.append(thread)
	for i in range(len(starting_val_dict_list)):
		full_result = threads[i].join()

		# if didn't catch exception in find_root 
		if full_result:
			root_result = full_result[0]

			is_zero = True
			for output in full_result[1]:
				if abs(output) > tolerance:
					is_zero = False

			# check if root already in list 
			if not (is_close_vector_lists(root_result, roots)) and is_zero:
				roots.append(root_result)
				results.append(full_result)

	# for testing, choose verbose 
	if verbose:
		return results
	else:
		return roots


