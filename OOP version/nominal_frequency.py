# Calculating theoretical nominal frequency
import numpy as np
import constants as co

def nominal_frequency(length, height):
	nom_freq = (((1.0279 * height) / (length ** 2)) * np.sqrt(co.E / co.rho))
	return nom_freq
			