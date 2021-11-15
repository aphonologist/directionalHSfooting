## Constraints
# Direction L/R -> directional evaluation
# Direction N   -> traditional evaluation

# ParseSyll
# penalizes unfooted syllables (s)
class ParseSyllable:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'ParseSyllable'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		if self.direction == 'R':
			candidate = candidate[::-1]
		loci = [0] * len(candidate)
		for i in range(len(candidate)):
			if candidate[i] == 's':
				loci[i] = 1

		if self.direction == 'N': return [sum(loci)]
		return loci

# Trochee
# penalizes disyllabic iambs (iI)
class Trochee:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'Trochee'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		loci = [0] * len(candidate)
		if self.direction == 'L':
			for i in range(len(candidate) - 1):
				if candidate[i:i+2] == 'iI':
					loci[i+1] = 1
		elif self.direction == 'R':
			candidate = candidate[::-1]
			for i in range(len(candidate) - 1):
				if candidate[i:i+2] == 'Ii':
					loci[i+1] = 1
		elif self.direction == 'N':
			loci = [candidate.count('iI')]

		return loci

# Iamb
# penalizes disyllabic trochees (Tt) and unary feet (F)
class Iamb:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'Iamb'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		loci = [0] * len(candidate)
		if self.direction == 'L':
			for i in range(len(candidate) - 1):
				if candidate[i:i+2] == 'Tt':
					loci[i+1] = 1
			for i in range(len(candidate)):
				if candidate[i] == 'F':
					loci[i] = 1
		elif self.direction == 'R':
			candidate = candidate[::-1]
			for i in range(len(candidate) - 1):
				if candidate[i:i+2] == 'tT':
					loci[i+1] = 1
			for i in range(len(candidate)):
				if candidate[i] == 'F':
					loci[i] = 1
		elif self.direction == 'N':
			loci = [candidate.count('Tt') + candidate.count('F')]

		return loci

# FtBin
# penalizes monosyllabic feet (U)
class FtBin:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'FtBin'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		loci = [0] * len(candidate)
		if self.direction == 'R':
			candidate = candidate[::-1]
		for i in range(len(candidate)):
			if candidate[i] == 'F':
				loci[i] = 1
		if self.direction == 'N':
			loci = [candidate.count('F')]

		return loci

# FootLeft
# assign a violation if the leftmost syllable is unfooted
class FootLeft:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'FootLeft'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		loci = [0] * len(candidate)
		if candidate[0] == 's':
			loci[0] = 1

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# FootRight
# assign a violation if the rightmost syllable is unfooted
class FootRight:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'FootRight'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		loci = [0] * len(candidate)
		if candidate[-1] == 's':
			loci[-1] = 1

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# NonFinality
# assign a violation if the rightmost syllable is footed
class NonFinality:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'NonFinality'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		loci = [0] * len(candidate)
		if candidate[-1] != 's':
			loci[-1] = 1

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# Hd(prwd)
# assign a violation if there are no feet
class HdPrWd:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'Hd(PrWd)'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		loci = [0]
		footless = True
		for syllable in candidate:
			if syllable in ['F', 'i', 'T']:
				footless = False
				break
		if footless:
			loci[0] = 1

		return loci

# *FootFoot
# penalizes adjacent feet
class FootFoot:
	def __init__(self, direction):
		self.direction = direction
		self.name = '*FootFoot'
		if direction != 'N':
			self.name += direction

	def vios(self, candidate):
		loci = [0] * len(candidate)
		if self.direction == 'L':
			for i in range(len(candidate) - 1):
				if candidate[i:i+2] in ['FF', 'FT', 'tF', 'Fi', 'IF', 'Ii', 'IT', 'ti', 'tT']:
					loci[i+1] = 1
		elif self.direction == 'R':
			candidate = candidate[::-1]
			for i in range(len(candidate) - 1):
				if candidate[i:i+2] in ['FF', 'TF', 'Ft', 'iF', 'FI', 'iI', 'TI', 'it', 'Tt']:
					loci[i+1] = 1
		elif self.direction == 'N':
			loci = [sum([candidate.count(x) for x in ['FF', 'FT', 'tF', 'Fi', 'IF', 'Ii', 'IT', 'ti', 'tT']])]

		return loci

# AllFt-L: For each foot in a word assign one violation for every syllable separating it from the left edge of the word
class AllFtL:
	def __init__(self):
		self.direction = 'N'
		self.name = 'AllFtL'

	def vios(self, candidate):
		loci = 0
		for i in range(len(candidate)):
			if candidate[i] == '(':
				for j in range(i):
					if candidate[j] in alph.alphabet:
						loci += 1
		return [loci]

# AllFt-R: For each foot in a word assign one violation for every syllable separating it from the right edge of the word
class AllFtR:
	def __init__(self):
		self.direction = 'N'
		self.name = 'AllFtR'

	def vios(self, candidate):
		loci = 0
		for i in range(len(candidate)):
			if candidate[i] == ')':
				for j in range(i+1, len(candidate)):
					if candidate[j] in alph.alphabet:
						loci += 1
		return [loci]
