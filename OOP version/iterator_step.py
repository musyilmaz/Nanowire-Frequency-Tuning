# Determining iterator step for the axial load frequency iteratior
import numpy as np

def iterator_step(freq, iteration_count, length_order):
	
	if iteration_count == 0: 
		
		# iteration_count == 0 means that 1st iteration
		# Determining iteration values based on bao frequency
		step = 10.0 ** length_order
		
		# Determining order of the bao frequency 
		num_dig = np.floor(np.log10(freq))

		# Determining the iteration start value for the system
		iter_start = ((10 ** num_dig) * np.floor(freq / 
			(10 ** num_dig))) 
		iter_finish = (iter_start + 0.9 * (10 ** num_dig)) +  ((length_order - 2) * 100 * step)
		
		return step, iter_start, iter_finish
	
	else:
		
		# iteration_count > 0 means that further iterations
		# Determining step size with iteration count
		step = 10.0 ** (length_order - iteration_count)

		# Determining order of the frequency
		num_dig = np.floor(np.log10(freq))

		# Determining the iteration start value for the system
		iter_start = ((10 ** (num_dig - iteration_count)) * 
			np.floor(freq / (10 ** (num_dig - iteration_count)))) - ((length_order - 2) * 100 * step)
		iter_finish = (iter_start + (10 ** (num_dig - iteration_count))) + ((length_order - 2) * 100 * step)

		return step, iter_start, iter_finish

