# Calculating theoretical bao frequency
import numpy as np
import constants as co

def bao_frequency(nom_freq, load, length, I):
	bao_freq = nom_freq * np.sqrt(1 + 
		(0.2949 * ((load * length ** 2) / (12 * co.E * I))))
	return bao_freq
