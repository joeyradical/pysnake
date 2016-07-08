import pygame
import snake
import gamescreengraphics
from constants import *



class GameScreen:

	def __init__(self, disp, clk):
		self.disp = disp
		self.game_running = False
		self.clk = clk
		self.snake = None
		self.walls = []

	def init_game(self):
		self.game_running = True
		self.snake = snake.Snake(self.disp, 300,200)
		self.init_walls()

	def init_walls(self):
		self.walls = [
			gamescreengraphics.Wall(self.disp, [0,0], [SCREEN_WIDTH, 0]),  # Top Wall
			gamescreengraphics.Wall(self.disp, [0,SCREEN_HEIGHT], [SCREEN_WIDTH, 0]),  # Bottom Wall
			gamescreengraphics.Wall(self.disp, [0, 0], [0, SCREEN_HEIGHT]), # Left Wall
			gamescreengraphics.Wall(self.disp, [SCREEN_WIDTH, 0], [0, SCREEN_HEIGHT]) # Right Wall
		]

	def draw_screen(self):
		self.disp.fill(COLOR_BLACK)
		# Draw walls
		for wall in self.walls:
			wall.draw()
		self.snake.draw()

	def run(self):
		self.init_game()
		while self.game_running:
			# Read event queue
			event_queue = pygame.event.get()
			# Iterate through event queue
			self.process_events(event_queue)
			self.check_collisions()
			self.draw_screen()
			pygame.display.flip()
			self.clk.tick(30)
		return 1

	def process_events(self,event_queue):
		for e in event_queue:
			if e.type is QUIT:
				self.game_running = False
			elif e.type is KEYDOWN:
				# Exit game if escape button has been pressed
				if e.key is K_ESCAPE:
					self.game_running = False
				# If arrow key or W, A, S, or D is pressed, change direction of snake
				elif e.key is K_DOWN or e.key is K_s:
					self.snake.move_down()
				elif e.key is K_UP or e.key is K_w:
					self.snake.move_up()
				elif e.key is K_LEFT or e.key is K_a:
					self.snake.move_left()
				elif e.key is K_RIGHT or e.key is K_d:
					self.snake.move_right()

	def check_collisions(self):
		for wall in self.walls:
			if self.snake.head.rect.colliderect(wall.rect):
				print "Collide"
