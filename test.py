# just horizontal checks
# still need to add vertical and diaganol checks

import random
# count the number of wins
wins = 0

# repeat the whole program
for i in range(100000):
	# how many positions are in each row (rect.w / size[0])
	rowLength = 10
	# get a random list of 1 and 0 to represent placed player list
	allPos = [random.randint(0, 1) for i in range(30)]
	random.shuffle(allPos)

	# which player to check win for
	player = 0

	# count which row is active
	row = rowLength
	for startIndex in range(len(allPos)):
		# check if the end of the row is at least 4 indexs away
		if startIndex + 4 <= row:
			# check if the start point is the player we are checking for
			if allPos[startIndex] == player:
				# create a set with start index
				indexs = set([startIndex])
				currentIndex = startIndex
				# check 4 indexs to the right 
				for i in range(4):
					# check if current index will go past the list length
					if currentIndex + 1 <= len(allPos):
						# check if the current position is the same as player
						if allPos[currentIndex] == player:
							# add index to the set because it is the same as the player and is adjacent to another player block
							indexs.add(currentIndex)
							# go to the next block
							currentIndex += 1
						else:
							# encounterd a block of opposite type
							break
					else:
						# index is at the end of the list
						break

				# check for 4 in a row
				if len(indexs) >= 4:
					print(indexs)
					wins += 1
				indexs = set([startIndex])
		# check if at the end of the row
		if startIndex + 1 >= row:
			row += rowLength
				

	string = "\n 0"
	for k in range(len(allPos) - 1):
		string += ", {}".format(k + 1)
	print(string)
	positions = ""
	for i, pos in enumerate(allPos):
		if i % rowLength == 0:
			positions += "| {}".format(str(pos))
		else:
			positions += ", {}".format(str(pos))
	print(positions)
	print("\n")

print("\nWins: ", wins)