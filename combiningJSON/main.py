import json

def openFile(name: str, filetype: str):
	with open(f"{name}.{filetype}") as file:
			file = json.load(file)
	return file

def multipleElements(text: str, stop=""):
	result = None
	elements = []
	while result != stop:
		result = input(text)
		if result != stop:
			try:
				elements.append(int(result))
			except:
				elements.append(result)
	return elements

def openElementsPath(path: list, var):
	for item in path:
		var = var[item]
	return var


def main():
	file1 = openFile(input("File 1 name (no extension): "), "JSON")
	path1keys = multipleElements("Describe path for keys: ")
	path1 = multipleElements("Describe path for list: ")
	file1keys = openElementsPath(path1keys, file1)
	file1 = openElementsPath(path1, file1)

	file2 = openFile(input("File 2 name (no extension): "), "JSON")
	path2keys = multipleElements("Describe path for keys: ")
	path2 = multipleElements("Describe path for list: ")
	file2keys = openElementsPath(path2keys, file2)
	file2 = openElementsPath(path2, file2)

	print(file1keys.keys())
	print(file2keys.keys())

	selection1 = multipleElements("Enter file 1 keys: ")
	selection2 = multipleElements("Enter file 2 keys: ")
	reps = max(len(file1), len(file2))
	new = []
	for i in range(reps):
		new.append({})
		for key in selection1:
			if key in file1keys.keys():
				try:
					new[i][key] = file1[i].get(key, None)
				except:
					pass
			else:
				selection1.remove(key)
		for key in selection2:
			if key in file2keys.keys():
				try:
					new[i][key] = file2[i].get(key, None)
				except:
					pass
			else:
				selection2.remove(key)
	print(new[0].keys())


main()