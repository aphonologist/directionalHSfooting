import sys
from sympy import *
import alph
from con import *
from gen import gen
from tablO import tablO
from fred import FRed

# command line parameter to control printing
verbose = '-v' in sys.argv

# function to determine whether v1 <= v2 by checking first position where they differ
def leq(v1, v2):
	for i in range(len(v1)):
		if v1[i] < v2[i]:
			return True
		if v1[i] > v2[i]:
			return False
	return True

# function that extracts ERCs in CNF from a comparative vector
def ERCs(cv):
	W = [i for i in range(len(cv)) if cv[i] == 'W']
	L = [i for i in range(len(cv)) if cv[i] == 'L']

	WLs = []
	for l in L:
		WL = []
		for w in W:
			WL.append(str(w) + '>>' + str(l))
		WLs.append(WL)

	return WLs

alpha = ['l', 'L']
alph.initialize(alpha)
urs = ['llllll', 'lllllll']

con = [ParseSyllable('L'), ParseSyllable('R'), Trochee('L'), Trochee('R'), Iamb('L'), Iamb('R'), FtBin('L'), FtBin('R')]

for input in urs:
	print(input)

	# Generate candidates
	candidates = gen(input)

	# Assemble tableau
	tableau = []
	for constraint in con:
		tableau.append([constraint.vios(candidate) for candidate in candidates])

	# Find minimal violation for all constraints
	viominima = [tableau[c][0][:] for c in range(len(con))]

	for c in range(1, len(candidates)):
		for v in range(len(con)):
			if not leq(viominima[v], tableau[v][c]):
					viominima[v] = tableau[v][c][:]

	# Iterate through candidates
	for optimum in range(len(candidates)):

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

		fnf = FRed(comptableau[:optimum] + comptableau[optimum + 1:])
		print(candidates[optimum])
		if 'unsat' not in fnf:
			ercs = []
			for x in fnf:
				ercs += ERCs(x)
			print(ercs)
		else:
			print('unsatisfiable!')
		print()
