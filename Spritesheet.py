# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame

class Spritesheet(pygame.sprite.Sprite):
	def __init__(self, imageFile, xSize, ySize):
		super().__init__()
		self.width = xSize
		self.height = ySize
		self.animation = False
		self.debug = False

		self.rect = pygame.Rect(0,0,xSize,ySize)

		#if type(imageFile) == list: #worst
		if isinstance(imageFile, list): 
			self.xLength = len(imageFile)
			self.yLength = len(imageFile[0])
			self.width = xSize * self.xLength
			self.height = ySize * self.yLength 
			self.src = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
			
			for ix in range(0, self.xLength):
				for iy in range(0, self.yLength):
					part = pygame.image.load(imageFile[ix][iy])
					
					self.src.blit(part, (0, 0), (ix * xSize, iy * ySize, width, height))
	 
		else:	
			self.changeImage(imageFile)	

	def changeImage(self, imageFile):
		self.image = pygame.image.load(imageFile)
		self.src = pygame.transform.scale(self.image, (self.width, self.height))

	def loadAnimation(self, sheetWidth, sheetHeight, cellWidth, cellHeight):
		self.animation = True
		self.animationLength = 10
		self.animationState = 0
		self.animCellWidth = cellWidth
		self.animCellHeight = cellHeight
		self.animSheetWidth = sheetWidth
		self.animSheetHeight = sheetHeight
		self.width = cellWidth
		self.height = cellHeight
		self.animationCell = 0
		self.test = 0	
		self.timer = 0
		self.animating = False

		self.rect = pygame.Rect(0,0,self.animCellWidth, self.animCellHeight)

		# compute horizontal animations
		self.hAnimations = (int(self.animSheetWidth / self.animCellWidth))
		self.vAnimations = (int(self.animSheetHeight / self.animCellHeight))
		
		self.sheet = [[None] * self.vAnimations] * self.hAnimations

		'''# go through columns and rows
		for i in range(0, self.vAnimations):
			for j in range(0, self.hAnimations):
				
				'''jPix = j * self.animCellWidth
				iPix = i * self.animCellHeight
				if self.debug == True:					
					print("I:"+ str(i))				
					print("J:" + str(j))
					print("J pix:", jPix )
					print("I pix:", iPix )'''	
				self.sheet[j][i] = pygame.Surface((self.animCellWidth, self.animCellHeight), pygame.SRCALPHA)
				#print("jpix", jPix)
				self.sheet[j][i].blit(self.src, (0, 0), (j * self.animCellWidth, i * self.animCellHeight, self.animCellWidth, self.animCellHeight))'''

		self.image = self.sheet[0][0]

		'''			surf = pygame.Surface((width, height), pygame.SRCALPHA)
			surf.blit(walk_all, (0, 0), (x_offset+n*width, 0, width, height))
			self.images.append(surf)'''


	def update(self):



		if self.debug == True:
			print("Tick ", self.timer)
		if self.animating == True:
			if self.debug == True:
				print("Animating")
			self.timer += 1
			if self.timer > self.animationLength:
				if self.debug == True:
					print("Changing to next frame ", self.animationCell)				
				self.animationCell += 1
				if self.animationCell > (self.hAnimations-1):
					if self.debug == True:
						print("Reset")
					self.animationCell = 0		
				print("Changing!", self.animationCell, self.animationState)
				self.image = pygame.Surface((self.animCellWidth, self.animCellHeight), pygame.SRCALPHA)
				self.image.blit(self.src, (0,0), (self.animationCell * self.animCellWidth, self.animCellHeight*self.animationState, self.animCellWidth, self.animCellHeight))
				self.timer = 0

	# setCurrentCycle(cycleState) – Changes the animation cycle to the one indicated by the number. 
	def setCurrentCycle(self, state):
		self.animationState = state

	# playAnimation() - begins (and repeats) the currently indicated animation.
	def playAnimation(self):
		self.animating = True

	# pauseAnimation() - Pauses the animation until it is re-started with a playAnimation() command.
	def pauseAnimation(self):
		self.animating = False