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

	return WLs

alpha = ['l', 'L']
alph.initialize(alpha)
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

tablO(tableau, input, candidates, con, optimum, comptableau)

for x in FRed(comptableau[:optimum] + comptableau[optimum + 1:]):
	print(x)
	print(ERCs(x))

# testing with exs from BP (2011)
ex90 = [['W', 'L', 'W'], ['e','W','L']]
#print(FRed(ex90))

ex96 = [['W', 'L', 'e', 'W'], ['e','W','L','W'], ['W','W','L','e'], ['W','L','W','e']]
#print(FRed(ex96))

ex98 = [['e','e','W','L'],['e','W','L','e'],['W','L','W','e'],['e','e','W','W'],['e','W','L','W'],['W','L','W','L'],['W','W','L','e']]
#print(FRed(ex98))

#print(ERCs(['W','W','L','L']))
