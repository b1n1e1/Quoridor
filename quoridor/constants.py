import pygame.font
pygame.font.init()

# Sizes
WIDTH, HEIGHT = 450,670
ROWS = 9  # Amount of rows and columns, board needs to be square
MARGIN = 110
BOARD_HEIGHT = HEIGHT - (2 * MARGIN)

TILE_WIDTH = WIDTH//ROWS
TILE_HEIGHT = BOARD_HEIGHT//ROWS

WALLS = 10
WALL_WIDTH = 5
WALL_HEIGHT = 2 * TILE_HEIGHT
PAWN_RADIUS = TILE_WIDTH//3
MOVE_RADIUS = TILE_WIDTH//7

# Positions
WHITE_START_POS = ((ROWS-1)//2,ROWS-1)
BLACK_START_POS = ((ROWS-1)//2,0)

# Font
FONT = pygame.font.SysFont('comicsansms', 30)

# Colors
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
TAN = (210,180,140)
BROWN = (64, 32, 11)
GRAY = (150,150,150)
BLUE = (0,0,255)
GREEN = (0,200,0)
LIGHTBLUE = (52,155,229)
LIGHTPINK = (214,105,255)