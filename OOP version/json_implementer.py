import json
import numpy as np

with open ("exp_ranges.json") as json_file:
	jData = json.load(json_file)

length_array = np. arange(
	float(jData['length_min']),
	(float(jData['length_max']) + float(jData['length_step'])),
	float(jData['length_step'])
	)

width_array = np. arange(
	float(jData['width_min']),
	(float(jData['width_max']) + float(jData['width_step'])),
	float(jData['width_step'])
	)

height_array = np. arange(
	float(jData['height_min']),
	(float(jData['height_max']) + float(jData['height_step'])),
	float(jData['height_step'])
	)

gap_array = np. arange(
	float(jData['gap_min']),
	(float(jData['gap_max']) + float(jData['gap_step'])),
	float(jData['gap_step'])
	)

bias_array = np. arange(
	float(jData['bias_min']),
	(float(jData['bias_max']) + float(jData['bias_step'])),
	float(jData['bias_step'])
	)

stress_array = np. arange(
	float(jData['stress_min']),
	(float(jData['stress_max']) + float(jData['stress_step'])),
	float(jData['stress_step'])
	)
