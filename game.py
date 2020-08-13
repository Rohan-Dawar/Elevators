# Dependencies
import pygame as pg
import os, sys

# Constants
FLOOR_W = 50
FLOOR_H = 64
# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (90,90,90)
LIGHTPURP = (200,200,230)
GREEN = (0,230,0)
ORANGE = (235,70,180)

# Sprites: Credit to SpiderDave from OpenGameArt.org
sprites = []
def load_sprites(liftsVar):
	for i in range(liftsVar):
		sprites.append(pg.image.load(f'{os.path.abspath(os.getcwd())}/sprites/{i}.png'))

# Elevator Class
class Elevator:
	instances = []
	def __init__(self, img, floorVar, liftsVar):
		self.__class__.instances.append(self)
		self.img = img
		self.floorVar = floorVar
		self.shaft = self.__class__.instances.index(self) # The Shaft # Of The Elevator Instance
		self.x = FLOOR_W*(self.shaft+2)
		self.y = FLOOR_H*floorVar
		self.ismoving = 0 # 0: static, -1: up (y-val decreasing), +1:down (y-val increasing)
		self.currentFloor = 1
		self.dest = 1
		self.speed = 1 #proportional to liftsVar: pow(2,liftsVar+1)/128
	@classmethod
	def draw_doors(cls, screen):
		for instance in cls.instances:
			screen.blit(instance.img, (instance.x, instance.y))
	@classmethod
	def motion(cls):
		comparitor = []
		for instance in cls.instances:
			instance.y += instance.speed*instance.ismoving
			# Set Destination From Specific Shaft
			if clicked[0] == instance.shaft+1:
				instance.dest = clicked[1]
			# Add to Comparitor for Main Shaft
			if clicked[0] == 0:
				comparitor.append(abs(clicked[1]-instance.currentFloor))
			# Elevator Direction:
			if instance.currentFloor < instance.dest:
				instance.ismoving = -1
			elif instance.currentFloor > instance.dest:
				instance.ismoving = 1
			# Check if Elevator has reached destination floor:
			if instance.y == FLOOR_H*(instance.floorVar-(instance.dest-1)):
				instance.currentFloor = instance.dest
				instance.ismoving = 0
		#Set Destination From Main Shaft
		if len(comparitor) > 0:
			cls.instances[comparitor.index(min(comparitor))].dest = clicked[1]

# Grid Class
class ShaftGrid:
	def __init__(self,floorVar,liftsVar):
		self.x = liftsVar
		self.y = floorVar
		self.LiftsGrid = []
		for i in range(liftsVar+1):
			nextShaft = []
			for n in range(floorVar):
				nextShaft.append(pg.Rect(FLOOR_W*(i+1),FLOOR_H*(n+1),FLOOR_W,FLOOR_H))
			self.LiftsGrid.append(nextShaft)

# HUD
def draw_hud(screen,gridSys):
	font = pg.font.Font('freesansbold.ttf', 15)

	# Uncomment This For 'Debug' On Screen:

	# floorsTXT = font.render(f'Floors:{gridSys.y}', True, BLACK)
	# screen.blit(floorsTXT, (10,10))

	# liftsTXT = font.render(f'Lifts:{gridSys.x}', True, BLACK)
	# screen.blit(liftsTXT, (10,30))

	# clickedTXT = font.render(f'Clicked:{clicked}', True, BLACK)
	# screen.blit(clickedTXT, (10,50))

	# Lifts Grid Shafts
	for shaft in gridSys.LiftsGrid:
		for floor in shaft:
			pg.draw.rect(screen, LIGHTPURP, floor, 1)

	# Draw Floor Nums in Leftmost Shaft:
	for floor in range(gridSys.y):
		renderFloorNum = font.render(str(gridSys.y-floor), True, WHITE)
		screen.blit(renderFloorNum, (FLOOR_W+(FLOOR_W/2.5), FLOOR_H*(floor+1)+FLOOR_H/2.5))

	# Draw Shaft Dests (Above Shaft)
	for shaft in range(gridSys.x):
		if Elevator.instances[shaft].currentFloor == Elevator.instances[shaft].dest:
			col = GREEN
		else:
			col = ORANGE
		renderShaftDest = font.render(str(Elevator.instances[shaft].dest), True, col)
		screen.blit(renderShaftDest, (FLOOR_W*(shaft+2)+(FLOOR_W/2.5),50))

# Click Floor
clicked = (1,1)
def click_floor(screen,gridSys):
	global clicked
	coords = pg.mouse.get_pos()
	lclick = pg.mouse.get_pressed()[0]
	for shaft in gridSys.LiftsGrid:
		for floor in shaft:
			if floor.collidepoint(coords) and lclick:
				pg.draw.rect(screen, GREEN, floor)
				shaftClicked = gridSys.LiftsGrid.index(shaft)
				floorClicked = gridSys.y - gridSys.LiftsGrid[shaftClicked].index(floor)
				clicked = (shaftClicked, floorClicked)

# Reconfigure Params
def reconfig(gridSys):
	# Delete Memory
	for instance in Elevator.instances:
		del instance
	Elevator.instances.clear()
	sprites.clear()
	del gridSys
	global clicked
	clicked = (1,1)
	running = False
	pg.quit()
	# Run TK
	from Launcher import main
	main()
	sys.exit()

# Init Pygame w/RunLoop, Destroy TK
def run_game(root,floorVar,liftsVar):
	pg.init()
	pg.display.set_caption("Elevators V4 - Rohan Dawar")
	SCREEN_W = FLOOR_W*(liftsVar+3)
	SCREEN_H = FLOOR_H*(floorVar+2)
	screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
	load_sprites(liftsVar)
	gridSys = ShaftGrid(floorVar,liftsVar)
	
	# Create Elevators:
	for i in range(liftsVar):
		Elevator(sprites[i],floorVar,liftsVar)

	try: # Close TK if opened from TK
		root.destroy()
	except AttributeError:
		pass

	# Game Loop
	global running
	running = True
	while running:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					running = False
					print("Safe Quit")
				if event.key == pg.K_RETURN:
					reconfig(gridSys)
		try:
			screen.fill(GRAY)
			draw_hud(screen,gridSys)
			Elevator.draw_doors(screen)
			click_floor(screen,gridSys)
			Elevator.motion()
			pg.display.update()
		except pg.error:
			return

# Run with default 3x3
if __name__ == '__main__': run_game(None,3,3)