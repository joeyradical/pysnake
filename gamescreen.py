import pygame
import snake
from constants import *



class GameScreen:

	def __init__(self, disp, clk):
		self.disp = disp
		self.game_running = False
		self.clk = clk
		self.snake = None

	def init_game(self):
		self.game_running = True
		self.snake = snake.Snake(self.disp, 300,200)

	def draw_screen(self):
		self.disp.fill(COLOR_BLACK)
		self.snake.draw()

	def run(self):
		self.init_game()
		while self.game_running:
			# Read event queue
			event_queue = pygame.event.get()
			# Iterate through event queue
			self.process_events(event_queue)
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
