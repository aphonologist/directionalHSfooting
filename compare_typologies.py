import sys
files = sys.argv[1:]

typologies = {}
for file in files:
	typologies[file] = set()
	f = open(file)
	for line in f:
		if not line.startswith('\t'):
			typologies[file].add(line.strip())
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
			f2_f1 = typologies[file2] - typologies[file1]
			if f2_f1:
				print('There are languages in', file2, 'that are not in', file1)
				for lang in sorted(f2_f1):
					print('\t', lang.strip())
		print()
