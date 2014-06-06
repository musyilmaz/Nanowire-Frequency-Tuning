# Calculating theoretical nominal frequency
import numpy as np

def nominal_frequency(height, length, E, rho):
	nom_freq = (((1.0279 * height) / (length ** 2)) * np.sqrt(E / rho))
	return nom_freq
			