import pygame
import sys
from gamescreen import GameScreen
from constants import *


def main():
	try:
		pygame.init()
		disp = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), False, False)
		pygame.display.set_caption("pysnake")
	except pygame.error:
		print "Pygame failed to initialize"
	clk = pygame.time.Clock()
	gamescreen = GameScreen(disp, clk)
	gamescreen.run()
	return 1

if __name__ == "__main__":
	status = main()
	sys.exit(status)