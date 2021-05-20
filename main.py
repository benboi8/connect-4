import pygame as pg
from pygame import gfxdraw

pg.init()
clock = pg.time.Clock()
fps = 60

sf = 2
width, height = 640 * sf, 360 * sf
screen = pg.display.set_mode((width, height))
running = True

darkGray = (55, 55, 55)
lightGray = (205, 205, 205)
red = (205, 0, 0)
green = (0, 205, 0)
blue = (0, 0, 205)

allBlocks = []
winObjs = []
allButtons = []
sideBarObjs = []

blockSize = (30, 30)

playerColors = {
	0: red,
	1: blue
}

hasWon = False


def DrawRectOutline(surface, color, rect, width=1, outWards=False):
	x, y, w, h = rect
	width = max(width, 1)  # Draw at least one rect.
	width = min(min(width, w//2), h//2)  # Don't overdraw.

	# This draws several smaller outlines inside the first outline
	# Invert the direction if it should grow outwards.
	if outWards:
		for i in range(int(width)):
			pg.gfxdraw.rectangle(surface, (x-i, y-i, w+i*2, h+i*2), color)
	else:
		for i in range(int(width)):
			pg.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)


class Label:
	def __init__(self, surface, rect, colors, textData, drawData=(True, False), lists=[]):
		self.surface = surface
		self.ogRect = pg.Rect(rect)
		self.borderColor = colors[0]
		self.backgroundColor = colors[1]
		self.text = textData[0]
		self.ogFontSize = textData[1]
		self.textColor = textData[2]
		self.drawBorder = drawData[0]
		self.drawBackground = drawData[1]

		for l in lists:
			l.append(self)

		self.Rescale()

	def Rescale(self):
		self.rect = pg.Rect(self.ogRect.x * sf, self.ogRect.y * sf, self.ogRect.w * sf, self.ogRect.h * sf)
		fontSize = self.ogFontSize * sf
		self.font = pg.font.SysFont("arial", fontSize)
		self.textSurface = self.font.render(self.text, True, self.textColor)

	def UpdateText(self, text):
		self.text = text
		self.textSurface = self.font.render(self.text, True, self.textColor)

	def Draw(self):
		if self.drawBorder:
			if self.drawBackground:
				pg.draw.rect(self.surface, self.backgroundColor, self.rect)
			DrawRectOutline(self.surface, self.borderColor, self.rect, 1.5 * sf)
		else:
			if self.drawBackground:
				pg.draw.rect(self.surface, self.borderColor, self.rect)

		self.surface.blit(self.textSurface, ((self.rect.x + self.rect.w // 2) - self.textSurface.get_width() // 2, (self.rect.y + self.rect.h // 2) - self.textSurface.get_height() // 2))


class Button:
	def __init__(self, surface, rect, colors, functionName, textData, lists=[allButtons]):
		self.surface = surface
		self.ogRect = pg.Rect(rect)
		self.borderColor = colors[0]
		self.backgroundColor = colors[1]
		self.functionName = functionName
		self.text = textData[0]
		self.ogFontSize = textData[1]
		self.textColor = textData[2]

		for l in lists:
			l.append(self)

		self.Rescale()

	def Rescale(self):
		self.rect = pg.Rect(self.ogRect.x * sf, self.ogRect.y * sf, self.ogRect.w * sf, self.ogRect.h * sf)
		fontSize = self.ogFontSize * sf
		self.font = pg.font.SysFont("arial", fontSize)
		self.textSurface = self.font.render(self.text, True, self.textColor)

	def UpdateText(self, text):
		self.textSurface = self.font.render(text, True, self.textColor)

	def Draw(self):
		pg.draw.rect(self.surface, self.backgroundColor, self.rect)
		DrawRectOutline(self.surface, self.borderColor, self.rect, 1.5 * sf)

		self.surface.blit(self.textSurface, ((self.rect.x + self.rect.w // 2) - self.textSurface.get_width() // 2, (self.rect.y + self.rect.h // 2) - self.textSurface.get_height() // 2))

	def HandleEvent(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				if self.rect.collidepoint(pg.mouse.get_pos()):
					globals()[self.functionName]()


class Board:
	def __init__(self, rect, size, color):
		self.surface = screen
		self.ogRect = pg.Rect(rect)
		self.ogSize = size
		self.color = color
		self.Rescale()

		self.xBlockPositions = []
		self.yBlockPositions = []
		self.placedBlockPositions = []

		self.tempBlocks = []
		self.placeCheck = False
		self.player = False

		self.CreateBorad()

	def Rescale(self):
		self.rect = pg.Rect(self.ogRect.x * sf, self.ogRect.y * sf, self.ogRect.w * sf, self.ogRect.h * sf)
		self.size = (self.ogSize[0] * sf, self.ogSize[1] * sf)
		self.rowLength = self.rect.w // self.size[0]
		self.playerBlocks = [[2 for i in range(self.rect.h // self.size[1])] for i in range((self.rect.w // self.size[0]) + 1)]

	def CreateBorad(self):
		for x in range(self.rect.w):
			if x % self.size[0] == 0:
				self.xBlockPositions.append((self.rect.x // sf) + (x // sf))
		for y in range(self.rect.h):
			if y % self.size[1] == 0:
				self.yBlockPositions.append((self.rect.y // sf) + (y // sf))

	def Draw(self):
		DrawRectOutline(self.surface, self.color, self.rect, 2)
		for x in self.xBlockPositions:
			for y in self.yBlockPositions:
				DrawRectOutline(self.surface, self.color, (x * sf, y * sf, self.size[0], self.size[1]))

		self.UpdateBlockPos()

		if not hasWon:
			for block in self.tempBlocks:
				if self.placeCheck:
					block.Draw()

	def UpdateBlockPos(self):
		self.tempBlocks[0].UpdatePos(self.GetTempBlockPos())

	def StartPlaceBlock(self):
		pos = self.GetBlockPos()
		Block((pos[0], pos[1], blockSize[0], blockSize[1]), playerColors[abs(self.player)], lists=[self.tempBlocks])

	def PlaceBlock(self):
		pos = self.GetBlockPos()
		if self.placeCheck:
			self.playerBlocks[self.yBlockPositions.index(pos[1]) + 1][self.xBlockPositions.index(pos[0])] = abs(self.player)
			Block((pos[0], pos[1], blockSize[0], blockSize[1]), playerColors[abs(self.player)], lists=[allBlocks])
			self.placedBlockPositions.append(pos)
			self.tempBlocks = []
			self.CheckWin()
			self.player = not self.player
			self.StartPlaceBlock()

	def GetBlockPos(self):
		mousePos = pg.mouse.get_pos()
		mouseX = mousePos[0] // sf		
		mouseY = mousePos[1] // sf		

		for i, x in enumerate(self.xBlockPositions):
			# get the position closest to the left of the mousePos
			xLowerBound = x
			# get the position closest to the right of the mousePos
			xUpperBound = self.xBlockPositions[min(len(self.xBlockPositions)-1, i+1)]
			# check if mouse is within those bounds
			if max(mouseX, self.xBlockPositions[0]) >= xLowerBound and min(mouseX, self.xBlockPositions[-1]) <= xUpperBound:
				pos = (xLowerBound, mouseY)

		pos = (pos[0], max(self.yBlockPositions))
		posCheck = False
		while not posCheck:
			if pos in self.placedBlockPositions:
				pos = (pos[0], pos[1] - self.size[1] // sf)
				if pos[1] < min(self.yBlockPositions):
					posCheck = True
					self.placeCheck = False
			else:
				posCheck = True
				self.placeCheck = True

		return pos

	def GetTempBlockPos(self):
		pos = self.GetBlockPos()
		return (pos[0], min(self.yBlockPositions) - self.size[1] // sf - 2 * sf)

	def CheckWin(self):
		if self.CheckHorizontal() or self.CheckVeritical() or self.CheckDiagonal():
			Win(abs(self.player))

	def CheckHorizontal(self):
		wins = 0
		for y, yList in enumerate(self.playerBlocks):
			for x in range(len(yList)):
				indexs = set([])
				for i in range(4):
					try:
						if self.playerBlocks[y][x + i] == abs(self.player):
							indexs.add((x + i, y))
						else:
							break
					except:
						break
				if len(indexs) >= 4:
					wins += 1
				indexs = set([])

		if wins >= 1:
			return True
		else:
			return False

	def CheckVeritical(self):
		wins = 0
		for y, yList in enumerate(self.playerBlocks):
			for x in range(len(yList)):
				indexs = set([])
				for i in range(4):
					try:
						if self.playerBlocks[y + i][x] == abs(self.player):
							indexs.add((x, y + i))
						else:
							break
					except:
						break
				if len(indexs) >= 4:
					wins += 1
				indexs = set([])

		if wins >= 1:
			return True
		else:
			return False

	def CheckDiagonal(self):
		wins = 0
		for y, yList in enumerate(self.playerBlocks):
			for x in range(len(yList)):
				indexs = set([])
				for i in range(4):
					try:
						if self.playerBlocks[y + i][x + i] == abs(self.player):
							indexs.add((x + i, y + i))
						else:
							break
					except:
						break
				if len(indexs) >= 4:
					wins += 1

				indexs = set([])
				for i in range(4):
					try:
						if x - i >= 0 and y + i >= 0:
							if self.playerBlocks[y + i][x - i] == abs(self.player):
								indexs.add((x - i, y + i))
							else:
								break
					except:
						break
				if len(indexs) >= 4:
					wins += 1

		if wins >= 1:
			return True
		else:
			return False
	

class Block:
	def __init__(self, rect, color, lists=[allBlocks]):
		self.surface = screen
		self.ogRect = pg.Rect(rect)
		self.color = color

		for l in lists:
			l.append(self)

		self.Rescale()

	def Rescale(self):
		self.rect = pg.Rect(self.ogRect.x * sf, self.ogRect.y * sf, self.ogRect.w * sf, self.ogRect.h * sf)

	def Draw(self):
		pg.draw.rect(self.surface, self.color, self.rect)

	def UpdatePos(self, pos):
		self.ogRect = pg.Rect(pos[0], pos[1], self.ogRect.w, self.ogRect.h)
		self.Rescale()


def Restart():
	global board, winObjs, allBlocks, hasWon
	allBlocks = []
	winObjs = []
	hasWon = False
	board = Board((width // sf // 2 - 150, height // sf // 2 - 125, 300, 300), blockSize, lightGray)
	board.StartPlaceBlock()


def CreateWinObjects():
	global winObjs
	winObjs = []
	Label(screen, (170, 5, 300, 40), (lightGray, darkGray), ("", 30, lightGray), (True, True), lists=[winObjs])
	Button(screen, (10, height // sf - 40, 130, 25), (lightGray, darkGray), "Restart", ("Restart", 16, lightGray), lists=[winObjs, allButtons])


def CreateSideBarObjs():
	global sideBarObjs
	sideBarObjs = []
	# scores
	Label(screen, (10, 40, 130, 25), (lightGray, darkGray), ("Player one score: 0", 12, lightGray), (True, True), lists=[sideBarObjs])
	Label(screen, (width // sf - 140, 40, 130, 25), (lightGray, darkGray), ("Player two score: 0", 12, lightGray), (True, True), lists=[sideBarObjs])

	# titles
	Label(screen, (10, 10, 130, 25), (lightGray, playerColors[0]), ("Player one", 15, lightGray), (True, True), lists=[sideBarObjs])
	Label(screen, (width // sf - 140, 10, 130, 25), (lightGray, playerColors[1]), ("Player two", 15, lightGray), (True, True), lists=[sideBarObjs])
	

def Win(player):
	global hasWon
	CreateWinObjects()

	scoreText = sideBarObjs[player].text.split(":")
	score = int(scoreText[1]) + 1
	sideBarObjs[player].UpdateText("Player one score: {}".format(score))
	
	hasWon = True
	if player == 0:
		player = "one"
	elif player == 1:
		player = "two"

	winObjs[0].UpdateText("Player {} has won!".format(player))


def DrawLoop():
	screen.fill(darkGray)

	for block in allBlocks:
		block.Draw()

	board.Draw()

	for obj in sideBarObjs:
		obj.Draw()

	if hasWon:
		for obj in winObjs:
			obj.Draw()

	pg.display.update()


Restart()
CreateSideBarObjs()
while running:
	clock.tick_busy_loop(fps)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				if not hasWon:
					board.PlaceBlock()

		for button in allButtons:
			button.HandleEvent(event)

	DrawLoop()