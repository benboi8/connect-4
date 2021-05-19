# still need to add diagonal checks

# test vertical checks

import random

# horizontal checks
def HorizontalCheck():
	# count the number of wins
	wins = 0

	# repeat the whole program
	for i in range(1):
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
					

		string = "\n  0"
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


# vertical checks
def VerticalCheck():
	# count the number of wins
	wins = 0

	# repeat the whole program
	for i in range(10):
		# how many positions are in each row (rect.w / size[0])
		rowLength = 10
		# get a random list of 1 and 0 to represent placed player list
		rowHeight = 50
		allPos = [random.randint(0, 1) for i in range(rowHeight)]
		random.shuffle(allPos)
		yPos = [[] for i in range(len(allPos)//rowLength)]
		row = 0
		for i, y in enumerate(allPos):
			if i != 0:
				if i % rowLength == 0:
					row += 1
			yPos[row].append(allPos[i])

		positions = []
		for j in range(rowLength):
			s = " "
			for l in yPos:
				s += "{}, ".format(str(l[j]))
				positions.append(l[j])


		# which player to check win for
		player = 0

		# count which row is active
		row = (rowHeight // rowLength)
		for startIndex in range(len(positions)):
			# check if the end of the row is at least 4 indexs away
			if startIndex + 4 <= row:
				# check if the start point is the player we are checking for
				if positions[startIndex] == player:
					# create a set with start index
					indexs = set([startIndex])
					currentIndex = startIndex
					# check 4 indexs to the right 
					for i in range(4):
						# check if current index will go past the list length
						if currentIndex + 1 <= len(positions):
							# check if the current position is the same as player
							if positions[currentIndex] == player:
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
				row += (rowHeight // rowLength)
				

		posString = "\n"
		for i, pos in enumerate(allPos):
			if i % rowLength == 0:
				posString += "\n{}, ".format(pos)
			else:
				posString += "{}, ".format(pos)
		print(posString)

		posString = "\n"
		for i, pos in enumerate(positions):
			if i % rowLength == 0:
				posString += "\n{}, ".format(pos)
			else:
				if i % (rowHeight // rowLength) == 0:
					posString += "|\n{}, ".format(pos)
				else:
					posString += "{}, ".format(pos)

		print(posString, "\n")

		print("\nWins: {}\n".format(wins))

		


def DiagonalCheck():
	wins = 0
	player = 0

	rowLength = 10
	rowHeight = 40
	row = 0

	allPos = [random.randint(0, 1) for i in range(rowHeight)]
	# allPos = [0 for i in range(rowHeight)]

	positions = [[] for i in range(len(allPos) // rowLength)]

	for i, pos in enumerate(allPos):
		if i != 0:
			if i % rowLength == 0:
				row += 1
		positions[row].append(pos)

	string = "\n"
	for i, pos in enumerate(allPos):
		if i % rowLength == 0:
			string += "\n{}, ".format(pos)
		else:
			string += "{}, ".format(pos)
	print(string, "\n")


	for y, yList in enumerate(positions):
		for x in range(len(yList)):
			indexs = set([])
			# down - right check
			for i in range(4):
				try:
					if positions[y + i][x + i] == player:
						indexs.add((x + i, y + i))
					else:
						break
				except:
					break
			if len(indexs) >= 4:
				print("DR:", indexs)
				wins += 1


			indexs = set([(x, y)])
			# down - left check
			for i in range(1, 4):
				try:
					if x - i >= 0 and y - i >= 0:
						if positions[y - i][x - i] == player:
							indexs.add((x - i, y - i))
						else:
							break
				except:
					break
			if len(indexs) >= 4:
				print("DL", indexs)
				wins += 1


	print(wins)


DiagonalCheck()