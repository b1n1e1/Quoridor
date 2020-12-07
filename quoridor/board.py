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
        self.board = [[Tile(TAN, 0, (j*TILE_WIDTH, MARGIN+i*TILE_HEIGHT)) for i in range(ROWS)] for j in range(ROWS)]
        self.board[WHITE_START_POS[0]][WHITE_START_POS[1]].occupied = Pawn(WHITE, (WHITE_START_POS[0],WHITE_START_POS[1]))
        self.board[BLACK_START_POS[0]][BLACK_START_POS[1]].occupied = Pawn(BLACK, (BLACK_START_POS[0],BLACK_START_POS[1]))

    def getPiece(self, pos):
        return self.board[pos[0]][pos[1]].occupied

    def draw(self, win):
        """
        Creates Visual Board.
        :param win: Window
        """
        pygame.draw.rect(win, TAN, pygame.Rect(0, 0, WIDTH, MARGIN))
        pygame.draw.rect(win, BROWN, pygame.Rect(0, MARGIN, WIDTH, BOARD_HEIGHT))
        pygame.draw.rect(win, TAN, pygame.Rect(0, MARGIN+BOARD_HEIGHT, WIDTH, MARGIN))
        for i in range(ROWS):
            for j in range(ROWS):
                self.board[i][j].draw(win)
                if self.board[i][j].occupied != 0:
                    self.board[i][j].occupied.draw(win)
                for wall in self.board[i][j].walls:
                    if wall:
                        wall.draw(win)

    def move(self, piece, pos):
        self.board[piece.pos[0]][piece.pos[1]].occupied = 0
        self.board[pos[0]][pos[1]].occupied = piece
        piece.move(pos)

    def placeWall(self, wall, pos):
        x,y = pos
        if wall.dir == 1:  # If wall is vertical
            self.board[x][y].walls[0] = wall
            self.board[x-1][y].walls[2] = wall
            self.board[x][y+1].walls[0] = wall
            self.board[x-1][y+1].walls[2] = wall
        else:  # If wall is horizontal
            self.board[x][y].walls[1] = wall
            self.board[x][y-1].walls[3] = wall
            self.board[x+1][y].walls[1] = wall
            self.board[x+1][y-1].walls[3] = wall
        wall.place(pos)

    def possibleMoves(self):
        """
        :return: Dictionary of all possible moves in each tile.
        """
        moves = {}
        for x in range(ROWS):
            for y in range(ROWS):
                moves[(x,y)] = []
                walls = self.board[x][y].walls
                if x > 0 and not walls[0]:  # Moving left -> No wall on the left and not on first column
                    if self.board[x-1][y].occupied != 0:  # If the tile to the left is occupied
                        if x-1>0 and not self.board[x-1][y].walls[0]:  # If there's no wall behind the piece to the left
                            moves[(x,y)].append((x-2, y))
                        else:  # If there is a wall (or border) behind the piece to the left
                            if not self.board[x-1][y].walls[1]:  # If there's no wall above piece to the left
                                moves[(x,y)].append((x-1,y-1))
                            if not self.board[x-1][y].walls[3]:  # If there's no wall below piece to the left
                                moves[(x,y)].append((x-1,y+1))
                    else:  # If the tile to the left is empty
                        moves[(x,y)].append((x-1, y))
                if x < ROWS - 1 and not walls[2]:  # Moving right -> No wall on the right and not on last column
                    if self.board[x+1][y].occupied != 0:  # If the tile to the right is occupied
                        if x+1<ROWS-1 and not self.board[x+1][y].walls[2]:  # If there's no wall behind piece to right
                            moves[(x,y)].append((x+2, y))
                        else:  # If there is a wall (or border) behind piece to right
                            if not self.board[x+1][y].walls[1]:  # If there's no wall above piece to the right
                                moves[(x,y)].append((x+1,y-1))
                            if not self.board[x+1][y].walls[3]:  # If there's no wall below piece to the right
                                moves[(x,y)].append((x+1,y+1))
                    else:  # If the tile to the right is empty
                        moves[(x,y)].append((x+1, y))
                if y > 0 and not walls[1]:  # Moving up -> No wall above and not on top row
                    if self.board[x][y-1].occupied != 0:  # If the tile above is occupied
                        if y-1>0 and not self.board[x][y-1].walls[1]:  # If there's no wall (or border) over piece above
                            moves[(x,y)].append((x, y-2))
                        else:  # If there's a wall over the piece above
                            if not self.board[x][y-1].walls[0]:  # If there's no wall left of piece above
                                moves[(x,y)].append((x-1,y-1))
                            if not self.board[x][y-1].walls[2]:  # If there's no wall right of piece above
                                moves[(x,y)].append((x+1,y-1))
                    else:  # If the tile above is empty
                        moves[(x,y)].append((x, y-1))
                if y < ROWS - 1 and not walls[3]:  # Moving down -> No wall beneath and not on bottom row
                    if self.board[x][y+1].occupied != 0:  # If the tile below is occupied
                        if y+1<ROWS-1 and not self.board[x][y+1].walls[3]:  # If there's no wall under piece below
                            moves[(x,y)].append((x, y+2))
                        else:  # If there's a wall under the piece below
                            if not self.board[x][y+1].walls[0]:  # If there's no wall left of piece below
                                moves[(x,y)].append((x-1,y+1))
                            if not self.board[x][y+1].walls[2]:  # If there's no wall right of piece below
                                moves[(x,y)].append((x+1,y+1))
                    else:  # If the tile below is empty
                        moves[(x,y)].append((x, y+1))
        return moves

    def winner(self):
        """
        :return: WHITE if any of the tiles on top are occupied by white, BLACK if any of the tiles on bottom are
        occupied by black, None if neither.
        """
        if any([self.board[i][0].occupied != 0 and self.board[i][0].occupied.color == WHITE for i in range(ROWS)]):
            return WHITE
        if any([self.board[i][ROWS-1].occupied != 0 and self.board[i][ROWS-1].occupied.color == BLACK for i in range(ROWS)]):
            return BLACK
        return None

    def printBoard(self):
        for i in range(ROWS):
            s = ""
            for j in range(ROWS):
                s = s+f"{self.board[j][i]} "
            print(s)
