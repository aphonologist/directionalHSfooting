# point-wise fusion
def fuse(a, b):
	if a == 'L' or b == 'L': return 'L'
	if a == 'e': return b
	if b == 'e': return a
	return 'W'

# function to fuse an entire comparative tableau
def fuse_tableau(A):
	if not A:
		return ()
	fuse_all = ['e'] * len(A[0])
	for v in A:
		fuse_all = [fuse(a,b) for a,b in zip(fuse_all, v)]
	return tuple(fuse_all)

# FRed: A is a comparative tableau
def FRed(A):
#	MIB = set()
	SKB = set()

	# Step 0: if A is empty, then FNF is empty
	if not A:
		return set()

	cols = len(A[0])

	# Step 1: fuse the entire tableau
	HoldFus = fuse_tableau(A)

	# Step 2: collect info loss residues
	ILC = []

	# info loss configurations:
	# columns i where HoldFus[i] = W and there's an e in some vector
	fused_Ws = [i for i in range(cols) if HoldFus[i] == 'W']
	for col in fused_Ws:
		for row in range(len(A)):
			if A[row][col] == 'e':
				ILC.append(col)
				continue

	# residue - vectors with e in col i where i is in ILC
	Res = []
	TR = []
	for col in ILC:
		Res.append([])
		for v in A:
			if v[col] == 'e':
				Res[-1].append(tuple(v))
				TR.append(tuple(v))

	# Step 3: check entailment
	fused_A = fuse_tableau(A)

	# return skeletal basis
	if fused_A and 'W' not in fused_A and 'e' not in fused_A:
		return ('unsat,')
	s = [x for x in fused_A]
	fuse_res = fuse_tableau(TR)
	for k in range(len(fuse_res)):
		if fuse_res[k] == 'L':
			s[k] = 'e'
	if 'L' not in s and 'e' not in s:
		HoldFus = ()
	else:
		SKB.add(tuple(s))

	# return maximally informative basis
#	# if fused tableau is all W, then no ranking info
#	if 'L' not in fused_A and 'e' not in fused_A:
#		HoldFus = ()
#	# if fused tableau is all L, then unsatisfiable
#	elif 'W' not in fused_A and 'e' not in fused_A:
#		return ('unsat',)
#	# if total residue entails fused tableau, then no ranking info
#	# i.e., if they have same number of Ls
#	else:
#		fuse_res = fuse_tableau(TR)
#		if fuse_res.count('L') == fused_A.count('L'):
#			HoldFus = ()
#		else:
#			MIB.add(HoldFus)

	# Step 4: recurse on the residue
	for res in Res:
#		MIB = MIB.union(FRed(res))
		SKB = SKB.union(FRed(res))

	if ('unsat',) in SKB:
		return ('unsat',)

#	return MIB
	return SKB
