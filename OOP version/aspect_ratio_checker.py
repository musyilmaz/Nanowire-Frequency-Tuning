# Aspect ratio checker

def aspect_ratio_checker(length, height):

	aspect_ratio = length / height

	if aspect_ratio >= 15:
		return True
	else:
		return False