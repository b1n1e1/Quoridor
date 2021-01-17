import pygame
import pygame.gfxdraw
import pygame.font
from copy import copy
from .constants import *
from .board import Board
from .pieces import Wall


class Game:
    """
    Game class
    """
    def __init__(self, win, init=True):
        self.win = win
        if init:
            self.init()
        else:
            self.started = False

    def init(self):
        """
        Start game (or reset)
        """
        self.started = True
        self.selected = None  # No tile is selected
        self.wall_selected = None  # No wall is lifted
        self.turn = WHITE  # First turn is WHITE
        self.board = Board()  # Create board
        self.winner = lambda: self.board.winner()  # Returns winner (None if no one is winning)
        self.valid_moves = []  # List of valid moves for selected piece (currently empty because no piece is selected)
        self.walls = [[Wall(1,RED) for _ in range(WALLS)] for _ in range(2)]  # [player 1 walls, player 2 walls]
        self.walls_remaining = [WALLS, WALLS]  # First is player 1, second is player 2. Walls left for each player
        self.possible = self.board.possible_moves()  # Global variable used for win_possible
        self.min_lengths = []

    def win_possible(self, pos, path, color, depth=0):
        """
        Recursive function that checks if it's possible for a piece of color 'color' to win from its current pos 'pos'
        :param pos: Position on board that is being checked
        :param path: List of all tiles that were already checked (so that it doesn't keep checking the same tiles)
        :param color: Color of piece that is being checked (white needs to get to top, black needs to get to bottom)
        """
        if pos in path:
            return False
        path.append(pos)
        bottom_row = [(i,ROWS-1) for i in range(ROWS-1)]  # All positions in bottom row
        top_row = [(i,0) for i in range(ROWS-1)]  # All positions in top row
        if (color == WHITE and pos in top_row) or (color==BLACK and pos in bottom_row):
            return True
        else:
            return any([self.win_possible(p, path, color, depth+1) for p in self.possible[pos]])
            # Return true if it is possible to win from any of the tiles that the piece can move to

    def can_place(self, pos):
        if self.board.can_place(self.wall_selected, pos):  # If walls aren't intercepting, crossing each other
            self.board.place_wall(self.wall_selected, pos)  # Place wall (only for sake of seeing if move is illegal
            pieces = self.board.find_pieces()  # Positions of both pieces
            self.possible = self.board.possible_moves()  # Only needed for win_possible function. Dict of all moves
            x = self.win_possible(pieces[1], [], BLACK) and self.win_possible(pieces[0 ], [], WHITE)  # True if move is legal
            self.unplace_last_wall()  # Unplace wall (this function is only supposed to check if the wall can be placed)
            self.min_lengths = []
            return x  # If move is legal, return true else false
        return False  # Wall can't be placed because it's illegal

    def place(self, pos):
        x = self.turn == BLACK  # x=0 if turn is white and 1 if turn is black
        if self.walls_remaining[x] > 0 and self.can_place(pos):  # If the placement isn't intercepting another wall
            self.board.place_wall(self.wall_selected, pos)  # Place the wall in pos
            self.walls_remaining[x] -= 1
            self.next_turn()
            return True  # Wall was successfully placed
        return False

    def unplace_last_wall(self):
        """
        This function will only be called right after someone made an illegal move (completely blocked other player).
        Therefore, if the turn is WHITE, the one who made the illegal move is WHITE and the wall that must be removed
        is the last WHITE wall. Walls_remaining didn't subtract 1 yet
        """
        self.board.unplace_wall(self.wall_selected)

    def possible_walls(self):
        """
        This will be a heavy function because it will check for each wall placement possible if the wall can be placed.
        This function will be called at the beginning of the turn for the ai, therefore no wall has been lifted yet.
        :return: List of all possible wall positions.
        """
        walls = [[],[]]
        if self.lift_wall((WIDTH,HEIGHT)):  # Lift outside of board
            for i in range(ROWS):  # Check all vertical walls
                for j in range(ROWS):
                    if self.can_place((i,j)):
                        walls[1].append((i,j))
            self.flip()
            for i in range(ROWS):  # Check all horizontal walls
                for j in range(ROWS):
                    if self.can_place((i,j)):
                        walls[0].append((i,j))
            self.flip()
            self.wall_selected = None
        return walls

    def flip(self):
        """
        Flip selected wall. Does nothing if no wall is selected
        """
        if self.wall_selected:
            self.wall_selected.flip()

    def select(self, pos):
        """
        Select tile in pos
        :param pos: Given x,y position of selected section
        :return: True if worked, False if not
        """
        board_pos = (pos[0] // TILE_WIDTH, (pos[1] - MARGIN) // TILE_HEIGHT)
        if self.wall_selected:  # If a wall is being placed by a human player
            board_pos = (round(pos[0]/TILE_WIDTH), round((pos[1] - MARGIN) / TILE_HEIGHT))  # Closest position to mouse
            self.place(board_pos)
            if self.wall_selected:  # If failed to place a wall
                self.wall_selected = None
                print('Illegal Move')
            return True
        elif self.selected:  # If a piece is currently selected
            result = self.move(board_pos)  # Try to move the currently selected piece to the pos
            if not result:  # If unable to move the piece
                self.selected = None  # Unselect piece
                self.valid_moves = []  # No piece selected so no possible moves
                self.select(pos)  # Select the new tile that was clicked.

        if board_pos[1] > ROWS-1 or board_pos[0] > ROWS-1:
            return False  # If selected beyond range, return False
        piece = self.board.get_piece(board_pos)  # Piece at tile that was selected (if no piece, piece=0)

        if piece != 0 and piece.color == self.turn:
            self.selected = piece  # Next time the board is clicked, the select function will run on this piece
            self.valid_moves = self.board.possible_moves()[(piece.pos[0], piece.pos[1])]  # Update valid moves
            return True  # The piece has been successfully selected
        return False  # No piece has been selected

    def move(self, pos):
        """
        Move piece
        :param pos: Position which the selected piece (self.selected) will be moving to
        :return: True if piece was able to move according to rules, false otherwise
        """
        if pos[1]>ROWS-1 or pos[0]>ROWS-1:  # If pos is above or below the board
            return False  # Can't move the piece above the board or under, return false

        piece = self.board.get_piece(pos)  # Needs to be 0, if not then the piece cannot move to the given place
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
        print(self.possible)

    def draw_moves(self, moves):
        """
        Draw all possible moves for selected pawn.
        :param moves: List of all possible moves. (self.valid_moves)
        """
        for move in moves:
            row, col = move
            pygame.gfxdraw.aacircle(self.win, row*TILE_WIDTH + TILE_WIDTH // 2,
                                    col*TILE_HEIGHT + TILE_HEIGHT // 2 + MARGIN, MOVE_RADIUS, GRAY)

    def walls_left(self):
        """
        Writes in margins how many walls are left for each player
        """
        txt = [0,0]
        for i in range(2):
            txt[i] = FONT.render(f'{self.walls_remaining[i]} walls left.', True, BLACK)
            w, h = txt[i].get_size()
            self.win.blit(txt[i],
                          ((WIDTH - w) // 2, (MARGIN + BOARD_HEIGHT) * (1 - i) + (MARGIN - h) // 2))

    def all_possible_moves(self):
        return {'moves':self.valid_moves, 'walls':self.possible_walls()}


    def lift_wall(self, pos):
        """
        Lift a wall. The wall that will be lifted is the first wall in the player's list that hasn't been placed yet.
        This function will only be used for human players because the computer can automatically place a wall without
        having to lift it first
        :param pos: Mouse position.
        """
        if self.selected:
            self.select((ROWS,ROWS))  # If a piece was chosen, unselect the piece and select a wall instead.
        turn = self.turn == BLACK
        if self.walls_remaining[turn] == 0:
            return False  # If player 1 has no walls left, they can't lift another wall
        self.wall_selected = self.walls[turn][WALLS-self.walls_remaining[turn]]
        self.wall_selected.lift(pos)  # Lift the first wall in the list which hasn't been placed yet
        return True

    def update(self, pos=None):
        """
        Every frame, the update function will run. This takes care of the graphics so that they truly remain correct
        throughout each frame
        :param pos: Mouse position
        """
        self.board.draw(self.win)  # This will draw the tiles, walls and pawns
        self.draw_moves(self.valid_moves)  # This will draw the possible moves as long as there is a selected piece
        self.walls_left()  # This updates in the margins that they will have the correct amount written
        if self.wall_selected:  # If a wall is being lifted, constantly make the wall follow the position of mouse
            self.lift_wall(pos)
            self.wall_selected.draw(self.win)
        pygame.display.update()

    def evaluate(self):
        """
        Used for ai
        :return: The value of the current position (how good it is for the white player). White will want to
        maximize this value while black will want to minimize it (minimax).
        """
        pass
