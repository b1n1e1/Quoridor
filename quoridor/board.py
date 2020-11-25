import pygame
from .constants import *
from.pieces import Wall, Pawn


class Tile:
    def __init__(self, color, piece, pos):
        self.color = color
        self.occupied = piece
        self.pos = pos
        self.rect = pygame.Rect(pos, (TILE_WIDTH, TILE_HEIGHT))
        self.walls = [False for _ in range(4)]
        # Self.walls: List of walls adjacent to tile. Order: Left, Top, Right, Bottom

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, WALL_WIDTH)


    def __str__(self):
        if self.occupied == 0:
            return '0'
        return '1'


class Board:
    def __init__(self, n=ROWS):
        self.n = n
        self.board = []
        self.createBoard()

    def createBoard(self):
        """
        Creates Board as 2d list. First # is on horizontal axis, second is vertical axis
        """
        self.board = [[Tile(TAN, 0, (j*TILE_WIDTH, MARGIN+i*TILE_HEIGHT)) for i in range(ROWS)] for j in range(COLS)]
        self.board[WHITE_START_POS[0]][WHITE_START_POS[1]].occupied = Pawn(WHITE, (WHITE_START_POS[0],WHITE_START_POS[1]))
        self.board[BLACK_START_POS[0]][BLACK_START_POS[1]].occupied = Pawn(BLACK, (BLACK_START_POS[0],BLACK_START_POS[1]))

    def draw(self, win):
        """
        Creates Visual Board.
        :param win: Window
        """
        pygame.draw.rect(win, BROWN, pygame.Rect(0, MARGIN, WIDTH, BOARD_HEIGHT))
        for i in self.board:
            for j in i:
                j.draw(win)
                if j.occupied != 0:
                    j.occupied.draw(win)

    def move(self, piece, pos):
        self.board[piece.pos[0]][piece.pos[1]].occupied = 0
        self.board[pos[0]][pos[1]].occupied = piece
        piece.move(pos)

    def possibleMoves(self, piece):
        moves = []
        x, y = piece.pos[0], piece.pos[1]
        if x > 0:
            if self.board[x-1][y].occupied != 0:
                if x-1>0:
                    moves.append((x-2, y))
            else:
                moves.append((x-1, y))
        if x < ROWS - 1:
            if self.board[x+1][y].occupied != 0:
                if x+1<ROWS-1:
                    moves.append((x+2, y))
            else:
                moves.append((x+1, y))
        if y > 0:
            if self.board[x][y-1].occupied != 0:
                if y-1>0:
                    moves.append((x, y-2))
            else:
                moves.append((x, y-1))
        if y < COLS - 1:
            if self.board[x][y+1].occupied != 0:
                if y+1 < COLS - 1:
                    moves.append((x, y+2))
            else:
                moves.append((x, y+1))
        return moves

    def winner(self):
        if any([self.board[i][0].occupied != 0 and self.board[i][0].occupied.color == WHITE for i in range(COLS)]):
            return WHITE
        if any([self.board[i][ROWS-1].occupied != 0 and self.board[i][ROWS-1].occupied.color == BLACK for i in range(COLS)]):
            return BLACK
        return None

    """def printBoard(self):
        for i in self.board:
            print(f"{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]} {i[7]} {i[8]}")
    """