# Creating objects for each experiments
import constants as co
import numpy as np

def make_object(num, length, width, height, gap, bias, stress, load, cs_area, I):
	exp_obj = expObj(num, length, width, height, gap, bias, stress, load, cs_area, I)
	return exp_obj


class expObj:
	def __init__(self, num, length, width, height, gap, bias, stress, load, cs_area, I):
		self.num = num
		self.length = length
		self.width = width
		self.height = height
		self.gap = gap
		self.bias = bias
		self.stress = stress
		self. load = load
		self.cs_area = cs_area
		self.I = I

