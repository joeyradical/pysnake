import pygame
import snake
import gamescreengraphics
import random
from constants import *


class GameScreen:

	def __init__(self, disp, clk):
		self.disp = disp
		self.game_running = False
		self.clk = clk
		self.snake = None
		self.walls = []
		self.field_blocks = []

	def init_game(self):
		self.game_running = True
		# Initialize snake
		self.init_snake()
		self.init_walls()
		pygame.time.set_timer(GAME_EVENT, GAME_PERIOD)

	def init_snake(self):
		# Generate start coords
		startx = random.randint(1, N_XPOSITIONS-1) * BLOCK_DIM
		starty = random.randint(1, N_YPOSITIONS-1) * BLOCK_DIM

		# Generate start direction
		sample = ['l', 'r', 'u', 'd']
		if starty == BLOCK_DIM:
			sample.remove('u')
		elif starty == (N_YPOSITIONS-1) * BLOCK_DIM:
			sample.remove('d')

		if startx == BLOCK_DIM:
			sample.remove('l')
		elif startx == (N_XPOSITIONS-1) * BLOCK_DIM:
			sample.remove('r')

		start_direction = random.sample(sample, 1)[0]
		self.snake = snake.Snake(self.disp, startx, starty, start_direction)
		test_block = snake.Variable(COLOR_WHITE, BLOCK_DIM, BLOCK_DIM, self.disp, 160,160)
		self.field_blocks.append(test_block)

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
		for block in self.field_blocks:
			block.draw(COLOR_WHITE)
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
			elif e.type is GAME_EVENT:
				self.process_game_event()
			elif e.type is KEYDOWN:
				# Exit game if escape button has been pressed
				if e.key is K_ESCAPE:
					self.game_running = False
				# If arrow key or W, A, S, or D is pressed, change direction of snake
				elif e.key is K_DOWN or e.key is K_s:
					if self.snake.get_head_direction() is not 'u' and self.snake.get_head_direction() is not 'd':
						self.snake.add_turn('d')
				elif e.key is K_UP or e.key is K_w:
					if self.snake.get_head_direction() is not 'u' and self.snake.get_head_direction() is not 'd':
						self.snake.add_turn('u')
				elif e.key is K_LEFT or e.key is K_a:
					if self.snake.get_head_direction() is not 'l' and self.snake.get_head_direction() is not 'r':
						self.snake.add_turn('l')
				elif e.key is K_RIGHT or e.key is K_d:
					if self.snake.get_head_direction() is not 'l' and self.snake.get_head_direction() is not 'r':
						self.snake.add_turn('r')


	def check_collisions(self):
		for wall in self.walls:
			if self.snake.head.get_rect().colliderect(wall.rect):
				self.game_running = False
		for var in self.snake.get_variables():
			if self.snake.head.get_rect().colliderect(var.get_rect()):
				print "Col damage"

		for block in self.field_blocks:
			if self.snake.head.get_rect().colliderect(block.rect):
				self.snake.collect_variable(block)
				self.field_blocks.remove(block)
				startx = random.randint(1, N_XPOSITIONS - 1) * BLOCK_DIM
				starty = random.randint(1, N_YPOSITIONS - 1) * BLOCK_DIM
				test_block = snake.Variable(COLOR_WHITE, BLOCK_DIM, BLOCK_DIM, self.disp, startx, starty)
				self.field_blocks.append(test_block)
	def process_game_event(self):
		self.snake.update()
