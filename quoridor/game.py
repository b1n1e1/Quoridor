import pygame
import pygame.gfxdraw
import pygame.font
from .constants import *
from .board import Board
from.pieces import Wall


class Game:
    def __init__(self, win):
        self.win = win
        self._init()

    def _init(self):
        """
        Start game (or reset)
        """
        self.selected = None
        self.wall_selected = None
        self.turn = WHITE
        self.board = Board()
        self.board.draw(self.win)
        self.winner = lambda: self.board.winner()
        self.valid_moves = []
        self.player1Walls = [Wall((0, 0), 1, LIGHTBLUE) for _ in range(10)]
        self.player2Walls = [Wall((0, 0), 1, BLUE) for _ in range(10)]
        self.wallsLeft1 = 10
        self.wallsLeft2 = 10
        self.wallsLeftText1 = FONT.render('10 walls left.', True, BLACK)
        self.wallsLeftText2 = FONT.render('10 walls left.', True, BLACK)

    def place(self, pos):
        if self.turn == WHITE:
            if self.wallsLeft1 == 0:
                return False
            wall = self.player1Walls[10-self.wallsLeft1]
            if self.can_place(wall, pos):
                self.wallsLeft1 -= 1
                self.board.placeWall(wall, pos)
                self.next_turn()
                return True
        else:
            if self.wallsLeft2 == 0:
                return False
            wall = self.player2Walls[10-self.wallsLeft2]
            if self.can_place(wall, pos):
                self.wallsLeft2 -= 1
                self.board.placeWall(wall, pos)
                self.next_turn()
                return True
        return False

    def can_place(self, wall, pos):
        return self.board.can_place(wall, pos)

    def walls_left(self):
        """
        Writes in margins how many walls are left for each player
        :return:
        """
        self.wallsLeftText1 = FONT.render(f'{self.wallsLeft1} walls left.', True, BLACK)
        w1, h1 = self.wallsLeftText1.get_size()
        self.win.blit(self.wallsLeftText1, ((WIDTH - w1) // 2, MARGIN + BOARD_HEIGHT + (MARGIN - h1) // 2))
        self.wallsLeftText2 = FONT.render(f'{self.wallsLeft2} walls left.', True, BLACK)
        w2, h2 = self.wallsLeftText2.get_size()
        self.win.blit(self.wallsLeftText2, ((WIDTH-w2)//2, (MARGIN-h2)//2))

    def update(self, pos=None):
        """
        Every frame, the update function will run. This takes care of the graphics so that they truly remain correct
        throughout each frame
        :param pos: Mouse position
        """
        self.board.draw(self.win)
        self.draw_moves(self.valid_moves)
        self.walls_left()
        for w1, w2 in zip(self.player1Walls, self.player2Walls):
            if w1.placed:
                w1.draw(self.win)
            if w2.placed:
                w2.draw(self.win)
        if self.wall_selected:
            self.lift_wall(pos)
            self.wall_selected.draw(self.win)
        pygame.display.update()

    def select(self, pos):
        """
        Select tile in pos
        :param pos: Given x,y position of selected section
        :return: True if worked, False if not
        """
        board_pos = (pos[0] // TILE_WIDTH, (pos[1] - MARGIN) // TILE_HEIGHT)
        if self.wall_selected:  # If a wall is being placed by a human player
            board_pos = (round(pos[0]/TILE_WIDTH), round((pos[1] - MARGIN) / TILE_HEIGHT))  # Closest position to mouse
            if self.wall_selected.dir == 0:
                if board_pos[0] == ROWS-1 or board_pos[1] < 1 or board_pos[1] > ROWS-1:
                    self.wall_selected = None
                    return False  # If selected pos is outside of the board
            else:
                if board_pos[0] == 0 or board_pos[0] == ROWS or board_pos[1] >= ROWS-1 or board_pos[1] < 0:
                    self.wall_selected = None
                    return False  # If selected pos is outside of the board
            self.place(board_pos)
            if self.wall_selected:  # If failed to place a wall
                self.wall_selected = None
            return True
        elif self.selected:  # If a piece is currently selected
            result = self.move(board_pos)  # Try to move the currently selected piece to the pos
            if not result:  # If unable to move the piece
                self.selected = None  # Unselect piece
                self.valid_moves = []  # No piece selected so no possible moves
                self.select(pos)  # Select the new tile that was clicked.

        if board_pos[1] > ROWS-1 or board_pos[0] > ROWS-1:
            return False  # If selected beyond range, return False
        piece = self.board.getPiece(board_pos)  # Piece at tile that was selected (if no piece, piece=0)

        if piece != 0 and piece.color == self.turn:
            self.selected = piece  # Update selected piece. Next time the board is clicked, the select function will run on this piece
            self.valid_moves = self.board.possibleMoves()[(piece.pos[0], piece.pos[1])]  # Update valid moves based on selected piece
            return True  # The piece has been successfully selected
        return False  # No piece has been selected

    def move(self, pos):
        """
        Move piece
        :param pos: Position which the selected piece (self.selected) will be moving to
        :return: True if piece was able to move according to rules, false otherwise
        """
        if pos[1]>ROWS-1 or pos[0]>ROWS-1:  # Can't move the piece above the board or under
            return False  # Can't move the piece above the board or under, return false

        piece = self.board.getPiece(pos)  # Needs to be 0, if not then the piece cannot move to the given place
        if self.selected and piece == 0 and pos in self.valid_moves:
            self.board.move(self.selected, pos)  # Move the selected piece to the pos if it's a valid move
            self.next_turn()
        else:
            return False  # Unable to move piece, return False
        return True  # Piece successfully moved

    def next_turn(self):
        """
        Reset the selections and change the turn
        """
        self.valid_moves = []  # There are no valid moves because no pawn has been selected
        self.wall_selected = None  # Unselect any walls when changing turns
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_moves(self, moves):
        """
        Draw all possible moves for selected pawn.
        :param moves: List of all possible moves. (self.valid_moves)
        """
        color = GRAY
        for move in moves:
            row, col = move
            pygame.gfxdraw.aacircle(self.win, row*TILE_WIDTH + TILE_WIDTH // 2, col*TILE_HEIGHT + TILE_HEIGHT // 2 + MARGIN, MOVE_RADIUS, color)

    def lift_wall(self, pos):
        """
        Lift a wall. The wall that will be lifted is the first wall in the player's list that hasn't been placed yet.
        This function will only be used for human players because the computer can automatically place a wall without
        having to lift it first
        :param pos: Mouse position.
        """
        if self.selected:
            self.select((ROWS,ROWS))  # If a piece was chosen, unselect the piece and select a wall instead.
        if self.turn == WHITE:
            if self.wallsLeft1 == 0:
                return False  # If player 1 has no walls left, they can't lift another wall
            self.wall_selected = self.player1Walls[10-self.wallsLeft1]
            self.wall_selected.lift(pos)  # Lift the first wall in the list which hasn't been placed yet
        else:
            if self.wallsLeft2==0:
                return False  # If player 2 has no walls left, they can't lift another wall
            self.wall_selected = self.player2Walls[10-self.wallsLeft2]
            self.wall_selected.lift(pos)  # Lift the first wall in the list which hasn't been placed yet

    def flip(self):
        """
        Flip selected wall
        """
        if self.wall_selected:
            self.wall_selected.flip()
