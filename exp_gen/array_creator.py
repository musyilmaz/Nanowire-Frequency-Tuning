import json_range_import as jri
import numpy as np

# Producing the arrays of;
#		==>	length - width - height - gap - bias - stress

length_array = np.arange(
	float(jri.exp_ranges_data["length_min"]), 
	(float(jri.exp_ranges_data["length_max"]) + 
		float(jri.exp_ranges_data["length_step"])),
	float(jri.exp_ranges_data["length_step"])
	)

width_array = np.arange(
	float(jri.exp_ranges_data["width_min"]), 
	(float(jri.exp_ranges_data["width_max"]) + 
		float(jri.exp_ranges_data["width_step"])),
	float(jri.exp_ranges_data["width_step"])
	)

height_array = np.arange(
	float(jri.exp_ranges_data["height_min"]), 
	(float(jri.exp_ranges_data["height_max"]) + 
		float(jri.exp_ranges_data["height_step"])),
	float(jri.exp_ranges_data["height_step"])
	)

gap_array = np.arange(
	float(jri.exp_ranges_data["gap_min"]), 
	(float(jri.exp_ranges_data["gap_max"]) + 
		float(jri.exp_ranges_data["gap_step"])),
	float(jri.exp_ranges_data["gap_step"])
	)

bias_array = np.arange(
	float(jri.exp_ranges_data["bias_min"]), 
	(float(jri.exp_ranges_data["bias_max"]) + 
		float(jri.exp_ranges_data["bias_step"])),
	float(jri.exp_ranges_data["bias_step"])
	)

stress_array = np.arange(
	float(jri.exp_ranges_data["stress_min"]), 
	(float(jri.exp_ranges_data["stress_max"]) + 
		float(jri.exp_ranges_data["stress_step"])),
	float(jri.exp_ranges_data["stress_step"])
	)
