import itertools
import random
import string
import re
import sys
import time
import math
 
# constants and dictionary
yv = 'aeo'
yc = 'rst'
bv = 'i'
bc = 'bcdmp'
gv = 'u'
gc = 'gn'
pi = 'fwvhy'
og = 'lk'
pu = 'jx'
red = 'qz'

grid_letters = (red*3)+(pu*3)+(og*4)+(pi*6)+(gc*12)+(gv*9)+(bc*11)+(bv*8)+(yc*20)+(yv*34)
grid_height = 9
grid_width = 13

# returns a randomized grid, similar to word soup
def generate_grid():
	grid = []
	for _ in itertools.repeat(None, grid_height):
		grid_row = ''.join(random.choice(grid_letters) for _ in range(grid_width))
		grid.append(grid_row)
	return grid

grid = generate_grid()

alphabet = ''.join(set(''.join(grid)))


bogglable = re.compile('[' + alphabet + ']{3,}$', re.I).match

words = set(word.rstrip('\n') for word in open("/usr/share/dict/words") if bogglable(word))
prefixes = set(word[:i] for word in words
			   for i in range(2, len(word)+1))

score = {"a": 1, "c": 2, "b": 2, "e": 1, "d": 2, "g": 3, "f": 4, "i": 2, "h": 4, "k": 5, "j": 8, "m": 2, "l": 5, "o": 1, "n": 3, "q": 10, "p": 2, "s": 1, "r": 1, "u": 3, "t": 1, "w": 4, "v": 4, "y": 4, "x": 8, "z": 10}


# returns the best option with score and grid rating taken into account
# ERROR- SOMETIMES RETURNS NOTHING WHEN WORDS ARE AVAILABLE
# POSSIBLY DUE TO LESS THAN 40 OPTIONS BEING AVAILABLE- EXAMINE
def examine_options(griddle, stage):
	topscore = 0
	score = 0
	choice = ()
	if stage == 8:
		return sorted(solve(), key=lambda (word, path): score_word(word))
	if stage == 9:
		return sorted(solve2(griddle), key=lambda (word, path): score_word(word))
	if stage == 0:
		return max(solve(), key=lambda (word, path): score_word(word))
	options =  sorted(solve(), key=lambda (word, path): score_word(word))
	print 'options = ' + str(len(options))
	if len(options) > 50:
		options = options[:-50]
	for opt in options:
		newgrid = move_letters(grid, opt[0])
		score = evaluate_grid0(newgrid, stage) + (score_word(opt[0]))
		if score >= topscore:
			topscore = score
			choice = opt
	print 'score = ' + str(score)
	if choice == ():
		print options
		print 'LEN = ' + str(len(options))
	return choice

qumix1 = 50
qnum1 = 100

cmix2 = 2
zmix2 = 8
qumix2 = 25

ratrat2 = 350

sqrat2 = 0.1

znum2 = 12
qunum2 = 50

vratio2 = 0.7


cmix3 = 1
zmix3 = 4
qumix3 = 15

ratrat3 = 450

sqrat3 = 5

znum3 = 12
qunum3 = 50

vratio3 = 0.7


def evaluate_grid0(grid, stage):
	rating = 0
	mixrating = 1
	ratiorating = 1
	sqrating = 1
	#print letter_match(grid)[0] * 4
	#print letter_match(grid)[1] * 20
	#print letter_match(grid)[2] * 50
	#print vowel_ratio(grid)
	if stage == 1:
		rating += letter_match(grid)[2] * qumix1
		rating += letter_match(grid)[4] * qnum1	
		return 100000 + rating
	if stage == 2:
		mixrating += letter_match(grid)[0] * cmix2
		mixrating += letter_match(grid)[1] * zmix2
		mixrating += letter_match(grid)[2] * qumix2
		mixrating += letter_match(grid)[3] * znum2
		mixrating += letter_match(grid)[4] * qunum2
		ratiorating = abs(vowel_ratio(grid) - vratio2) * ratrat2
		sqrating = unsquareness(grid) * sqrat2

	if stage == 3:
		mixrating += letter_match(grid)[0] * cmix3
		mixrating += letter_match(grid)[1] * zmix3
		mixrating += letter_match(grid)[2] * qumix3
		mixrating += letter_match(grid)[3] * znum3
		mixrating += letter_match(grid)[4] * qunum3		
		ratiorating = abs(vowel_ratio(grid) - vratio3) * ratrat3
		sqrating = unsquareness(grid) * sqrat3
	#print 'mixrating = ' + str(mixrating)
	#print 'ratiorating = ' + str(ratiorating)
	#print 'sqrating = ' + str(sqrating)
	rating = 1000000 + mixrating - ratiorating - sqrating
	return rating

def evaluate_grid_display(grid, stage):
	rating = 0
	mixrating = 1
	ratiorating = 1
	sqrating = 1
	#print letter_match(grid)[0] * 4
	#print letter_match(grid)[1] * 20
	#print letter_match(grid)[2] * 50
	#print vowel_ratio(grid)
	if stage == 1:
		rating += letter_match(grid)[2] * qumix1
		rating += letter_match(grid)[4] * qnum1	
		return 100000 + rating
	if stage == 2:
		mixrating += letter_match(grid)[0] * cmix2
		mixrating += letter_match(grid)[1] * zmix2
		mixrating += letter_match(grid)[2] * qumix2
		mixrating += letter_match(grid)[3] * znum2
		mixrating += letter_match(grid)[4] * qunum2		
		ratiorating = abs(vowel_ratio(grid) - vratio2) * ratrat2
		sqrating = unsquareness(grid) * sqrat2
		print '----mixrating--cmix-zmix-qmix-znum-qnum'
		print 'mixrating = ' + str(mixrating) + "::" + str([letter_match(grid)[0]*cmix2]+[letter_match(grid)[1]*zmix2]+[letter_match(grid)[2]*qumix2]+[letter_match(grid)[3]*znum2]+[letter_match(grid)[4]*qunum2])

	if stage == 3:
		mixrating += letter_match(grid)[0] * cmix3
		mixrating += letter_match(grid)[1] * zmix3
		mixrating += letter_match(grid)[2] * qumix3
		mixrating += letter_match(grid)[3] * znum3
		mixrating += letter_match(grid)[4] * qunum3		
		ratiorating = abs(vowel_ratio(grid) - vratio3) * ratrat3
		sqrating = unsquareness(grid) * sqrat3
		print '----mixrating--cmix-zmix-qmix-znum-qnum'
		print 'mixrating = ' + str(mixrating) + "::" + str([letter_match(grid)[0]*cmix3]+[letter_match(grid)[1]*zmix3]+[letter_match(grid)[2]*qumix3]+[letter_match(grid)[3]*znum3]+[letter_match(grid)[4]*qunum3])

	#print 'mixrating = ' + str(mixrating)
	#print 'ratiorating = ' + str(ratiorating)
	#print 'sqrating = ' + str(sqrating)
	rating = 1000000 + mixrating - ratiorating - sqrating

	
	print 'ratiorating = ' + str(ratiorating)
	print 'sqrating = ' + str(sqrating)
	print 'rating = ' + str(rating)



#def evaluate_grid(grid, stage):
#	match_ratings = letter_match(grid)
#	vcount, ccount = vowel_ratio(grid)[0], vowel_ratio(grid)[1]
#	width, height, scount = squareness(grid)[0], squareness(grid)[1], squareness(grid)[2]
#	#print width
#	#print height
#	#print scount
#	#print vcount
#	#print ccount
#	rating = 0
#	if stage == 1:
#		rating += match_ratings[0]
#		rating += match_ratings[1] * 3
#		if match_ratings[2] > 0:
#			rating += 50 
#		rmix = (float(vcount)/float(ccount)) - .4
#		rating += -(rmix * rmix * 1500)
#		rating += (grid_width - (grid_width - width)) * 30
#		rating += (grid_height - (grid_height  - width)) * 60
#	if stage == 2:
#		rating += match_ratings[0] * 2
#		rating += match_ratings[1] * 5
#		if match_ratings[2] > 0:
#			rating += 50 		
#		rmix = (float(vcount)/float(ccount)) - .4
#		rating += - (rmix * rmix * 2000)
#		rating -= height * 15
#		rating -= width * 60
#	return rating
#
## returns the rating of the grid
#def evaluate_grid1(grid, stage):
#	match_ratings = letter_match(grid)
#	vcount, ccount = vowel_ratio(grid)[0], vowel_ratio(grid)[1]
#	#shape = widths(grid)
#	unsq = unsquareness(grid)
#	rating = 0
#	if stage == 1:
#		rating += match_ratings[0]
#		rating += match_ratings[1] * 3
#		if match_ratings[2] > 0:
#			rating += 50 
#		rmix = (float(vcount)/float(ccount)) - .4
#		rating += -(rmix * rmix * 1500)
#		rating -= unsq * 10
#		#rating += (grid_width - (grid_width - width)) * 30
#		#rating += (grid_height - (grid_height  - width)) * 60
#	if stage == 2:
#		rating += match_ratings[0] * 2
#		rating += match_ratings[1] * 5
#		if match_ratings[2] > 0:
#			rating += 50 		
#		rmix = (float(vcount)/float(ccount)) - .4
#		rating += - (rmix * rmix * 2000)
#		rating -= unsq * 10
#		#rating -= height * 15
#		#rating -= width * 60
#	return rating

	


# returns the rating of how well vowels and constanants match up
def letter_match(grid):
	cmixing = 0
	zmixing = 0
	qrating = 0
	znum = 0
	qnum = 0
	for y, row in enumerate(grid):
		for x, letter in enumerate(row):
			coord = [x]+[y]
			if letter == 'b' or letter == 'c' or letter == 'd' or letter == 'f' or letter == 'g' or letter == 'h' or letter == 'm' or letter == 'l' or letter == 'm' or letter == 'n' or letter == 'p' or letter == 'r' or letter == 't' or letter == 'w':
				for (nx, ny) in neighbors(coord):
					if grid[ny][nx] == 'a' or grid[ny][nx] == 'e' or grid[ny][nx] == 'i' or grid[ny][nx] =='o' or grid[ny][nx] == 'u':
						cmixing += 1				
			elif letter == 'z' or letter == 'j' or letter == 'k' or letter == 'v' or letter == 'x':
				znum += 1
				for (nx, ny) in neighbors(coord):
					if grid[ny][nx] == 'a' or grid[ny][nx] == 'e' or grid[ny][nx] == 'i' or grid[ny][nx] =='o' or grid[ny][nx] == 'u':
						zmixing += 1
			elif letter == 'q':
				qnum += 1
				for (nx, ny) in neighbors(coord):
					if grid[ny][nx] == 'u':
						qrating += 1
	rating = [cmixing] + [zmixing] + [qrating] + [znum] + [qnum]		
	return rating

# return number of vowels, consanants, and stars
def vowel_ratio(grid):
	vcount = 0
	ccount = 0
	for y, row in enumerate(grid):
		for x, letter in enumerate(row):
			if letter == 'a' or letter == 'e' or letter == 'i' or letter =='o' or letter == 'u':
				vcount += 1
			else:
				ccount +=1
	#print vcount
	#print ccount
	return float(vcount)/(ccount+vcount)

# returns how the sums of the squares of each row's deviation from the average (only when larger)
def unsquareness(grid):
	ws = widths(grid)
	level = math.sqrt(float(sum(ws)))
	deviation = 0
	for row in ws:
		deviation += (abs(level-row))**3
	return deviation/len(ws)
	#avg = sum(ws)/len(ws)
	#for row in ws:
	#	if row >= avg:
	#		deviation += (avg-row)**2
	#return deviation + 1



def squareness(grid):
	width = grid_width - grid[0].count('*')
	height = grid_height
	scount = 0
	for y, row in enumerate(grid):
		scount += row.count('*')
		if row.count('*') != grid_width:
			height = y + 1
	result = [width] + [height] + [scount]
	return result


# returns the width of each row
def widths(grid):
	widths = []
	for row in grid:
		if row.count('*') != grid_width:
			widths.append(grid_width - row.count('*'))
	return widths


#def cvmatch


# all stages:
# 1. match up Qs and Us
# 2. match up ZXJKV with vowels
# later stages:
# 1. make the grid square
# 2. regulate vowel frequency
# 3. towards the end, start looking for clearances



#print grid


#grid = "fxie amlo ewbx astu".split()
#nrows, ncols = len(grid), len(grid[0])

# A dictionary word that could be a solution must use only the grid's
# letters and have length >= 3. (With a case-insensitive match.)
def triplemove(grid):
	scorelist = []
	score1 = 0
	score2 = 0
	options1 =  sorted(solve(), key=lambda (word, path): score_word(word))[-5:]
	for opt1 in options1:
		grid = move_letters(grid, opt1[1])
		options2 = sorted(solve(), key=lambda (word, path): score_word(word))[-5:]
		for opt2 in options2:
			grid = move_letters(grid, opt2[1])
			topword =  max(solve(), key=lambda (word, path): score_word(word))
			total_score = score_word(topword[0]) + score_word(opt2[0]) + score_word(opt1[0])
			print total_score
			scorelist.append(total_score)
	return max(scorelist)

#def clear_grid(grid):
#	options1 =  (solve(), key=lambda (word, path): score_word(word))
#	for opt1 in options1:
#		grid = move_letters(grid, opt1[1])
#		options2 = (solve(), key=lambda (word, path): score_word(word))[-5:]
#		for opt2 in options2:
#			grid = move_letters(grid, opt2[1])
#			topword = (solve(), key=lambda (word, path): score_word(word))

# returns word score according to word soup rules
def score_word(word):
  return (sum([score[c] for c in word]) * len(word))

# finds all words in grid
def solve():
	for y, row in enumerate(grid):
		for x, letter in enumerate(row):
			if letter != '*':
				for result in extending(letter, ((x, y),)):
					yield result

# yields possible next steps in path to make words
def extending(prefix, path):
	if prefix in words:
		yield (prefix, path)
	for (nx, ny) in neighbors(path[-1]):
		if (nx, ny) not in path:
			prefix1 = prefix + grid[ny][nx]
			if prefix1 in prefixes:
				for result in extending(prefix1, path + ((nx, ny),)):
					yield result

# yields letter's neighbours in grid
def neighbors((x, y)):
	for nx in range(max(0, x-1), min(x+2, len(grid[0]))):
		for ny in range(max(0, y-1), min(y+2, len(grid))):
			yield (nx, ny)

def solve2(grid):
	for y, row in enumerate(grid):
		for x, letter in enumerate(row):
			if letter != '*':
				for result in extending2(letter, ((x, y),), grid):
					yield result

def extending2(prefix, path, grid):
	if prefix in words:
		yield (prefix, path)
	for (nx, ny) in neighbors2(path[-1], grid):
		if (nx, ny) not in path:
			prefix1 = prefix + grid[ny][nx]
			if prefix1 in prefixes:
				for result in extending2(prefix1, path + ((nx, ny),), grid):
					yield result

# yields letter's neighbours in grid
def neighbors2((x, y,), grid):
	for nx in range(max(0, x-1), min(x+2, len(grid[0]))):
		for ny in range(max(0, y-1), min(y+2, len(grid))):
			yield (nx, ny)

# prints topword, path, and score
def display_word(topword):
	print topword
	if len(topword) > 0:		
		print "word score = " + str(score_word(topword[0]))
	

# rearranges grid after words are found
def move_letters(grid, empty_points):
	newgrid = [list(row) for row in grid]
	empty_points = [list(pair) for pair in empty_points]
	for y, row in enumerate(newgrid):
		for x, letter in enumerate(row): #look at all squares
			for point in empty_points:
				if x == point[0] and y == point[1]: #if empty matches square location
					#print 'check 1'
					#print empty_points
					location = [x, y]
					#print location
					while location in empty_points:
						#print 'check 2'
						for j, r in enumerate(newgrid): 
							for i, l in enumerate(r): #look at all squares
								if j >= y and x == i:   # and see which are above it
									if j == grid_height-1:
										newgrid[j][i] = '*'
										#print 'star'
									else:
										newgrid[j][i] = newgrid[j+1][i] #copy  upper neighbour onto lower in all of column 
										#print newgrid[j][i] + ' to ' + newgrid[j+1][i] + ' at ' + str(x) +', ' + str(y)
						for p in empty_points:
							if p[0] == x:
								p[1] -= 1
								#print 'empty lowered'
	newgrid2 = []
	for row in newgrid:
		stars = row.count('*')
		row[:] = (value for value in row if value != "*")
		if stars == 0:
			newgrid2.append(row)
		else:            
			for _ in itertools.repeat(None, stars):
				row = ['*'] + row
			newgrid2.append(row)
	resultgrid = []
	for row in newgrid2:
		resultgrid.append(''.join(row))
	return resultgrid

def find_squares(original_grid):
	start = time.time()
	routes = []
	squares = []
	grid = original_grid
	options1 = examine_options(original_grid, 8)[:-20:-2]
	counter = [0,0,0,0]
	for opt1 in options1:
		counter[0] +=1
		moves = [(),(),()]
		moves[0] = opt1
		grid2 = move_letters(original_grid, opt1[1])
		grid = grid2
		options2 = examine_options(grid2, 8)[:-80:-1]
		for opt2 in options2:
			counter[1] +=1
			moves[1] = opt2
			grid3 = move_letters(grid2, opt2[1])
			wid = widths(grid3)
			if 2 < len(wid) < 5 and 2 < wid[0] <= wid[1] + 1 <= wid[2] + 2 < 7 and moves not in routes:
				routes.append(moves)
				squares.append(grid3)
				print '----------'
				for row in reversed(grid3):
					print row 
				print '----------'
				print grid3
			grid = grid3
			options3 = examine_options(grid3, 8)[::-1]
			for opt3 in options3:
				counter[2] +=1
				moves[2] = opt3			
				grid4 = move_letters(grid3, opt3[1])
				grid = grid4
				wid = widths(grid4)
				if 2 < len(wid) < 5 and 2 < wid[0] <= wid[1] + 1 <= wid[2] + 2 < 7 and moves not in routes:
					routes.append(moves)
					squares.append(grid4)
					print '----------'
					for row in reversed(grid4):
						print row 
					print '----------'
					print grid4
					if time.time() - start > 30:
						print 'TIMEOUT'
						print len(routes)
						print counter
						return [routes] + [squares]

	return [routes] + [squares]




def finish(original_grid):
	timeout = 10
	finish_start = time.time()
	complete = ['*'*grid_width]*grid_height
	result = [(),(),(),()]
	grid = original_grid
	options1 = examine_options(original_grid, 9)[::-7]
	timer = time.time()
	for opt1 in options1:
		result[0] = opt1
		grid1 = move_letters(original_grid, opt1[1])
		grid = grid1
		if grid1 == complete:
			return result		
		options2 = examine_options(grid1, 9)[::-3]
		for opt2 in options2:
			result[1] = opt2
			grid2 = move_letters(grid1, opt2[1])
			grid = grid2
			if grid2 == complete:
				print '----------'
				for row in reversed(original_grid):
					print row 
				print '----------'
				for row in reversed(grid1):
					print row 
				print '----------'
				for row in reversed(grid2):
					print row 
				print time.time() - timer
				return result
				return result
			if time.time() - finish_start > timeout:
				print 'TIMEOUT2'
				return None
			options3 = examine_options(grid2, 9)
			for opt3 in options3:
				result[2] = opt3
				grid3 = move_letters(grid2, opt3[1])
				if grid3 == complete:
					print '----------'
					for row in reversed(original_grid):
						print row 
					print '----------'
					for row in reversed(grid1):
						print row 
					print '----------'
					for row in reversed(grid2):
						print row 
					print '----------'
					for row in reversed(grid3):
						print row
					print time.time() - timer
					return result
				options4 = reversed(examine_options(grid3, 9))
				for opt4 in options4:
					result[3] = opt4
					grid4 = move_letters(grid3, opt4[1])
					if grid4 == complete:
						print '----------'
						for row in reversed(original_grid):
							print row 
						print '----------'
						for row in reversed(grid1):
							print row 
						print '----------'
						for row in reversed(grid2):
							print row 
						print '----------'
						for row in reversed(grid3):
							print row
						print '----------'
						for row in reversed(grid4):
							print row							
						return result
						if time.time() - finish_start > timeout:
							print result
							print grid
							print 'TIMEOUT4'
	if grid == complete:
		return result
	else:
		print 'NO SOLUTION'



timeout = 0 
letter_count = grid_height*grid_width
total_score = 0

print alphabet
for row in reversed(grid):
	print row 

while letter_count > 90 and timeout < 30:
	print '+++STAGE 1'

	topword =  examine_options(grid, 1)

	display_word(topword)

	letter_count -= len(topword[0])

	grid = move_letters(grid, topword[1])

	total_score += score_word(topword[0])
	print 'letter count = ' + str(letter_count)
	evaluate_grid_display(grid, 1)

	timeout += 1
	for row in reversed(grid):
		print row
	print grid

s1grid = grid

while letter_count > 55 and timeout < 50:
	print '+++STAGE 2'
	topword = examine_options(grid, 2)


	display_word(topword)

	if len(topword) > 0:
		letter_count -= len(topword[0])
		print 'letter count = ' + str(letter_count)


	if topword != ():
		grid = move_letters(grid, topword[1])
		total_score += score_word(topword[0])	
	else:
		print 'complete'
		timeout = 50

	print 'total score = ' + str(total_score)

	evaluate_grid_display(grid, 2)
	timeout += 1
	for row in reversed(grid):
		print row 
	print grid

s2grid = grid

while letter_count > 18 and timeout < 50:
	print '+++STAGE 3'
	topword = examine_options(grid, 3)


	display_word(topword)

	if len(topword) > 0:
		letter_count -= len(topword[0])
		print 'letter count = ' + str(letter_count)


	if topword != ():
		grid = move_letters(grid, topword[1])
		total_score += score_word(topword[0])	
	else:
		print 'complete'
		timeout = 50

	print 'total score = ' + str(total_score)

	evaluate_grid_display(grid, 3)
	timeout += 1
	for row in reversed(grid):
		print row
	print grid

s3grid = grid 		
print "+++FINISHING"
print grid
finish(grid)


#print find_squares(grid)
print "+++DONE"

#	print 'l = ' + str(letter_count)
for row in reversed(grid):
	print row 
print grid

print 'total score = ' + str(total_score)

print '++++++++++++++++++++'	
for row in reversed(s1grid):
	print row 
print '++++++++++++++++++++'
for row in reversed(s2grid):
	print row 
print '++++++++++++++++++++'	

for row in reversed(s3grid):
	print row 
print '++++++++++++++++++++'	









