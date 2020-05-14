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

# FootForm -- combines Trochee and Iamb into one constraint
class FootForm:
	def __init__(self, type, direction):
		self.type = type
		self.direction = direction
		self.name = 'FootForm' + type + direction

	def vios(self, candidate):
		if self.type == 'Trochee':
			loci = [0 for segment in candidate if segment in alph.alphabet]
			seg = 0
			for i in range(len(candidate)):
				if candidate[i] in alph.alphabet:
					if i > 1:
						if candidate[i-1] == "'":
							if candidate[i-2] != '(':
								loci[seg] = 1
					seg += 1
		elif self.type == 'Iamb':
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

# FtBin v2 -- violated by (H)
class FtBinSyll:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'FtBinSyll' + direction

	def vios(self, candidate):
		loci = [0 for segment in candidate if segment in alph.alphabet]
		seg = 0
		for i in range(len(candidate)):
			if candidate[i] in alphabet:
				if 1 < i < len(candidate) - 1:
					if candidate[i-1] == "'":
						if candidate[i-2] == '(':
							if candidate[i+1] == ')':
								loci[seg] = 1
				seg += 1

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# Clash -- Pruitt doesn't use this constraint
class Clash:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'Clash' + direction

	def vios(self, candidate):
		cand = candidate.replace('(', '').replace(')', '')
		loci = [0 for segment in cand if segment in alph.alphabet]
		seg = 0
		for i in range(len(cand)):
			if cand[i] in alphabet:
				if 0 < i < len(cand) - 1:
					if cand[i-1] == "'":
						if cand[i+1] == "'":
							loci[seg] = 1
				seg += 1

		if self.direction == 'N': return [sum(loci)]
		if self.direction == 'R': return loci[::-1]
		return loci

# Edgefoot -- assign a violation if the left/right edge is unfooted
class EdgeFoot:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'EdgeFoot' + direction

	def vios(self, candidate):
		loci = [0]
		if self.direction == 'L':
			for segment in candidate:
				if segment in alph.alphabet:
					if segment == segment.lower():
						loci[0] = 1
					break
		else:
			for segment in candidate[::-1]:
				if segment in alph.alphabet:
					if segment == segment.lower():
						loci[0] = 1
					break

		return loci

# NonFinality -- assign a violation if the rightmost syllable is stressed
class NonFinality:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'NonFinality' + direction

	def vios(self, candidate):
		loci = [0]
		if len(candidate) > 2:
			if candidate[-3] == "'":
				loci[0] = candidate[1]

		if self.direction == 'N': return [sum(loci)]
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
		return loci

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
		return loci

# Nate Koser align L: *syllable(Foot)
class SyllFt:
	def __init__(self):
		self.direction = 'N'
		self.name = 'SyllFt'

	def vios(self, candidate):
		loci = 0
		for i in range(1,len(candidate)):
			if candidate[i] == '(':
				if candidate[i-1] in alph.alphabet:
					loci += 1
		return loci

# Nate Koser align R: *(Foot)syllable
class FtSyll:
	def __init__(self):
		self.direction = 'N'
		self.name = 'FtSyll'

	def vios(self, candidate):
		loci = 0
		for i in range(len(candidate) - 1):
			if candidate[i] == ')':
				if candidate[i+1] in alph.alphabet:
					loci += 1
		return loci

# *Foot -- don't have feet
class NoFeet:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'NoFeet' + direction

	def vios(self, candidate):
		if self.direction == 'N':
			loci = 0
			for i in range(len(candidate)):
				if candidate[i] == '(':
					loci += 1
			return loci
		else:
			loci = [' ' for segment in candidate if segment in alph.alphabet]
			seg = 0
			for i in range(len(candidate)):
				if candidate[i] == '(':
					loci[seg] = '('
					seg += 1
			if self.direction == 'R':
				return loci[::-1]
			return loci

# HaveStress -- have at least one stress
class HaveStress:
	def __init__(self, direction):
		self.direction = direction
		self.name = 'HaveStress' + direction

	def vios(self, candidate):
		if self.direction == 'N':
			loci = 0
			if '(' not in candidate:
				loci = 1
			return loci
		else:
			loci = [' ']
			if '(' not in candidate:
				loci[0] = '('

			# Direction doesn't matter -- there is exactly one locus of violation
			return loci
