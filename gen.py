import alph

# GEN function
def gen(input):
	candidates = set([])

	# add fully faithful candidate
	candidates.add(input)

	# build candidates with monosyllabic feet
	for j in range(len(input)):
		if input[j] in alph.alphabet:
			if input[j] == input[j].lower():
				candidate = input[:j] + "('" + input[j].upper() + ")" + input[j+1:]
				candidates.add(candidate)

	# build candidates with bisyllabic feet
	for j in range(len(input) - 1):
		if input[j] in alph.alphabet and input[j+1] in alph.alphabet:
			if input[j:j+2] == input[j:j+2].lower():
				# trochees
				candidate = input[:j] + "('" + input[j:j+2].upper() + ")" + input[j+2:]
				candidates.add(candidate)
				# iambs
				candidate = input[:j] + "(" + input[j].upper() + "'" + input[j+1].upper() + ")" + input[j+2:]
				candidates.add(candidate)

	return sorted(list(candidates))
