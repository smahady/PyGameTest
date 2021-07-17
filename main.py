import pygame
from Background import Background
from Spritesheet import Spritesheet
from Ground import Ground
from enum import Enum

class States(Enum):
	FALLING = 0
	WALK = 1
	JUMP = 2
	STAND = 3

class Facing():
	RIGHT = 0
	LEFT = 1

class Keys:
	# key variables
	K_ESC = 27
	K_SPACE = 32
	K_PGUP = 33
	K_PGDOWN = 34
	K_END = 35
	K_HOME = 36
	K_LEFT = 37
	K_UP = 38
	K_RIGHT = 39
	K_DOWN = 40



class Camera():
	def __init__(self, game):
		self.scene = game

	def follow(self, sprite):
		self.sprite = sprite

	def update(self):
		if self.sprite.drawX < 250:
			if self.sprite.posX < 300:
				self.sprite.posX = 300
			else:
				self.scene.offsetX -= 6
		if self.sprite.drawX > (350):
			if self.sprite.posX > (26*120):
				self.sprite.posX = (26*120)
			else:
				self.scene.offsetX += 6

class Spaceship(Spritesheet):
	def __init__(self, thisScene):
		super().__init__(thisScene, "sprites/spaceship100.png", 100, 100)
		self.posX = 300
		self.posY = 100
		self.dx = 6
		self.timer = 60
		self.enemies = []

	def update(self):

		if self.drawX < 0:
			self.dx = 6
		if self.drawX > 550:
			self.dx = -6
		self.timer -= 1
		if self.timer < 1:
			self.timer = 60
			self.enemySpawn()

		#for enemy in self.enemies:
		#	enemy.update(self.scene.offsetX, self.scene.offsetY)

	def enemySpawn(self):
		pass



class Character(Spritesheet):
	# Constructor. Pass in the color of the block,
	# and its x and y position
	def __init__(self, game, sprite, x, y):
		# Call the parent class (Sprite) constructor
		super().__init__(game, sprite,x, y)
		self.debug = False
		self.loadAnimation(500, 200, 100, 100)
		self.stateTimer = 0
		self.dy = 7
		self.state = States.FALLING

	def update(self, offsetX = 0, offsetY = 0):
		if self.state == States.FALLING:
			if self.game.ground.collidesWith(self):
				self.standBehavior()
		elif self.state == States.STAND or self.state == States.WALK:
			if self.game.keysDown[Keys.K_SPACE]:
				self.jumpBehavior()
			elif self.game.keysDown[Keys.K_RIGHT] or self.game.keysDown[Keys.K_LEFT]:
				self.walkBehavior()
			elif self.state == States.WALK:
				if (self.facing == Facing.RIGHT) and (self.game.keysDown[Keys.K_RIGHT] == False):
					self.standBehavior()
				if (self.facing == Facing.LEFT) and (self.game.keysDown[Keys.K_LEFT] == False):
					self.standBehavior()
		elif self.state == States.JUMP:
			self.stateTimer = self.stateTimer - 1
			if self.stateTimer < 1:
				self.dy = self.dy * -1
				self.state = States.FALLING
		super().update(offsetX, offsetY)		

	def standBehavior(self):
		self.dy = 0
		self.dx = 0
		self.state = States.STAND
		self.pauseAnimation()

	# override this in your Character
	def jumpBehavior(self):
		pass

	# override this in your Character
	def walkBehavior(self):
		pass

# sean mahady
#250x100
# 50, 50
class Sean(Character):
	def __init__(self, game):
		super().__init__(game, "sprites/sean_sheet.png", 250, 100)
		self.posX = 75	
		self.posY = 100
		self.loadAnimation(250, 100, 50, 50) 	# divides the sprite sheet into pieces
		self.setAnimationSpeed(10)	#sets a QTimer to 100ms
		self.playAnimation()	#starts the QTimer
		self.game = game

		#make a state for you class
		self.state = States.FALLING	#falling

	# Add a method called walkBehavior. 
	# This should check if self.scene.keysDown[Scene.K_RIGHT]is True. If so self.facing to 0, self.setCurrentCycle to 0, call the self.playAnimation method. Set the DX to a value between 0 and 10. Set a State to States.WALK
	# If not check if self.scene.keysDown[Scene.K_LEFT] is True. If so self.facing to 1, self.setCurrentCycle to 1, call the self.playAnimation method. Set the DX to a value between 0 and -10. Set a State to States.WALK
	def walkBehavior(self):
		if self.game.keysDown[Keys.K_RIGHT]:
			self.facing = 0
			self.setCurrentCycle(0)
			self.playAnimation()
			self.dx = 4
			self.state = States.WALK
		elif self.game.keysDown[Keys.K_LEFT]:
			self.facing = 1
			self.setCurrentCycle(1)
			self.playAnimation()
			self.dx = -4
			self.state = States.WALK

	# Add a method called jumpBehavior. This should set the dy to a negative number (moving up), and set the stateTimer to the number of frames before falling.
	def jumpBehavior(self):
		self.stateTimer = 25
		self.dy = -4	
		self.state = States.JUMP


class Game:
	def __init__(self):
		pygame.init()

		# Setup the clock for a decent framerate
		self.clock = pygame.time.Clock()

		self.screen = pygame.display.set_mode((600, 600))

		self.camera = Camera(self)

		self.offsetX = 20
		self.offsetY = 20

		self.offsetX = 20
		self.offsetY = 20

		self.keysDown = [None] * 256

		self.bg0 = Background(self, "sprites/parallax-forest-back-trees.png", 1020, 600, .25, 0)
		self.bg1 = Background(self, "sprites/parallax-forest-middle-trees.png", 1020, 600, .5, 0)		
		self.bg2 = Background(self, "sprites/parallax-forest-front-trees.png", 1020, 600, .75, 0)
		self.bg3 = Background(self, "sprites/parallax-forest-lights.png", 1020, 600, 1, 0)		
		self.ground = Ground(self)

		self.main = Sean(self)



		self.spaceship = Spaceship(self)

		self.camera.follow(self.main)	

		self.sprites = pygame.sprite.Group()
		self.sprites.add(self.main)
		self.sprites.add(self.ground)
		self.sprites.add(self.spaceship)

		self.groundedSprites = pygame.sprite.Group()
		self.groundedSprites.add(self.main)

	# initializes key values to false
	def initKeys(self):
		for i in range(255):
			self.keysDown[i] = False
		for i in range(255):
			self.boardKeysDown[i] = False

	# check events
	def keyPressEvent(self, keys):
		if keys[pygame.K_LEFT]:
			self.keysDown[Keys.K_LEFT] = True
		else:
			self.keysDown[Keys.K_LEFT] = False

		if keys[pygame.K_RIGHT]:
			self.keysDown[Keys.K_RIGHT] = True
		else:
			self.keysDown[Keys.K_RIGHT] = False	

		if keys[pygame.K_SPACE]:
			self.keysDown[Keys.K_SPACE] = True
		else:
			self.keysDown[Keys.K_SPACE] = False


	# execute our main loop
	def run(self):
		done = False

		while not done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True


			keys = pygame.key.get_pressed()  #checking pressed keys
			self.keyPressEvent(keys)

			# Add this somewhere after the event pumping and before the display.flip()
			pygame.draw.rect(self.screen, (0, 128, 255), pygame.Rect(30, 30, 60, 60))

			self.bg0.draw(self.offsetX, self.offsetY)
			self.bg1.draw(self.offsetX, self.offsetY)
			self.bg2.draw(self.offsetX, self.offsetY)
			self.bg3.draw(self.offsetX, self.offsetY)







			for sprite in self.sprites:
				sprite.update(self.offsetX, self.offsetY)

			self.camera.update()


			self.sprites.draw(self.screen)
       
			pygame.display.flip()

			self.clock.tick(30)

game = Game()
game.run()