"""
Length order should be either 3 or 6
"""


import constants as co # use constants as co.E
import array_creator as ac # use arrays as ac.length_array
import nominal_frequency as nf # nominal frequency calculator
import bao_frequency as bf # bao frequency calculator
import iterator_step as iStep # iterator step determiner
import solver_iterator as sIter # generating solver list / deriving 1st mode frequency
import rlc_calculator as rlc # generating rlc values
import numpy as np
import csv

# Empty list creations
exp_count = ["Experimental Design"]
length_exp = ["Length (m)"]
width_exp = ["Width (m)"]
height_exp = ["Height (m)"]
gap_exp = ["Electrode - Wire Gap (m)"]
bias_exp = ["Bias Voltage (V)"]
stress_exp = ["Applied Stress (Pa)"]
load_exp = ["Applied Load (N)"]
nominal_freq_exp = ["Nominal Frequency (Hz)"]
bao_freq_exp = ["Bao Frequency (Hz)"] 
axial_load_exp = ["Axial Load Frequency (Hz)"]
softened_freq_exp = ["Electrical Softeneed Frequency (Hz)"]
eta_exp = ["Eta Value"]
R_exp = ["R Value (Ohm)"]
L_exp = ["L Value (H)"]
C_exp = ["C Value (F)"]

exp_num = 0

# List filling and iterator on experimental designs
for length in np.nditer(ac.length_array):
	for width in np.nditer(ac.width_array):
		for height in np.nditer(ac.height_array):
			for gap in np.nditer(ac.gap_array):
				for bias in np.nditer(ac.bias_array):
					for stress in np.nditer(ac.stress_array):
						
						# Each calculation is an experimental design
						# Exp_num only dictates which experimental design is running
						exp_num += 1
						exp_count.append(exp_num)

						# ***_exp list ====> Required for output.csv
						length_exp.append(length)
						width_exp.append(width)
						height_exp.append(height)
						gap_exp.append(gap)
						bias_exp.append(bias)
						stress_exp.append(stress)

						# Calculating the load from the stress value 
						# for each experimental design
						# cs_area ===> Cross sectional area
						#       I ===> Inertia       
						cs_area = height * width
						I = (width * (height ** 3)) / 12
						axial_load = stress * cs_area
						# Filling the load_exp list for output.csv
						load_exp.append(axial_load)

						# Nominal Frequency
						nominal_frequency = nf.nominal_frequency(height, length, co.E, co.rho)
						nominal_freq_exp.append(nominal_frequency)			

						# Axial Load implemented frequency (Bao formulation)
						bao_frequency = bf.bao_frequency(nominal_frequency, axial_load, 
							length, co.E, I)
						bao_freq_exp.append(bao_frequency)

						length_order = np.ceil(abs(np.log10(length)))

						
						iteration = [0, 1, 2, 3, 4]
					
						# iteration count starts from 0
						for iteration_count in iteration:	

							# Feeding the iteration base point to the iterator
							if iteration_count == 0:
								freq = bao_frequency * 2 * np.pi
							else:
								freq = axial_load_frequency * 2 * np.pi

							# Getting iteration values based on the iteration count
							# 			===>iteration_start, iteration_finish, step 
							step, iter_start, iter_finish = iStep.iterator_step(
								freq, iteration_count, length_order)
							
							# Creating Loop list for iterator process
							Loop = np.arange(iter_start, iter_finish, step)

							# Variables for iterator process
							X_value = (axial_load * (length ** 2)) / (2 * co.E * I)
							Y_value = (length ** 2) * np.sqrt((co.rho * cs_area) / 
								(co.E * I))

							# Filling Solver list and deriving 1st mode frequency
							axial_load_frequency = sIter.solver_iterator(Loop, X_value, Y_value)

						# Filling the axial_load_exp list with the tuned result
						axial_load_exp.append(axial_load_frequency)
						
						# Determining RLC values based on inputs
						# 			Inputs ===> axial_load_frequency, bias, gap

						softened_frequency, eta, R, L, C = rlc.rlc_calculator(axial_load, 
							I, axial_load_frequency, cs_area, length, width, bias, gap)

						softened_freq_exp.append(softened_frequency)
						eta_exp.append(eta)
						R_exp.append(R)
						L_exp.append(L)
						C_exp.append(C)

						print "Experimental Design #%d is completed" % exp_num

csv_list = [exp_count, length_exp, width_exp, height_exp, gap_exp, bias_exp, stress_exp, 
	load_exp, nominal_freq_exp, bao_freq_exp, axial_load_exp, softened_freq_exp, eta_exp, 
	R_exp, L_exp, C_exp]
csv_list = zip(*csv_list)
with open("output.txt", "a") as outputtxt:
	writer = csv.writer(outputtxt, delimiter = ',', lineterminator = '\n')
	for item in csv_list:
		writer.writerow(item)