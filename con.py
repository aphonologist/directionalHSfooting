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
		loci = [0 for segment in candidate if segment in alph.alphabet]
		seg = 0
		for i in range(len(candidate)):
			if candidate[i] in alph.alphabet:
				if i > 1:
					if candidate[i-1] == "'":
						if candidate[i-2] != '(':
							loci[seg] = 1
				seg += 1

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# Iamb
class Iamb:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'Iamb' + direction

	def vios(self, candidate):
		loci = [0 for segment in candidate if segment in alph.alphabet]
		seg = 0
		for i in range(len(candidate)):
			if candidate[i] in alph.alphabet:
				if 0 < i < len(candidate) - 1:
					if candidate[i-1] == "'":
						if candidate[i+1] != ')':
							loci[seg] = 1
				seg += 1

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# FtBin v1 -- satisfied by (H)
class FtBin:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'FtBin' + direction

	def vios(self, candidate):
		loci = [0 for segment in candidate if segment in alph.alphabet]
		seg = 0
		for i in range(len(candidate)):
			if candidate[i] in alph.alphabet:
				if 1 < i < len(candidate) - 1:
					if candidate[i-1] == "'":
						if candidate[i-2] == '(':
							if candidate[i+1] == ')':
								if candidate[i] != 'H':
									loci[seg] = 1
				seg += 1
		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci
