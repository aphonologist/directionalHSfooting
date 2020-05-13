import alph

## Constraints
# Direction L/R -> directional evaluation
# Direction N   -> traditional evaluation

# ParseSyll
class ParseSyllable:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'ParseSyllable' + direction

	def vios(self, candidate):
		loci = []
		for segment in candidate:
			if segment in alph.alphabet:
				if segment == segment.lower():
					loci.append(1)
				else:
					loci.append(0)

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# Trochee
class Trochee:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'Trochee' + direction

	def vios(self, candidate):
		loci = []

		for i in range(len(candidate)):
			if candidate[i] in alph.alphabet:
				if candidate[i-1:i+4] == "(L'L)" or candidate[i-3:i+2] == "(L'L)":
					loci.append(1)
				else:
					loci.append(0)

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# Iamb
class Iamb:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'Iamb' + direction

	def vios(self, candidate):
		loci = []

		for i in range(len(candidate)):
			if candidate[i] in alph.alphabet:
				if candidate[i-1:i+4] == "('LL)" or candidate[i-3:i+2] == "('LL)":
					loci.append(1)
				else:
					loci.append(0)

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# FtBin
class FtBin:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'FtBin' + direction

	def vios(self, candidate):
		loci = []
		for i in range(len(candidate)):
			if candidate[i] in alph.alphabet:
				if candidate[i-2:i+2] == "('L)":
					loci.append(1)
				else:
					loci.append(0)

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci
