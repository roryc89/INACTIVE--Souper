import itertools
import random
import string
import re
import sys
import time
 

#methods
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
grid_height = 3
grid_width = 3

# returns a randomized grid, similar to word soup
def generate_grid():
	grid = []
	for _ in itertools.repeat(None, grid_height):
	    grid_row = ''.join(random.choice(grid_letters) for _ in range(grid_width))
	    grid.append(grid_row)
	return grid

grid = generate_grid()


# contants and dictionary





alphabet = ''.join(set(''.join(grid)))
print alphabet


bogglable = re.compile('[' + alphabet + ']{3,}$', re.I).match

words = set(word.rstrip('\n') for word in open("/usr/share/dict/words") if bogglable(word))
prefixes = set(word[:i] for word in words
               for i in range(2, len(word)+1))

score = {"a": 1, "c": 2, "b": 2, "e": 1, "d": 2, "g": 3, "f": 4, "i": 2, "h": 4, "k": 5, "j": 8, "m": 2, "l": 5, "o": 1, "n": 3, "q": 10, "p": 2, "s": 1, "r": 1, "u": 3, "t": 1, "w": 4, "v": 4, "y": 4, "x": 8, "z": 10}


# returns the best option with score and grid rating taken into account
# ERROR- SOMETIMES RETURNS NOTHING WHEN WORDS ARE AVAILABLE
# POSSIBLY DUE TO LESS THAN 40 OPTIONS BEING AVAILABLE- EXAMINE
def examine_options(grid, stage):
	topscore = 0
	score = 0
	choice = ()	
	options =  sorted(solve(), key=lambda (word, path): score_word(word))[-20:]
	print 'NUMBER = ' + str(len(options))
	if len(options) < 40:
		options = sorted(solve(), key=lambda (word, path): score_word(word))
	for opt in options:
		newgrid = move_letters(grid, opt[1])
		score = evaluate_grid(newgrid, stage) + (score_word(opt[0] * 2))
		if score > topscore:
			topscore = score
			choice = opt
	if choice == ():
		print options
		print 'LEN = ' + str(len(options))
	return choice


# returns the rating of the grid
def evaluate_grid(grid, stage):
	match_ratings = letter_match(grid)
	vcount, ccount = vowel_ratio(grid)[0], vowel_ratio(grid)[1]
	width, height, scount = squareness(grid)[0], squareness(grid)[1], squareness(grid)[2]
	#print width
	#print height
	#print scount
	#print vcount
	#print ccount
	rating = 0
	if stage == 1:
		rating += match_ratings[0]
		rating += match_ratings[1] * 3
		if match_ratings[2] > 0:
			rating += 50 
		rmix = (float(vcount)/float(ccount)) - .4
		rating += -(rmix * rmix * 1500)
		rating += (grid_width - (grid_width - width)) * 30
		rating += (grid_height - (grid_height  - width)) * 60
	if stage == 2:
		rating += match_ratings[0] * 2
		rating += match_ratings[1] * 5
		if match_ratings[2] > 0:
			rating += 50 		
		rmix = (float(vcount)/float(ccount)) - .4
		rating += - (rmix * rmix * 2000)
		rating -= height * 15
		rating -= width * 60
	return rating

	


# returns the rating of how well vowels and constanants match up
def letter_match(grid):
	crating = 0
	zrating = 0
	qrating = 0
	for y, row in enumerate(grid):
		for x, letter in enumerate(row):
			coord = [x]+[y]
			if letter == 'b' or letter == 'c' or letter == 'd' or letter == 'f' or letter == 'g' or letter == 'h' or letter == 'm' or letter == 'l' or letter == 'm' or letter == 'n' or letter == 'p' or letter == 'r' or letter == 't' or letter == 'w':
				for (nx, ny) in neighbors(coord):
					if grid[ny][nx] == 'a' or grid[ny][nx] == 'e' or grid[ny][nx] == 'i' or grid[ny][nx] =='o' or grid[ny][nx] == 'u':
						crating += 1				
			elif letter == 'z' or letter == 'j' or letter == 'k' or letter == 'v' or letter == 'x':
				for (nx, ny) in neighbors(coord):
					if grid[ny][nx] == 'a' or grid[ny][nx] == 'e' or grid[ny][nx] == 'i' or grid[ny][nx] =='o' or grid[ny][nx] == 'u':
						zrating += 1
			elif letter == 'q':
				for (nx, ny) in neighbors(coord):
					if grid[ny][nx] == 'u':
						qrating += 1
	rating = [crating] + [zrating] + [qrating]			
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
	return [vcount]+[ccount]

# returns height and width of grid and number of stars
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
			else:
				print 'star found'

def solve2(grida):
    for y, row in enumerate(grida):
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

# prints topword, path, and score
def display_word(topword):
	print topword
	if len(topword) > 0:		
		print score_word(topword[0])
	

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


def finish(original_grid):
	finish_start = time.time()
	complete = ['*'*grid_width]*grid_height
	result = [(),(),()]
	grida = original_grid
	options1 =  sorted(solve2(grida), key=lambda (word, path): score_word(word))
	print 'pos = ' + str(len(options1))
	for opt1 in options1:
		result[0] = opt1
		grid1 = move_letters(grid, opt1[1])
		if grid1 == complete:
			return result
		else:
			grida = grid1
			options2 = sorted(solve2(grida), key=lambda (word, path): score_word(word))
			for opt2 in options2:
				result[1] = opt2
				grid2 = move_letters(grid1, opt2[1])
				if grid2 == complete:
					return result
				elif time.time() - finish_start > 20:
					print 'TIMEOUT'
					return None
				else:
					grida = grid2
					options3 = sorted(solve2(grida), key=lambda (word, path): score_word(word))
					for opt3 in options3:
						result[2] = opt3
						grid3 = move_letters(grid2, opt3[1])
						if grid3 == complete:
							for row in reversed(grid1):
								print row 
							for row in reversed(grid2):
								print row 
							for row in reversed(grid3):
								print row 																
							return result
#						else:				
#							options4 = sorted(solve(), key=lambda (word, path): score_word(word))
#							print 'grid 3'
#							print grid3
#							for opt4 in options4:
#								result[3] = opt4
#								grid4 = move_letters(grid3, opt4[1])
#								if grid4 == ['****']*4:
#									return result
#								else:
#									options5 = sorted(solve(), key=lambda (word, path): score_word(word))
#									print 'grid 4'
#									print grid4
#									for opt5 in options5:
#										result[4] = opt4
#										grid5 = move_letters(grid4, opt5[1])
#										if grid5 == ['******']*5:	
#											return result
#										else:							
#											options6 = sorted(solve(), key=lambda (word, path): score_word(word))
#											print 'grid 4'
#											print grid4	
#											for opt6 in options6:
#												result[5] = opt6
#												grid6 = move_letters(grid5, opt6[1])
#												print 'grid 5'
#												print grid5
#												if grid6 == ['******']*5:
#													return result
	if grid == complete:
		return result
	else:
		print 'NO SOLUTION'


grid = generate_grid()
for row in reversed(grid):
	print row 

timeout = 0 
letter_count = grid_height*grid_width
total_score = 0
start = time.time()
								
																																				
result = finish(grid)
print result
print time.time() - start





