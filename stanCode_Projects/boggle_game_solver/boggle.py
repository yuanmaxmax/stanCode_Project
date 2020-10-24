"""
File: boggle.py
Name:Max Chang
----------------------------------------
TODO:
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it

import time

# Constant
FILE = 'dictionary.txt'
SIZE = 4				# boggle game size
MIN_LENGTH = 4			# minimum length of found words

# Global Variablds
dictionary = [set() for i in range(26)]		# Dictonary
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'     # Alphabet index
panel = [list() for i in range(SIZE)]		# The game panel
find = []									# The found word

def main():
	"""
	TODO:
	"""
	read_dictionary()
	print('Welcome to stanCode boggle game')
	create_panel()
	tStart = time.time()
	find_boggle()
	tEnd = time.time()
	print(f'There are {len(find)} words in total')
	print(f"Use {tEnd - tStart} seconds")


def create_panel():
	"""
	Create game panel from user input
	"""
	for i in range(SIZE):
		while  True:
			data = input(f'{i+1} row of letters:')
			data = data.split()
			if len(data) == SIZE:
				for j in range(SIZE):
					if len(data[j]) == 1 and data[j].isalpha():
						panel[i].append([data[j].lower(), 0])
			if len(panel[i]) == SIZE:
				break
			else:
				print('Illegal Format')
				panel[i] = []


def read_dictionary():
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	with open(FILE, 'r') as f:
		for line in f:
			dictionary[ALPHABET.find(line[0])].add(line.lower().strip())


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	for element in dictionary[ALPHABET.find(sub_s[0])]:
		if element.startswith(sub_s):
			return True
	return False


def find_boggle():
	"""
	Find the word from boggle panel
	"""
	for i in range(SIZE):
		for j in range(SIZE):
			panel[i][j][1] = 1
			boggle_helper(i, j, panel[i][j][0])
			panel[i][j][1] = 0


def boggle_helper(x, y, chosen):
	"""
	Boggle DFS search recurrsion
	:param x: (int) the index of start x coordinate
	:param y: (int) the index of start y coordinate
	:param chosen: (string) the string that have already chosen
	"""
	if len(chosen) >= MIN_LENGTH:
		check(chosen)
	for i in range(-1, 2):
		if 0 <= x+i < SIZE:
			for j in range(-1, 2):
				if 0 <= y+j < SIZE:
					if not panel[x+i][y+j][1] and has_prefix(chosen + panel[x+i][y+j][0]):
						panel[x+i][y+j][1] = 1
						boggle_helper(x+i, y+j, chosen + panel[x+i][y+j][0])
						panel[x+i][y+j][1] = 0


def check(chosen):
	"""
	Check if a string is in the dictionary
	:param chosen: (str) The string to be check if in dictionary
	"""
	if chosen in dictionary[ALPHABET.index(chosen[0])] and chosen not in find:
		print(f'Found: "{chosen}"')
		find.append(chosen)


if __name__ == '__main__':
	main()
