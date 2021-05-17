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

blockSize = (30, 30)

playerColors = {
	0: red,
	1: blue
}

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
			Block((pos[0], pos[1], blockSize[0], blockSize[1]), playerColors[abs(self.player)])
			self.placedBlockPositions.append(pos)
			self.tempBlocks = []
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


	def CheckWin(self, newBlock):
		# check horizontally 
		index = allBlocks.index(newBlock)

		pass


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


def DrawLoop():
	screen.fill(darkGray)

	for block in allBlocks:
		block.Draw()

	board.Draw()

	pg.display.update()


board = Board((width // sf // 2 - 150, height // sf // 2 - 125, 300, 300), blockSize, lightGray)

board.StartPlaceBlock()
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
				board.PlaceBlock()

	DrawLoop()