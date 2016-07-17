import pygame
from constants import *


class Wall(object):
	def __init__(self, disp, pos, dims):
		self.rect = pygame.Rect(pos[0], pos[1], dims[0], dims[1])
		self.disp = disp

	def draw(self):
		pygame.draw.rect(self.disp, COLOR_WHITE, self.rect, 1)

	def get_rect(self):
		return self.rect()