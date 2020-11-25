import pygame
import pygame.gfxdraw
from .constants import *


class Pawn:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos # Pos: (row, column)
        self.x = self.y = 0 # Real location of piece
        self.calc_pos()

    def calc_pos(self):
        self.x = self.pos[0]*TILE_WIDTH + TILE_WIDTH // 2
        self.y = self.pos[1]*TILE_HEIGHT + TILE_HEIGHT//2 + MARGIN

    def move(self, new_pos):
        self.pos = new_pos
        self.calc_pos()

    def draw(self, win):
        pygame.gfxdraw.filled_circle(win, self.x, self.y, PAWN_RADIUS, self.color)

    def __str__(self):
        return f"Pawn at ({self.pos[0]}, {self.pos[1]})"


class Wall:
    def __init__(self, pos):
        """
        Creates wall
        :param pos: Pos: [(row1, col1), (row2, col2)] -> row1 = row2 or col1 = col2
        """
        self.color = WALL_COLOR
        self.pos = pos
        self.x1 = self.x2 = self.y1 = self.y2 = 0
        self.placed = False

    def place(self, pos):
        self.pos = pos
        self.calc_pos()

    def calc_pos(self):
        self.x1 = self.pos[0][0]*TILE_WIDTH
        self.x2 = self.pos[1][0]*TILE_WIDTH
        self.y1 = self.pos[0][1]*TILE_HEIGHT + MARGIN
        self.y2 = self.pos[1][1]*TILE_HEIGHT + MARGIN

    def draw(self, win):
        pygame.draw.line(win, self.color, (self.x1, self.y1), (self.x2, self.y2), WALL_WIDTH)

