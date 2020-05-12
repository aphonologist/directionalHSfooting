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
