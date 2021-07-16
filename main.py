import pygame
from Background import Background
from Spritesheet import Spritesheet



pygame.init()

# Setup the clock for a decent framerate

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 500))




class Character(pygame.sprite.Sprite):

	# Constructor. Pass in the color of the block,
	# and its x and y position
	def __init__(self):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)

		# Create an image of the block, and fill it with a color.
		# This could also be an image loaded from the disk.
		self.image = pygame.image.load('sprites/sean_sprite.png')

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values of rect.x and rect.y
		self.rect = self.image.get_rect()


class Character2(Spritesheet):

	# Constructor. Pass in the color of the block,
	# and its x and y position
	def __init__(self):
		# Call the parent class (Sprite) constructor
		super().__init__("sprites/sean_sheet.png", 500, 200)
		self.debug = True
		self.loadAnimation(500, 200, 100, 100)

		self.timer = 0
		self.frame = 0

		# Create an image of the block, and fill it with a color.
		# This could also be an image loaded from the disk.
		#load sprite sheet
		N = 6; width = 50; height = 50; x_offset = 0
		self.images = []
		walk_all = pygame.image.load('sprites/sean_sheet.png').convert_alpha()
		for n in range(N):
			surf = pygame.Surface((width, height), pygame.SRCALPHA)
			surf.blit(walk_all, (0, 0), (x_offset+n*width, 0, width, height))
			self.images.append(surf)

		# Fetch the rectangle object that has the dimensions of the image
		# Update the position of this object by setting the values of rect.x and rect.y
		self.rect = pygame.Rect(0,0,50,50)

class Character3(Spritesheet):
	# Constructor. Pass in the color of the block,
	# and its x and y position
	def __init__(self):
		# Call the parent class (Sprite) constructor
		super().__init__("sprites/sean_sheet.png", 500, 200)
		self.debug = True
		self.loadAnimation(500, 200, 100, 100)
		self.playAnimation()






		




done = False

char = Character3()
sprites = pygame.sprite.Group()
sprites.add(char)
bg0 = Background(screen, "sprites/parallax-forest-back-trees.png", 1020, 600, .25, 0)
bg1 = Background(screen, "sprites/parallax-forest-middle-trees.png", 1020, 600, .5, 0)		
bg2 = Background(screen, "sprites/parallax-forest-front-trees.png", 1020, 600, .75, 0)
bg3 = Background(screen, "sprites/parallax-forest-lights.png", 1020, 600, 1, 0)		
offsetX = 0
offsetY = 0

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

		# Add this somewhere after the event pumping and before the display.flip()
		pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(30, 30, 60, 60))

		bg0.draw(offsetX, offsetY)
		bg1.draw(offsetX, offsetY)
		bg2.draw(offsetX, offsetY)

		sprites.draw(screen)


		for sprite in sprites:
			sprite.update()
        
		pygame.display.flip()

		clock.tick(0)