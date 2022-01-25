# GEN functions

# s  = unfooted syllable
# Tt = trochee
# iI = iamb
# F  = monosyllabic foot

def gen_foot(input):
	candidates = set([])

	# add fully faithful candidate
	candidates.add(input)

	# build candidates with monosyllabic feet
	for i in range(len(input)):
		if input[i] == 's':
			candidate = input[:i] + "F" + input[i+1:]
			candidates.add(candidate)

	# build candidates with bisyllabic feet
	for i in range(len(input) - 1):
		if input[i:i+2] == 'ss':
			# trochees
			candidate = input[:i] + "Tt" + input[i+2:]
			candidates.add(candidate)
			# iambs
			candidate = input[:i] + "iI" + input[i+2:]
			candidates.add(candidate)

	return sorted(list(candidates))

# parallel equivalent
def gen_foot_parallel(input):
	candidates = set([])

	# add fully faithful candidate
	candidates.add(input)

	# build candidates of length equal to input
	stack = ['']
	while stack:
		cand = stack.pop()
		for foot in ['s', 'F', 'Tt', 'iI']:
			cand2 = cand + foot
			if len(cand2) == len(input):
				candidates.add(cand2)
			if len(cand2) < len(input):
				stack.append(cand2)

	return sorted(list(candidates))

