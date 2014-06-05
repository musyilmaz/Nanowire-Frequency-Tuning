import constants as co
import exp_array_creator as eac
import math
import numpy as np
import csv
import time
from scipy import integrate

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
steps = [1e6, 1e3]

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

						Lfinish = Lstart + (0.9999999999 * (10 ** (Num_Dig - 1)))

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
								if a >= 1 and b < 1:
									omega_freq_axial_load = omega
									break

							axial_load_freq = (omega_freq_axial_load / (2 * math.pi))

							# Determining RLC values for the new frequency

							X_ = load / (2 * co.E * I)
							Y_ = omega_freq_axial_load * np.sqrt((co.rho * cs_area) / (co.E * I))

							K = np.sqrt(np.sqrt(((X_ / 2) ** 2) + (Y_ ** 2)) + (X_ / 2))
							L = np.sqrt(np.sqrt(((X_ / 2) ** 2) + (Y_ ** 2)) - (X_ / 2))

							a1 = (L * np.sinh(K * length) - K * np.sin(L * length)) / (L * np.cosh(K * length) - L * np.cos(L * length))
							a2 = - 1
							a3 = - a1
							a4 = (-K / L) * a2

							Xmode = lambda y: (a1 * np.cosh(K * y)) + (a2 * np.sinh(K * y)) + (a3 * np.cos(L * y)) + (a4 * np.sin(L * y))
							Xmode2 = lambda y: ((a1 * np.cosh(K * y)) + (a2 * np.sinh(K * y)) + (a3 * np.cos(L * y)) + (a4 * np.sin(L * y))) ** 2

							int_Xmode, err = integrate.quad(Xmode, 0, length)
							int_Xmode2, err = integrate.quad(Xmode2, 0, length)

							mr = lambda y: (co.rho * cs_area* int_Xmode2) / Xmode(y)
							km = lambda y: (omega_freq_axial_load ** 2) * mr(y)

							mre = mr(length / 2)
							kme = km(length / 2)

							#  Mohammad's derivation for displacement function

							disp_constA = (co.eps * width * (bias ** 2)) / (2 * co.E * I * (gap **2))
							c1 = - (disp_constA * length) / 2
							c2 = (disp_constA * (length ** 2)) / 12
							y_four = lambda y: y ** 4
							y_three = lambda y: y ** 3
							y_two = lambda y: y ** 2
							part1 = lambda y: (disp_constA * y_four(y)) / 24
							part2 = lambda y: (c1 * y_three(y)) / 6
							part3 = lambda y: (c2 * y_two(y)) / 2

							totaldisp = lambda y: part1(y) + part2(y) + part3(y)
							d_fun = lambda y: (gap - totaldisp(y))

							inv_d_fun3 = lambda y: (1 / (d_fun(y) ** 3))
							int_inv_d_fun3, err = integrate.quad(inv_d_fun3, 0, length)
							ke = (bias ** 2) * width * co.eps * int_inv_d_fun3
							kr = lambda y: (km(y) - ke)
							kre = kr(length / 2)
							freq_new = np.sqrt(kre / mre) / (2 * math.pi)

							if step == 1e3:
								Num_Dig = np.ceil(math.log10(abs(axial_load_freq)))
								Lstart = (10 ** (Num_Dig - 2) * 
									np.floor(axial_load_freq / (10 ** (Num_Dig - 2))))
								Lfinish = Lstart + (0.9 * (10 ** (Num_Dig - 2)))
								print "running 1"
							



print axial_load_freq, freq_new
print (time.time() - now)

csv_list = [exp_count, length_array, width_array, height_array,
			gap_array, bias_array, stress_array, axial_load, nominal_freq, bao_freq]
csv_list = zip(*csv_list)
with open("output.csv", "a") as outputcsv:

	writer = csv.writer(outputcsv, delimiter = ',', lineterminator = '\n')

	for item in csv_list:
		writer.writerow(item)

