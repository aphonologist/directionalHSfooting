import sys
files = sys.argv[1:]

typologies = {}
for file in files:
	typologies[file] = set()
	f = open(file)
	for line in f:
		linstr = line.rstrip()
		if linstr:
			if not linstr.startswith('\t'):
				typologies[file].add(linstr)
	f.close()
	print(file, 'contains', len(typologies[file]), 'languages')

print()

for f1 in range(len(files)):
	file1 = files[f1]
	for f2 in range(f1 + 1, len(files)):
		file2 = files[f2]
		if typologies[file1] == typologies[file2]:
			print(file1, file2, 'contain the same set of languages')
		else:
			f1_f2 = typologies[file1] - typologies[file2]
			if f1_f2:
				print('There are languages in', file1, 'that are not in', file2)
				for lang in sorted(f1_f2):
					print('\t', lang.strip())

				print()
				f = open(file1)
				state = 0
				for line in f:
					linstr = line.rstrip()
					if state == 0:
						if linstr in f1_f2:
							print(linstr)
							state = 1
					elif state == 1:
						if ',' not in linstr:
							print(linstr)
						else:
							if linstr in f1_f2:
								print(linstr)
							else:
								state = 0
				f.close()
				print()

			f2_f1 = typologies[file2] - typologies[file1]
			if f2_f1:
				print('There are languages in', file2, 'that are not in', file1)
				for lang in sorted(f2_f1):
					print('\t', lang.strip())

				print()
				f = open(file2)
				state = 0
				for line in f:
					linstr = line.rstrip()
					if state == 0:
						if linstr in f2_f1:
							print(linstr)
							state = 1
					elif state == 1:
							if ',' not in linstr:
								print(linstr)
							else:
								if linstr in f2_f1:
									print(linstr)
								else:
									state = 0
				f.close()
				print()

		print()
