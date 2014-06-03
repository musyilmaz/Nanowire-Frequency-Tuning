import exp_range_import as eri
import numpy as np

length_array = np.arange(
	float(eri.exp_ranges_data["length_min"]),
	(float(eri.exp_ranges_data["length_max"]) + 
		float(eri.exp_ranges_data["length_step"])),
	float(eri.exp_ranges_data["length_step"])
	)

width_array = np.arange(
	float(eri.exp_ranges_data["width_min"]),
	(float(eri.exp_ranges_data["width_max"]) + 
		float(eri.exp_ranges_data["width_step"])),
	float(eri.exp_ranges_data["width_step"])
	)

height_array = np.arange(
	float(eri.exp_ranges_data["height_min"]),
	(float(eri.exp_ranges_data["height_max"]) + 
		float(eri.exp_ranges_data["height_step"])),
	float(eri.exp_ranges_data["height_step"])
	)

gap_array = np.arange(
	float(eri.exp_ranges_data["gap_min"]),
	(float(eri.exp_ranges_data["gap_max"]) + 
		float(eri.exp_ranges_data["gap_step"])),
	float(eri.exp_ranges_data["gap_step"])
	)

bias_array = np.arange(
	float(eri.exp_ranges_data["bias_min"]),
	(float(eri.exp_ranges_data["bias_max"]) + 
		float(eri.exp_ranges_data["bias_step"])),
	float(eri.exp_ranges_data["bias_step"])
	)

stress_array = np.arange(
	float(eri.exp_ranges_data["stress_min"]),
	(float(eri.exp_ranges_data["stress_max"]) + 
		float(eri.exp_ranges_data["stress_step"])),
	float(eri.exp_ranges_data["stress_step"])
	)