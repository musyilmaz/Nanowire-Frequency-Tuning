import constants as co
import exp_array_creator as eac
import math
import numpy as np
import csv
import time


now = time.time()
# Iterating for each element

exp_count = [] 
length_array = []
width_array = []
height_array = []
gap_array = []
bias_array = []
stress_array = []
axial_load = []
nominal_freq = []
bao_freq = []

exp_num = 0
steps = [1e6]


for length in np.nditer(eac.length_array):
	for width in np.nditer(eac.width_array):
		for height in np.nditer(eac.height_array):
			for gap in np.nditer(eac.gap_array):
				for bias in np.nditer(eac.bias_array):
					for stress in np.nditer(eac.stress_array):

						exp_num += 1
						exp_count.append(exp_num)

						length_array.append(length)
						width_array.append(width)
						height_array.append(height)
						gap_array.append(gap)
						bias_array.append(bias)
						stress_array.append(stress)

						# Axial load calc. and appender
						cs_area = height * width
						load = stress * cs_area
						axial_load.append(load)

						I = (width * (height ** 3)) / 12
						
						# Nominal frequency calc. and appender
						nom_freq = (((1.0279 * height) / (length ** 2)) * 
							math.sqrt(co.E / co.rho))
						nominal_freq.append(nom_freq)

						bao_freq_calc = (nom_freq * math.sqrt(1 + (co.bao_gamma * 
							((load * length ** 2) / (12 * co.E * I)))))
						bao_freq.append(bao_freq_calc)

						## Mahmut's integration approach from now on
						Num_Dig = np.ceil(math.log10(abs(bao_freq_calc)))
						
						Lstart = (10 ** (Num_Dig - 1) * 
							np.floor(bao_freq_calc / (10 ** (Num_Dig - 1))))

						Lfinish = Lstart + (0.99999999 * (10 ** (Num_Dig - 1)))

						for step in steps:
							X_freq = (load * (length ** 2)) / (2 * co.E * I)
							Y_freq = (length ** 2) * math.sqrt((co.rho * cs_area) / 
								(co.E * I))

							Loop_start = Lstart * 2 * math.pi
							Loop_finish = (Lfinish * 2 * math.pi) + step

							Loop = np.arange(Loop_start, Loop_finish, step)

							Solver = []

							for omega in Loop:

								kn_freq = omega * Y_freq
								k_freq = np.sqrt((np.sqrt(X_freq + (kn_freq ** 2))) 
									+ X_freq)
								l_freq = np.sqrt((np.sqrt(X_freq + (kn_freq ** 2)))
									- X_freq)
								
								Solv = ((np.cosh(k_freq) * np.cos(l_freq)) - 
									((X_freq / kn_freq) * (np.sinh(k_freq) * np.sin(l_freq))))

								Solver.append(Solv)

								omega_freq_axial_load = []
								for a, b in zip(Solver, Solver[1:]):
									if a <= 1 and b > 1:
										omega_freq_axial_load = omega
										break
									elif a >= 1 and b < 1:
										omega_freq_axial_load = omega
										break	
									else:
										continue
								
								print omega_freq_axial_load
print (time.time() - now)


csv_list = [exp_count, length_array, width_array, height_array,
			gap_array, bias_array, stress_array, axial_load, nominal_freq, bao_freq]
csv_list = zip(*csv_list)
with open("output.csv", "a") as outputcsv:

	writer = csv.writer(outputcsv, delimiter = ',', lineterminator = '\n')

	for item in csv_list:
		writer.writerow(item)

