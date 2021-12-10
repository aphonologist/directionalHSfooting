# GEN functions

# s  = unsyllabified syllable
# Tt = disyllabic trochee
# iI = disyllabic iamb
# F  = unary foot
# Ddd = internally layered trochee ((Tt)t)
# dDd = internally layered trochee (t(Tt))
# yYy = internally layered iamb ((yY)y)
# yyY = internally layered iamb (y(yY))

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

	# build candidates with internally layered feet
	for i in range(len(input) - 2):
		if input[i:i+3] == 'sss':
			# internal trochees
			candidate = input[:i] + 'Ddd' + input[i+3:]
			candidates.add(candidate)
			candidate = input[:i] + 'dDd' + input[i+3:]
			candidates.add(candidate)
			# internal iambs
			candidate = input[:i] + 'yYy' + input[i+3:]
			candidates.add(candidate)
			candidate = input[:i] + 'yyY' + input[i+3:]
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

