# Deriving RLC values of the experimental design
import numpy as np
from scipy import integrate
import constants as co

def rlc_calculator(axial_load, I, axial_load_frequency, cs_area, length, width, bias, gap):
	X_value = axial_load / (2 * co.E * I)
	Y_value = (axial_load_frequency * 2 * np.pi) * np.sqrt((co.rho 
		* cs_area) / (co.E * I))

	K_value = np.sqrt(np.sqrt(((X_value / 2) ** 2) + (Y_value ** 2)) 
		+ (X_value / 2))
	L_value = np.sqrt(np.sqrt(((X_value / 2) ** 2) + (Y_value ** 2)) 
		- (X_value / 2))

	a1 = (L_value * np.sinh(K_value * length) - K_value * np.sin(L_value * 
		length)) / (L_value * np.cosh(K_value 
		* length) - L_value * np.cos(L_value * length))
	a2 = - 1
	a3 = - a1
	a4 = (-K_value / L_value) * a2

	Xmode = lambda y: ((a1 * np.cosh(K_value * y)) + (a2 * np.sinh(K_value * y)) 
		+ (a3 * np.cos(L_value * y)) + (a4 * np.sin(L_value * y)))
	Xmode2 = lambda y: ((a1 * np.cosh(K_value * y)) + (a2 * np.sinh(K_value * y)) 
		+ (a3 * np.cos(L_value * y)) + (a4 * np.sin(L_value * y))) ** 2

	int_Xmode, err = integrate.quad(Xmode, 0, length)
	int_Xmode2, err = integrate.quad(Xmode2, 0, length)

	mr = lambda y: (co.rho * cs_area * int_Xmode2) / Xmode(y)
	km = lambda y: ((axial_load_frequency * 2 * np.pi) ** 2) * mr(y)

	mre = mr(length / 2)
	kme = km(length / 2)

	# Mohammad's derivation for displacement function
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
	softened_frequency = np.sqrt(kre / mre) / (2 * np.pi)

	eta_constant = ((bias * co.eps * width) ** 2) * kre
	eta_fun1 = lambda y: Xmode(y) / (d_fun(y) ** 2)
	int_eta_fun1, err = integrate.quad(eta_fun1, 0, length)

	eta_fun2_ip = lambda y: kr(y) * (d_fun(y) ** 2)
	eta_fun2 = lambda y: Xmode(y) / eta_fun2_ip(y)
	int_eta_fun2, err = integrate.quad(eta_fun2, 0, length)

	eta = np.sqrt(eta_constant * int_eta_fun1 * int_eta_fun2)

	R = np.sqrt(kre * mre) / (co.Q * (eta ** 2))
	L = mre / (eta ** 2)
	C = (eta ** 2) / kre

	return softened_frequency, eta, R, L, C