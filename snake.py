import pygame
from constants import *


class Snake:
	def __init__(self, disp, posx, posy, startdirection):
		self.disp = disp
		self.head = Head(COLOR_BLACK, BLOCK_DIM, BLOCK_DIM, disp, posx, posy)
		self.variables = []
		self.turns = []
		"""for i in range(0,10):
			self.variables.append(Variable(COLOR_BLACK, BLOCK_DIM, BLOCK_DIM, disp, 0, 0))
			self.variables[i].set_index(i+ 1)
			self.variables[i].set_direction(startdirection)"""
		self.head.set_direction(startdirection)
		self.turn_cnt = len(self.variables )

	def draw(self):
		self.head.draw(COLOR_WHITE)
		for var in self.variables:
			var.draw(COLOR_WHITE)

	def add_turn(self, direction):
		self.head.set_direction(direction)
		turn = Turn(direction, self.head.get_x_coord(), self.head.get_y_coord(), min(len(self.variables) + 1, self.turn_cnt))
		self.turns.append(turn)
		for var in self.variables:
			var.add_turn(turn)
		self.turn_cnt = 0

	def update(self):
		self.turn_cnt += 1
		self.move_head()
		self.calc_var_moves()
		for var in self.variables:
			self.move_var(var)

	def collect_variable(self, variable):
		variable.set_index(len(self.variables) + 1)
		variable.set_direction(self.get_head_direction())
		self.variables.append(variable)


	def get_head_direction(self):
		return self.head.get_direction()

	def get_variables(self):
		return self.variables

	def calc_var_moves(self):
		for var in self.variables:
			if var.is_turning():
				turn = var.get_current_turn()
				var.inc_turn_cnt()
				if var.get_x_coord() == turn.get_x_coord() and var.get_y_coord() == turn.get_y_coord():
					var.reset_turn_cnt()
					var.set_direction(turn.get_direction())
					var.shift_turn_list()


	def move_head(self):
		direction = self.head.get_direction()
		x_coord = self.head.get_x_coord()
		y_coord = self.head.get_y_coord()
		if direction is "l":
			self.head.update_x_coord(x_coord - BLOCK_DIM)
		elif direction is "r":
			self.head.update_x_coord(x_coord + BLOCK_DIM)
		elif direction is "u":
			self.head.update_y_coord(y_coord - BLOCK_DIM)
		elif direction is "d":
			self.head.update_y_coord(y_coord + BLOCK_DIM)


	def move_var(self, block):
		if block.is_turning():
			turn = block.get_current_turn()
			ref_x = turn.get_x_coord()
			ref_y = turn.get_y_coord()
			block_x = block.get_x_coord()
			block_y = block.get_y_coord()
			cnt = min([block.get_index(), turn.get_length()-1]) - block.get_turn_cnt()

		else:
			if block.get_index() > 1:
				ref_x = self.variables[block.get_index() -2].get_x_coord()
				ref_y = self.variables[block.get_index() - 2].get_y_coord()
			else:
				ref_x = self.head.get_x_coord()
				ref_y = self.head.get_y_coord()
			cnt = 1

		direction = block.get_direction()

		if direction is "l":
			block.update_x_coord(ref_x + BLOCK_DIM * cnt)
			block.update_y_coord(ref_y)
		elif direction is "r":
			block.update_x_coord(ref_x - BLOCK_DIM * cnt)
			block.update_y_coord(ref_y)
		elif direction is "u":
			block.update_y_coord(ref_y + BLOCK_DIM * cnt)
			block.update_x_coord(ref_x)
		elif direction is "d":
			block.update_y_coord(ref_y - BLOCK_DIM * cnt)
			block.update_x_coord(ref_x)

		block_x = block.get_x_coord()
		block_y = block.get_y_coord()


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

	def get_rect(self):
		return self.rect

	def draw(self, color):
		raise NotImplementedError




class Head(Block):
	def __init__(self, color, width, height, disp, posx, posy):
		# Call the parent class (Block) constructor
		Block.__init__(self, color, width, height, disp, posx, posy)
		self.direction = ""

	def draw(self, color):
		pygame.draw.rect(self.disp, color, self.rect, 1)

	def set_direction(self, direction):
		self.direction = direction

	def get_direction(self):
		return self.direction




class Variable(Block):
	def __init__(self, color, width, height, disp, posx, posy):
		# Call the parent class (Block) constructor
		Block.__init__(self, color, width, height, disp, posx, posy)
		self.change_dir = False
		self.index = 0
		self.font = pygame.font.Font(None, 18)
		self.font_image = self.font.render(str(self.index), True, COLOR_WHITE)
		self.turns = []
		self.direction = ''
		self.turn_cnt = 0

	def draw(self, color):
		pygame.draw.rect(self.disp, color, self.rect, 1)
		self.disp.blit(self.font_image, (self.get_x_coord() + BLOCK_DIM/2, self.get_y_coord() + BLOCK_DIM/2))

	def set_index(self, index):
		self.index = index
		self.font_image = self.font.render(str(self.index), True, COLOR_WHITE)

	def get_index(self):
		return self.index

	def set_direction(self, direction):
		self.direction = direction

	def get_direction(self):
		return self.direction

	def add_turn(self, turn):
		self.turns.append(turn)

	def get_current_turn(self):
		return self.turns[0]

	def shift_turn_list(self):
		self.turns[:] = self.turns[1:]

	def is_turning(self):
		if self.turns:
			return True
		else:
			return False

	def get_turn_cnt(self):
		return self.turn_cnt

	def inc_turn_cnt(self):
		self.turn_cnt += 1

	def reset_turn_cnt(self):
		self.turn_cnt = 0




class Turn:

	def __init__(self, direction, x_coord, y_coord, length):
		self.direction = direction
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.length = length

	def get_direction(self):
		return self.direction

	def get_x_coord(self):
		return self.x_coord

	def get_y_coord(self):
		return self.y_coord

	def get_length(self):
		return self.length

	def set_length(self, length):
		self.length = length


