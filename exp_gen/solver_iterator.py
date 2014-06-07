# Generating Solver List with inputs 
# Deriving 1st mode frequency based on the step size
import numpy as np

def solver_iterator(Loop, X_value, Y_value):

	# Solver ===> Decision mechanism list
	# It should be empty for each tuning step
	Solver = []

	for omega in Loop: 
	
		# Determining kN, k_value and l_value 
		# Required for det(a) = 0 verification equation which is Solver list
		kN = omega * Y_value
		k_value = np.sqrt((np.sqrt(X_value + (kN ** 2))) + X_value)
		l_value = np.sqrt((np.sqrt(X_value + (kN ** 2))) - X_value)

		# det(a) = 0 verification
		Solv = (np.cosh(k_value) * np.cos(l_value)) - ((X_value / kN) * 
			np.sinh(k_value) * np.sin(l_value))

		Solver.append(Solv)

		# Deriving 1st mode frequency based on Solver
		for i, j in zip(Solver, Solver[1:]):
			if i <= 1 and j > 1:
				axial_load_frequency = omega / (2 * np.pi)
				return axial_load_frequency
				break
			elif i >= 1 and j < 1:
				axial_load_frequency = omega / (2 * np.pi)
				return axial_load_frequency
				break




	