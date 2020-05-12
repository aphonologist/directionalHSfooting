# point-wise fusion
def fuse(a, b):
	if a == 'L' or b == 'L': return 'L'
	if a == 'e': return b
	if b == 'e': return a
	return 'W'

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
		return []

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

	return set([tuple(fnf) for fnf in FNF if fnf])
