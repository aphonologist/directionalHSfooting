#import sys
from con import *
#from tablO import tablO
from fred import FRed

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

# underlying forms
urs = ['s' * i for i in range(2, 10)]

# parallel/serial gen
parallel = True

if parallel:
	from gen import gen_foot_parallel as gen
else:
	from gen import gen_foot as gen

# traditional/directional constraints
traditional = False

if traditional:
	con = [
		ParseSyllable('N'),
		Trochee('N'),
		Iamb('N'),
		FootLeft('N'),
		FootRight('N'),
		NonFinality('N'),
		FootFoot('N'),
		HdPrWd('N'),
		AllFtL(),
		AllFtR()
		]
else:
	con = [
		ParseSyllable('L'), ParseSyllable('R'),
		Trochee('L'), Trochee('R'),
		Iamb('L'), Iamb('R'),
		FootLeft('L'), FootLeft('R'),
		FootRight('L'), FootRight('R'),
		NonFinality('L'), NonFinality('R'),
		FootFoot('L'), FootFoot('R'),
		HdPrWd('L'), HdPrWd('R')
		]

typology = []

# (SKB, derivation)
for ur in urs:
	derivations = []

	stack = []
	stack.append((set(), (ur,)))

	while stack:
		derivation = stack.pop()

		# check for convergence
		if len(derivation[1]) > 1 and derivation[1][-2] == derivation[1][-1]:
			derivations.append(derivation)
			continue

		# Generate candidate set
		input = derivation[1][-1]
		candidates = sorted(list(gen(input)))

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
			unsat = False
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
				if 'W' not in row and 'L' in row:
					unsat = True
					break
			if unsat: continue

			#tablO(tableau, input, candidates, con, optimum, comptableau)

			# Run FRed on optimum
			SKB = FRed(comptableau[:optimum] + comptableau[optimum + 1:])

			if 'unsat' not in SKB:
				# combine ranking arguments
				combinedSKB = derivation[0].union(SKB)

				# check for inconsistency
				newSKB = FRed(combinedSKB)
				if 'unsat' not in newSKB:
					newderivation = (newSKB, derivation[1] + (candidates[optimum],))
					if parallel:
						derivations.append(newderivation)
					else:
						stack.append(newderivation)

	# combine derivations with previous derivations
	# (SKB, derivation, derivation, ...)
	if typology:
		new_languages = []
		while derivations:
			derivation = derivations.pop()
			for language in typology:
				combinedSKB = derivation[0].union(language[0])
				newSKB = FRed(combinedSKB)
				if 'unsat' not in newSKB:
					new_language = (newSKB,) + language[1:] + (derivation[1],)
					new_languages.append(new_language)
		typology = []
		while new_languages:
			typology.append(new_languages.pop())

	else:
		while derivations:
			typology.append(derivations.pop())

# representing in terms of stress patterns
stress_gram = {}

for language in sorted(typology):
	# get surface stress string
	stress = []
	feet = '\t'
	for derivation in language[1:]:
		rhythm = derivation[-1]
		for stressed_syllable in ['F', 'T', 'I']:
			rhythm = rhythm.replace(stressed_syllable, 'S')
		for unstressed_syllable in ['t', 'i']:
			rhythm = rhythm.replace(unstressed_syllable, 's')
		stress.append(rhythm)
		feet += derivation[-1] + '\t'
	feet += '\n'
	stress_tup = tuple(stress)
	if stress_tup not in stress_gram:
		stress_gram[stress_tup] = []

	# can constraints be collapsed for this language
	if traditional:
		direction_matters = [True for c in con]
		constraint_names = [c.name for c in con]
	else:
		direction_matters = []
		constraint_names = []
		for i in range(0, len(con) - 1, 2):
			matters = False
			for erc in language[0]:
				if erc[i] != erc[i+1]:
					matters = True
					break
			if matters:
				direction_matters += [True, True]
				constraint_names += [con[i].name, con[i+1].name]
			else:
				direction_matters += [False, False]
				constraint_names += [con[i].name[:-1] + 'L/R']

	# get derivation string
	deriv_str = ''
	for derivation in language[1:]:
		deriv_str += '\t/' + derivation[0] + '/\t[' + derivation[-1] + ']\n'
		deriv_str += '\t' + ' -> '.join(derivation) + '\n'

	# get constraint string
	con_str = '\t' + '\t'.join(constraint_names) + '\n'
	for erc in sorted(language[0]):
		con_str += '\t'
		i = 0
		while i < len(erc):
			con_str += erc[i] + '\t'
			if not direction_matters[i]:
				i += 1
			i += 1
		con_str += '\n'

	# add to dictionary
	stress_gram[stress_tup].append([feet, deriv_str, con_str])

for s in sorted(stress_gram, key=lambda x:[sum(y.count('S') for y in x), x], reverse=True):
	print(','.join(s))
	for g in sorted(stress_gram[s]):
		for x in g:
			print(x)
	print()
