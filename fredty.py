import sys

# command line parameter to control printing
verbose = '-v' in sys.argv

# GEN function
def gen(input):
	candidates = set([])

	# add fully faithful candidate
	candidates.add(input)

	# build candidates with monosyllabic feet
	for j in range(len(input)):
		if input[j] in alphabet:
			if input[j] == input[j].lower():
				candidate = input[:j] + "('" + input[j].upper() + ")" + input[j+1:]
				candidates.add(candidate)

	# build candidates with bisyllabic feet
	for j in range(len(input) - 1):
		if input[j] in alphabet and input[j+1] in alphabet:
			if input[j:j+2] == input[j:j+2].lower():
				# trochees
				candidate = input[:j] + "('" + input[j:j+2].upper() + ")" + input[j+2:]
				candidates.add(candidate)
				# iambs
				candidate = input[:j] + "(" + input[j].upper() + "'" + input[j+1].upper() + ")" + input[j+2:]
				candidates.add(candidate)

	return sorted(list(candidates))

# EVAL function
def eval(tableau, traditional=False):
	# Each candidate may be a winner
	optima = [True for candidate in tableau[0]]

	# Step through constraints
	for con in tableau[1:]:
		# Stop if only one optima
		if len([x for x in optima if x]) == 1:
			return optima

		if traditional:
			best = 99999999999999999999999999
			for c in range(len(con)):
				if optima[c]:
					if con[c] < best:
						best = con[c]
			for c in range(len(con)):
				if con[c] > best:
					optima[c] = False
		else:

			## Step through loci from worst to best
			# Does this locus decide between possible optima?
			for l in range(len(con[0])):
				deciding = False
				for c in range(len(con)):
					if optima[c]:
						if con[c][l] == ' ':
							deciding = True
							break
				# Some candidate does not possess this locus of violation
				# Remove candidates that do
				if deciding:
					for c in range(len(con)):
						if con[c][l] != ' ':
							optima[c] = False
	return optima

# HS function -- assumes a unique output for each input
def HS(ur, g, traditional):
	input = ur
	converged = False

	while not converged:
		# Generate candidates
		candidates = gen(input)

		# Assemble tableau
		tableau = [candidates]
		for constraint in g:
			tableau.append([constraint.vios(candidate) for candidate in candidates])

		# Get optimal candidates
		optima = eval(tableau, traditional)

		# Check for convergence
		fullyfaithful = candidates.index(input)
		if optima[fullyfaithful]:
			return input
		else:
			input = candidates[optima.index(True)]

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
			if segment in alphabet:
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
		loci = [0 for segment in candidate if segment in alphabet]
		seg = 0
		for i in range(len(candidate)):
			if candidate[i] in alphabet:
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
		loci = [0 for segment in candidate if segment in alphabet]
		seg = 0
		for i in range(len(candidate)):
			if candidate[i] in alphabet:
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
		loci = [0 for segment in candidate if segment in alphabet]
		seg = 0
		for i in range(len(candidate)):
			if candidate[i] in alphabet:
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

# function to print tableaux
def tablO(tableau, input, candidates, constraints, optimum, comptableau):
	input = '/' + input + '/'

	colwidths = [max(len(input), 3 + max([len(can) for can in candidates]))] + [2 + max(2*len(input),len(con.name)) for con in constraints]

	hline = ''
	for colwidth in colwidths[:-1]:
		hline += '-' * colwidth + '-|-'
	hline += '-' * colwidths[-1]

	# first row: input and constraints
	print('{0:<{1}}'.format(input, colwidths[0]), end=' | ')
	for c in range(len(constraints)):
		if c == len(constraints) - 1:
			print('{0:^{1}}'.format(constraints[c].name, colwidths[c+1]))
		else:
			print('{0:^{1}}'.format(constraints[c].name, colwidths[c+1]), end=' | ')
	print(hline)

	# remaining rows: candidates and violations
	for c in range(len(candidates)):
		if c == optimum:
			print('-> {0:>{1}}'.format(candidates[c], colwidths[0]-3), end=' | ')
			for v in range(len(tableau)):
				if v == len(tableau) - 1:
					print('', '{0:^{1}}'.format(' '.join([str(x) for x in tableau[v][c]]), colwidths[v+1] - 1))
				else:
					print('', '{0:^{1}}'.format(' '.join([str(x) for x in tableau[v][c]]), colwidths[v+1] - 1), end=' | ')
		else:
			print('   {0:<{1}}'.format(candidates[c], colwidths[0]-3), end=' | ')
			for v in range(len(tableau)):
				if v == len(tableau) - 1:
					print(comptableau[c][v], '{0:^{1}}'.format(' '.join([str(x) for x in tableau[v][c]]), colwidths[v+1] - 2))
				else:
					print(comptableau[c][v], '{0:^{1}}'.format(' '.join([str(x) for x in tableau[v][c]]), colwidths[v+1] - 2), end=' | ')
		if c < len(tableau[0]) - 1:
			print(hline)

# function to determine whether v1 <= v2 by checking first position where they differ
def leq(v1, v2):
	for i in range(len(v1)):
		if v1[i] < v2[i]:
			return True
		if v1[i] > v2[i]:
			return False
	return True

# point-wise fusion
def fuse(a, b):
	if a == 'L' or b == 'L': return 'L'
	if a == 'e': return b
	if b == 'e': return a
	return 'W'

# function that extracts ERCs from a comparative vector
def ERCs(cv):
	W = []
	L = []

	for c in range(len(cv)):
		if cv[c] == 'W':
			W.append(c)
		if cv[c] == 'L':
			L.append(c)

	WLs = []
	for l in L:
		WL = []
		for w in W:
			WL.append(str(w) + '>>' + str(l))
		WLs.append(WL)

	ERC = WLs[0][:]
	for WL in WLs[1:]:
		temp = ERC[:]
		ERC = []
		for wl in WL:
			for t in temp:
				ERC.append(wl + ',' + t)
	return ERC

# FRed
def FRed(comptableau):
	FNF = []

	# if A is empty, then FNF is empty
	if not comptableau:
		return FNF

	cols = len(comptableau[0])

	# Fuse the entire tableau
	fuseall = comptableau[0][:]

	# Residuals - collect vectors with an 'e' in col i
	res = []
	for c in range(cols):
		res.append([])

	for row in comptableau[1:]:
		fuseall = [fuse(a,b) for a,b in zip(fuseall, row)]
		for c in range(cols):
			if row[c] == 'e':
				res[c].append(row)

	holdfus = fuseall[:]

	# Update residuals - keep only cols with 'W' in fuseall
	for c in range(cols):
		if fuseall[c] != 'W':
			res[c] = []

	# Check entailments

	# if fuseall is all 'W', then no ranking info
	if 'L' not in fuseall and 'e' not in fuseall:
		holdfus = []

	# if fuseall is all 'L', then unsatisfiable
	if 'W' not in fuseall and 'e' not in fuseall:
		print('unsatisfiable!')
		FNF = []

	# does the set of residuals entail fuseall?

	# fuse residuals
	fuseres = ['e'] * cols
	for c in range(cols):
		for r in res[c]:
			fuseres = [fuse(a,b) for a,b in zip(fuseres, r)]

	# fuseres entails fuseall if they have the same number of 'L's
	if fuseres.count('L') == fuseall.count('L'):
		holdfus = []

	FNF = [holdfus]

	# recurse on the residuals
	for c in range(cols):
		FNF += FRed(res[c])

	return [fnf for fnf in FNF if fnf]

alphabet = ['l', 'L']
input = 'lll'

con = [ParseSyllable('L'), ParseSyllable('R'), Trochee('L'), Trochee('R'), Iamb('L'), Iamb('R'), FtBin('L'), FtBin('R')]

# Generate candidates
candidates = gen(input)

# Assemble tableau
tableau = []
for constraint in con:
	tableau.append([constraint.vios(candidate) for candidate in candidates])

import random
optimum = random.randint(0,len(candidates)-1)

# Find minimal violation for all constraints
viominima = [tableau[c][0][:] for c in range(len(con))]

for c in range(1, len(candidates)):
	for v in range(len(con)):
		if not leq(viominima[v], tableau[v][c]):
				viominima[v] = tableau[v][c][:]

# Generate comparative tableau
comptableau = []
for c in range(len(candidates)):
	row = [''] * len(con)
	for v in range(len(con)):
		if leq(tableau[v][optimum], tableau[v][c]) and leq(tableau[v][c], tableau[v][optimum]):
			row[v] = 'e'
		elif leq(tableau[v][c], tableau[v][optimum]):
			row[v] = 'L'
		else:
			row[v] = 'W'
	comptableau.append(row)

#tablO(tableau, input, candidates, con, optimum, comptableau)

#print(FRed(comptableau[:optimum] + comptableau[optimum + 1:]))

# testing with exs from BP (2011)
ex90 = [['W', 'L', 'W'], ['e','W','L']]
#print(FRed(ex90))

ex96 = [['W', 'L', 'e', 'W'], ['e','W','L','W'], ['W','W','L','e'], ['W','L','W','e']]
#print(FRed(ex96))

ex98 = [['e','e','W','L'],['e','W','L','e'],['W','L','W','e'],['e','e','W','W'],['e','W','L','W'],['W','L','W','L'],['W','W','L','e']]
#print(FRed(ex98))
