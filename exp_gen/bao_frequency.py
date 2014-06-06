# Calculating theoretical axial loaded frequency (bao formulation)
import numpy as np

bao_gamma = 0.2949
def bao_frequency(nom_freq, axial_load, length, E, I):
	bao_freq = (nom_freq * np.sqrt(1 + (bao_gamma * 
							((axial_load * length ** 2) / (12 * E * I)))))
	return bao_freq
			