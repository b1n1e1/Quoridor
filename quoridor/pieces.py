import pygame
import pygame.gfxdraw
from .constants import *


class Pawn:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos  # Pos: (row, column)
        self.x = self.y = 0  # Real location of piece
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
    def __init__(self, pos, dir, color):
        """
        Creates wall
        :param pos: Pos: (row1, col1) If horizontal: Left point. If Vertical: Top point
        :param dir: Horizontal:0, Vertical:1
        :param color: Color
        """
        self.color = color
        self.pos = []
        self.dir = dir
        self.x1 = self.x2 = self.y1 = self.y2 = 0
        self.placed = False  # Will be true when the wall is placed on the board and can no longer be moved.
        self.lifted = False  # Will be true when the wall is selected (when the player presses space)
        self.find_pos(pos)  # Will find the pos of the second point of the wall.

    def find_pos(self, first_pos):
        if self.placed:
            if self.dir == 0:
                self.pos = [first_pos, (first_pos[0]+2, first_pos[1])]
            else:
                self.pos = [first_pos, (first_pos[0], first_pos[1]+2)]
        else:
            if self.dir == 0:
                self.pos = [first_pos, (first_pos[0]+WALL_HEIGHT, first_pos[1])]
            else:
                self.pos = [first_pos, (first_pos[0], first_pos[1]+WALL_HEIGHT)]
        self.calc_pos()

    def flip(self):
        if not self.placed:
            self.dir = 1 - self.dir

    def lift(self, pos):
        self.lifted = True
        self.find_pos(pos)

    def place(self, pos):
        self.lifted = False
        self.placed = True
        self.find_pos(pos)

    def calc_pos(self):
        if self.placed:
            self.x1 = self.pos[0][0]*TILE_WIDTH
            self.x2 = self.pos[1][0]*TILE_WIDTH
            self.y1 = self.pos[0][1]*TILE_HEIGHT + MARGIN
            self.y2 = self.pos[1][1]*TILE_HEIGHT + MARGIN
        else:
            self.x1 = self.pos[0][0]
            self.x2 = self.pos[1][0]
            self.y1 = self.pos[0][1]
            self.y2 = self.pos[1][1]


    def draw(self, win):
        pygame.draw.line(win, self.color, (self.x1-1, self.y1-1), (self.x2-1, self.y2-1), WALL_WIDTH+1)

    def __str__(self):
        return f"Wall at {self.pos[0]}, {self.pos[1]}"
