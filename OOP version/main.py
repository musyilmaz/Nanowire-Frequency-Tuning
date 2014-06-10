import json_implementer as jImp
import aspect_ratio_checker as arc
import object_system as objSys 
import nominal_frequency as nf
import bao_frequency as bf
import iterator_step as iStep 
import solver_iterator as sIter
import rlc_calculator as rlc
import csv
import constants as co
import numpy as np

count_exp = ["Experimental Design"]
length_exp = ["Length (m)"]
width_exp = ["Width (m)"]
height_exp = ["Height (m)"]
gap_exp = ["Electrode - Wire Gap (m)"]
bias_exp = ["Bias Voltage (V)"]
stress_exp = ["Applied Stress (Pa)"]
load_exp = ["Applied Load (N)"]
nominal_freq_exp = ["Nominal Frequency (Hz)"]
bao_freq_exp = ["Bao Frequency (Hz)"]
axial_load_exp = ["Axial Loaded Frequency (Hz)"]
softened_freq_exp = ["Electrical Softened Frequency (Hz)"]
eta_exp = ["Eta Value"]
R_exp = ["R Value (Ohm)"]
L_exp = ["L Value (H)"]
C_exp = ["C Value (F)"]

exp_num = 0

exp_obj = []

for length in np.nditer(jImp.length_array):
	for width in np.nditer(jImp.width_array):
		for height in np.nditer(jImp.height_array):
			for gap in np.nditer(jImp.gap_array):
				for bias in np.nditer(jImp.bias_array):
					for stress in np.nditer(jImp.stress_array):

						# Getting boolean for Aspect ratio >= 15
						# 			Aspect Ratio ===> Length / Height
						arc_boolean = arc.aspect_ratio_checker(length, height)

						if arc_boolean == False: # System will not solve the geometry
							
							break

						else:                    # System will solve the geometry
							
							# Appending the experiment to the array
							exp_num += 1
							count_exp.append(exp_num)

							# ***_exp list ====> generation
							length_exp.append(length)
							width_exp.append(width)
							height_exp.append(height)
							gap_exp.append(gap)
							bias_exp.append(bias)
							stress_exp.append(stress)

							# cs_area ===> Cross Sectional Area
							#       I ===> Inertia
							cs_area = height * width
							I = (width * (height ** 3)) / 12
							load = stress * cs_area

							load_exp.append(load)

							# Creating objects for further experimental analysis
							exp_obj.append(
								objSys.make_object(
									exp_num, length, width, height, 
									gap, bias, stress, load, cs_area, I)
								)

# Getting other properties of objects
for obj in exp_obj: 	

	# Determining objects properties
	obj.nomFreq = nf.nominal_frequency(obj.length, obj.height)

	obj.baoFreq = bf.bao_frequency(obj.nomFreq, obj.load, obj.length, obj.I)

	length_order = np.ceil(abs(np.log10(obj.length)))

	# Iteration fining
	iteration = [0, 1, 2, 3, 4]

	for iteration_count in iteration:

		if iteration_count == 0:
			freq = obj.baoFreq * 2 * np.pi
		else:
			freq = axial_load_freq * 2 * np.pi

		step, iter_start, iter_finish = iStep.iterator_step(
			freq, iteration_count, length_order)

		Loop = np.arange(iter_start, iter_finish, step)

		X_value = (obj.load * (obj.length ** 2)) / (2 * co.E * obj.I)
		Y_value = (obj.length ** 2) * np.sqrt((co.rho * obj.cs_area) /
			(co.E * obj.I))

		axial_load_freq = sIter.solver_iterator(Loop, X_value, Y_value)

	obj.axialLoadFreq = axial_load_freq

	obj.softenedFreq, obj.etaValue, obj.rValue, obj.lValue, obj.cValue = rlc.rlc_calculator(
		obj.load, obj.I, obj.axialLoadFreq, obj.cs_area, obj.length, obj.width, obj.bias, obj.gap)


	# object appender
	nominal_freq_exp.append(obj.nomFreq)
	bao_freq_exp.append(obj.baoFreq)
	axial_load_exp.append(obj.axialLoadFreq)
	softened_freq_exp.append(obj.softenedFreq)
	eta_exp.append(obj.etaValue)
	R_exp.append(obj.rValue)
	L_exp.append(obj.lValue)
	C_exp.append(obj.cValue)


	print "Experimental study completed"
csv_list = [count_exp, length_exp, width_exp, height_exp, gap_exp, bias_exp, stress_exp, 
	load_exp, nominal_freq_exp, bao_freq_exp, axial_load_exp, softened_freq_exp, eta_exp, 
	R_exp, L_exp, C_exp]
csv_list = zip(*csv_list)
with open("output.txt", "a") as outputtxt:
	writer = csv.writer(outputtxt, delimiter = ',', lineterminator = '\n')
	for item in csv_list:
		writer.writerow(item)