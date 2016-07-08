import pygame
from constants import *


class Snake:
	def __init__(self, disp, posx, posy):
		self.disp = disp
		self.head = Head(COLOR_BLACK, BLOCK_DIM, BLOCK_DIM, disp, posx, posy)
		self.variables = []

	def draw(self):
		self.head.draw(COLOR_WHITE)
		for var in self.variables:
			var.draw(COLOR_WHITE)

	def move_left(self):
		self.head.update_x_coord(self.head.get_x_coord() - BLOCK_DIM)

	def move_right(self):
		self.head.update_x_coord(self.head.get_x_coord() + BLOCK_DIM)

	def move_up(self):
		self.head.update_y_coord(self.head.get_y_coord() - BLOCK_DIM)
		print "UP"

	def move_down(self):
		self.head.update_y_coord(self.head.get_y_coord() + BLOCK_DIM)


class Block(pygame.sprite.Sprite):
	def __init__(self, color, width, height, disp, posx, posy):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)

		# Create an image of the block, and fill it with color
		self.image = pygame.Surface([width, height])
		self.image.fill(color)

		# Fetch the rectangle object that has the dimensions of the image
		self.rect = self.image.get_rect()
		self.rect.x = posx
		self.rect.y = posy
		self.disp = disp

	def update_x_coord(self, new_x):
		self.rect.x = new_x

	def update_y_coord(self, new_y):
		self.rect.y = new_y

	def get_x_coord(self):
		return self.rect.x

	def get_y_coord(self):
		return self.rect.y


	def draw(self, color):
		raise NotImplementedError


class Head(Block):
	def __init__(self, color, width, height, disp, posx, posy):
		# Call the parent class (Block) constructor
		Block.__init__(self, color, width, height, disp, posx, posy)

	def draw(self, color):
		pygame.draw.rect(self.disp, color, self.rect, 1)


class Variable(Block):
	def __init__(self, color, width, height, disp, posx, posy):
		# Call the parent class (Block) constructor
		Block.__init__(self, color, width, height, disp, posx, posy)

	def draw(self, color):
		pygame.draw.rect(self.disp, color, self.rect, 1)
