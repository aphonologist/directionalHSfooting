# point-wise fusion
def fuse(a, b):
	if a == 'L' or b == 'L': return 'L'
	if a == 'e': return b
	if b == 'e': return a
	return 'W'

# FRed
def FRed(comptableau):
	FNF = set([])

	# if A is empty, then FNF is empty
	if not comptableau:
		return set([])

	cols = len(comptableau[0])

	# Fuse the entire tableau
	fuseall = ['e'] * cols

	# Residuals - collect vectors with an 'e' in col i
	res = []
	for c in range(cols):
		res.append([])

	for row in comptableau:
		fuseall = [fuse(a,b) for a,b in zip(fuseall, row)]
		for c in range(cols):
			if row[c] == 'e':
				res[c].append(row)

	holdfus = [tuple(fuseall)]

	# Update residuals - keep only cols with 'W' in fuseall
	for c in range(cols):
		if fuseall[c] != 'W':
			res[c] = []

	# Check entailments

	# if fuseall is all 'W', then no ranking info
	if 'L' not in fuseall and 'e' not in fuseall:
		holdfus = []

	# if fuseall is all 'L', then unsatisfiable
	if 'W' not in fuseall:
		return ('unsat',)

	# does the set of residuals entail fuseall?

	# fuse residuals
	fuseres = ['e'] * cols
	for c in range(cols):
		for r in res[c]:
			fuseres = [fuse(a,b) for a,b in zip(fuseres, r)]

	# fuseres entails fuseall if they have the same number of 'L's
	if fuseres.count('L') == fuseall.count('L'):
		holdfus = []

	if holdfus:
		FNF.add(tuple(fuseall))

	# recurse on the residuals
	for c in range(cols):
		FNF = FNF.union(FRed(res[c]))

	if ('unsat',) in FNF:
		return ('unsat',)

	return FNF
