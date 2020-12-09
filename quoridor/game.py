import pygame
import pygame.gfxdraw
import pygame.font
from .constants import *
from .board import Board
from .pieces import Wall


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
        self.winner = lambda: self.board.winner()
        self.valid_moves = []
        self.player1Walls = [Wall((0, 0), 1, RED) for _ in range(10)]
        self.player2Walls = [Wall((0, 0), 1, RED) for _ in range(10)]
        self.walls_remaining = [10,10]
        self.walls_remaining_text = [FONT.render('10 walls left.', True, BLACK), FONT.render('10 walls left.', True, BLACK)]

    def win_possible(self, pos, sent_from):
        """
        Returns true if it's possible to win from both pos (pos isn't completely blocked off by walls)
        """
        try:
            pos1, pos2 = pos
            BOTTOM_ROW = [(i,ROWS) for i in range(ROWS)]
            TOP_ROW = [(i,0) for i in range(ROWS)]
            all_moves = self.board.possible_moves()
            if any([i in TOP_ROW for i in all_moves[pos1]]):
                return True
            elif pos1 in sent_from:
                return False
            else:
                sent_from.append(pos1)
                return any([self.win_possible([p, 0], sent_from) for p in all_moves[pos1]])
        except:
            return False

    def can_place(self, wall, pos):
        if self.board.can_place(wall, pos):  # If walls aren't intercepting, crossing each other
            pos = self.board.find_pieces()
            if self.win_possible(pos, []):
                return True
        return False

    def place(self, pos):
        if self.turn == WHITE:
            if self.walls_remaining[0] == 0:
                return False
            wall = self.player1Walls[10-self.walls_remaining[0]]
            if self.can_place(wall, pos):
                self.walls_remaining[0] -= 1
                self.board.place_wall(wall, pos)
                if not self.win_possible(self.board.find_pieces(), []):
                    self.walls_remaining[0] += 1
                    self.player1Walls[10-self.walls_remaining[0]].placed = False
                self.next_turn()
                return True
        else:
            if self.walls_remaining[1] == 0:
                return False
            wall = self.player2Walls[10-self.walls_remaining[1]]
            if self.can_place(wall, pos):
                self.walls_remaining[1] -= 1
                self.board.place_wall(wall, pos)
                self.next_turn()
                return True
        return False

    def flip(self):
        """
        Flip selected wall. Does nothing if no wall is selected
        """
        if self.wall_selected:
            self.wall_selected.flip()

    def walls_left(self):
        """
        Writes in margins how many walls are left for each player
        :return:
        """
        self.walls_remaining_text[0] = FONT.render(f'{self.walls_remaining[0]} walls left.', True, BLACK)
        w, h = self.walls_remaining_text[0].get_size()
        self.win.blit(self.walls_remaining_text[0], ((WIDTH - w) // 2, MARGIN + BOARD_HEIGHT + (MARGIN - h) // 2))
        self.walls_remaining_text[1] = FONT.render(f'{self.walls_remaining[1]} walls left.', True, BLACK)
        w, h = self.walls_remaining_text[1].get_size()
        self.win.blit(self.walls_remaining_text[1], ((WIDTH-w)//2, (MARGIN-h)//2))

    def select(self, pos):
        """
        Select tile in pos
        :param pos: Given x,y position of selected section
        :return: True if worked, False if not
        """
        board_pos = (pos[0] // TILE_WIDTH, (pos[1] - MARGIN) // TILE_HEIGHT)
        if self.wall_selected:  # If a wall is being placed by a human player
            board_pos = (round(pos[0]/TILE_WIDTH), round((pos[1] - MARGIN) / TILE_HEIGHT))  # Closest position to mouse
            if self.wall_selected.dir == 0:  # If wall is horizontal
                if board_pos[0] == ROWS-1 or board_pos[1] < 1 or board_pos[1] > ROWS-1:  # If selected pos is outside of the board
                    self.wall_selected = None  # Unselect current lifted wall
                    return False
            else:
                if board_pos[0] == 0 or board_pos[0] == ROWS or board_pos[1] >= ROWS-1 or board_pos[1] < 0:  # If selected pos is outside of the board
                    self.wall_selected = None  # Unselect current lifted wall
                    return False
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
        piece = self.board.get_piece(board_pos)  # Piece at tile that was selected (if no piece, piece=0)

        if piece != 0 and piece.color == self.turn:
            self.selected = piece  # Update selected piece. Next time the board is clicked, the select function will run on this piece
            self.valid_moves = self.board.possible_moves()[(piece.pos[0], piece.pos[1])]  # Update valid moves based on selected piece
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
        print(self.win_possible(self.board.find_pieces(), []))

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
            if self.walls_remaining[0] == 0:
                return False  # If player 1 has no walls left, they can't lift another wall
            self.wall_selected = self.player1Walls[10-self.walls_remaining[0]]
            self.wall_selected.lift(pos)  # Lift the first wall in the list which hasn't been placed yet
        else:
            if self.walls_remaining[1]==0:
                return False  # If player 2 has no walls left, they can't lift another wall
            self.wall_selected = self.player2Walls[10-self.walls_remaining[1]]
            self.wall_selected.lift(pos)  # Lift the first wall in the list which hasn't been placed yet

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
