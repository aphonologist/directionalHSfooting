#import sys
import alph
from con import *
from gen import gen
from tablO import tablO
from fred import FRed
#from itertools import combinations

# command line parameter to control printing
#verbose = '-v' in sys.argv

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
		WLs.append(tuple(WL))

	return WLs

alpha = ['l', 'L']
alph.initialize(alpha)
urs = ['l','ll','llllll', 'lllllll']

# Pruitt (2010, 2012)
#filename = 'pruitt20102012'
#con = [ParseSyllable('N'), Trochee('N'), Iamb('N'), FtBin('N'), AllFtL(), AllFtR()]

# Directional typology!
filename = 'directional-iterative'
con = [ParseSyllable('L'), ParseSyllable('R'), Trochee('L'), Trochee('R'), Iamb('L'), Iamb('R'), FtBin('L'), FtBin('R'), EdgeFoot('L'), EdgeFoot('R')]

typology = []

# ([FNF], derivation)
for ur in urs:
	derivations = []

	stack = []
	stack.append(([], (ur,)))

	while stack:
		derivation = stack.pop()

		# check for convergence
		if len(derivation[1]) > 1 and derivation[1][-2] == derivation[1][-1]:
			derivations.append(derivation)
			continue

		# Generate candidate set
		input = derivation[1][-1]
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

			# Run FRed on optimum
			FNF = FRed(comptableau[:optimum] + comptableau[optimum + 1:])

			if 'unsat' not in FNF:
				# combine ranking arguments
				combinedFNF = derivation[0][:]
				for fnf in FNF:
					combinedFNF.append(list(fnf))

				# check for inconsistency
				newFNF = FRed(combinedFNF)
				if 'unsat' not in newFNF:
					newderivation = (list(newFNF)[:], derivation[1] + (candidates[optimum],))
					stack.append(newderivation)

	# combine derivations with previous derivations
	if typology:
		toadd = []
		while derivations:
			derivation = derivations.pop()
			for language in typology:
				combinedFNF = derivation[0][:] + language[0][:]
				newFNF = FRed(combinedFNF)
				if 'unsat' not in newFNF:
					newlanguage = (list(newFNF)[:],) + language[1:] + (derivation[1],)
					toadd.append(newlanguage)
		typology = []
		while toadd:
			typology.append(toadd.pop())

	else:
		while derivations:
			typology.append(derivations.pop())
#	else:
#		while derivations:
#			d1 = derivations.pop()
#			for d2 in typology:
#				combinedFNF = d1[0][:] + d2[0][:]
#				newFNF = FRed(combinedFNF)
#				if 'unsat' not in newFNF:
#					language = (list(newFNF)[:],) + d2[1:] + d1[2:]
#					typology.append(language)
#					for x in language[1:]:
#						print(x[0],x[-1])

#count = 0
# combine derivations
#combined = combinations(derivations, len(urs))
#for combo in combined:
#	print('combo', count)
#	count += 1
#	comboFNF = []
#	for derivation in combo:
#		comboFNF += derivation[0][:]

#	derivs = [derivation[1] for derivation in combo]

	# check for inconsistency
#	newFNF = FRed(comboFNF)
#	if 'unsat' not in newFNF:
#		language = (list(newFNF)[:], derivs)
#		typology.append(language)

outstr = '\t'.join(x.name for x in con) + '\n'

for language in typology:
	for chain in language[1:]:
		outstr += chain[0] + '\t' + chain[-1] + '\n'

	ERCS = set()
	for cv in language[0]:
		ERC = ERCs(cv)
		for erc in ERC:
			ERCS.add(erc)

	# collapse ercs on direction
	collapseset = set()
	for constraint in con:
		if constraint.direction in ['L', 'R']:
			n = constraint.name[:-1]
			d = constraint.direction
			b = 'L'
			if d == 'L': b = 'R'
			dset = set()
			bset = set()
			for erc in ERCS:
				for e in erc:
					espl = [con[int(x)].name for x in e.split('>>')]
					if espl[0][:-1] == espl[1][:-1]: continue
					if espl[0][:-1] == n:
						if espl[0][-1] == d:
							dset.add(('',espl[1]))
						elif espl[0][-1] == b:
							bset.add(('',espl[1]))
					if espl[1][:-1] == n:
						if espl[1][-1] == d:
							dset.add((espl[0],''))
						elif espl[1][-1] == b:
							bset.add((espl[0],''))
			if dset == bset:
				collapseset.add(n)
	collapsedERCS = {}
	for erc in ERCS:
		for e in erc:
			espl = [con[int(x)].name for x in e.split('>>')]
			if espl[0][:-1] in collapseset:
				espl[0] = espl[0][:-1]
			if espl[1][:-1] in collapseset:
				espl[1] = espl[1][:-1]
			if espl[0] not in collapsedERCS:
				collapsedERCS[espl[0]] = set()
			collapsedERCS[espl[0]].add(espl[1])

	# remove transitive edges
	visited = set()

	def visit(v):
		if v not in visited:
			visited.add(v)
			indirect = set()
			if v in collapsedERCS:
				for w in collapsedERCS[v]:
					visit(w)
					# run bfs to find descendents of w
					queue = [w]
					discovered = set()
					while queue:
						x = queue.pop()
						if x in collapsedERCS:
							for y in collapsedERCS[x]:
								if y not in discovered:
									discovered.add(y)
									queue = [y] + queue
					indirect = indirect.union(discovered)
				for ind in indirect:
					collapsedERCS[v].remove(ind)

	for v in collapsedERCS:
		visit(v)

	for ce in collapsedERCS:
		outstr += ce + '\t' + '\t'.join(collapsedERCS[ce]) + '\n'
	outstr += '\n'

f = open('results/' + filename + '.tsv', 'w')
f.write(outstr)
f.close()
