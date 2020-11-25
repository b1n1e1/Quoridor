import pygame
from .constants import *
from .board import Board
import pygame.gfxdraw


class Game:
    def __init__(self, win):
        self.win = win
        self.turn = WHITE
        self._init()

    def _init(self):
        self.selected = None
        self.win.fill(TAN)
        self.board = Board()
        self.board.draw(self.win)
        self.player1 = self.board.board[WHITE_START_POS[0]][WHITE_START_POS[1]]
        self.player2 = self.board.board[BLACK_START_POS[0]][BLACK_START_POS[1]]
        self.player1.draw(self.win)
        self.player2.draw(self.win)
        self.winner = lambda: self.board.winner()
        self.valid_moves = []

    def update(self):
        self.board.draw(self.win)
        self.draw_moves(self.valid_moves)
        pygame.display.update()

    def select(self, pos):
        """
        Select tile in pos
        :param pos: Tuple (row, col)
        """
        if self.selected:
            result = self.move(pos)
            if not result:
                self.selected = None
                self.valid_moves = []
                self.select(pos)

        piece = self.board.board[pos[0]][pos[1]].occupied
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.possibleMoves(piece)
            return True  # The piece has been selected
        return False  # No piece has been selected

    def move(self, pos):
        """
        Move piece
        :param pos: Position which the selected piece (self.selected) will be moving to
        :return: True if piece was able to move according to rules, false otherwise
        """
        piece = self.board.board[pos[0]][pos[1]].occupied
        if self.selected and piece == 0 and pos in self.valid_moves:
            self.board.move(self.selected, pos)
            self.next_turn()
        else:
            return False
        return True

    def next_turn(self):
        self.valid_moves = []
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.gfxdraw.aacircle(self.win, row*TILE_WIDTH + TILE_WIDTH // 2, col*TILE_HEIGHT + TILE_HEIGHT // 2 + MARGIN, MOVE_RADIUS, GRAY)
