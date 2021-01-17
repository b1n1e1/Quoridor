from .pieces import *


class Tile:
    def __init__(self, color, piece, pos):
        self.color = color
        self.occupied = piece  # 0 if empty, Pawn object if occupied
        self.pos = pos  # (Number between 0-ROWS-1, Number between 0-ROWS-1)
        self.rect = pygame.Rect(pos, (TILE_WIDTH, TILE_HEIGHT))  # Pygame rectangle of tile
        self.walls = [False for _ in range(4)]  # List of walls adjacent to tile. Order: Left, Top, Right, Bottom

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, WALL_WIDTH)

    def __str__(self):  # Used only for debugging
        if self.occupied == 0:
            return '0'
        return '1'


class Board:
    def __init__(self, n=ROWS):
        self.n = n
        self.board = []
        self.create_board()

    def create_board(self):
        """
        Creates Board as 2d list. Creates ROWS*ROWS board of tiles, adds white piece on bottom and black piece on top
        """
        self.board = [[Tile(TAN, 0, (j*TILE_WIDTH, MARGIN+i*TILE_HEIGHT)) for i in range(ROWS)] for j in range(ROWS)]
        self.board[WHITE_START[0]][WHITE_START[1]].occupied = Pawn(WHITE, (WHITE_START[0],WHITE_START[1]))
        self.board[BLACK_START[0]][BLACK_START[1]].occupied = Pawn(BLACK, (BLACK_START[0],BLACK_START[1]))

    def get_piece(self, pos):
        """
        :param pos: Row,col of tile
        :return: The piece that is in the tile. (0 if no piece is in tile)
        """
        return self.board[pos[0]][pos[1]].occupied

    def draw(self, win):
        """
        Draws board (and margins)
        :param win: Screen (window)
        """
        pygame.draw.rect(win, TAN, pygame.Rect(0, 0, WIDTH, MARGIN))  # Top margin
        pygame.draw.rect(win, BROWN, pygame.Rect(0, MARGIN, WIDTH, BOARD_HEIGHT))  # Board background
        pygame.draw.rect(win, TAN, pygame.Rect(0, MARGIN+BOARD_HEIGHT, WIDTH, MARGIN))  # Bottom margin
        for i in range(ROWS):
            for j in range(ROWS):  # For every single tile on board
                self.board[i][j].draw(win)  # Draw tile
                if self.board[i][j].occupied != 0:  # If there is a pawn in the tile
                    self.board[i][j].occupied.draw(win)  # Draw pawn
                for wall in self.board[i][j].walls:  # For all the items in list of walls
                    if wall:  # If the item isn't False
                        wall.draw(win)  # Draw the wall

    def move(self, piece, pos):
        self.board[piece.pos[0]][piece.pos[1]].occupied = 0  # The tile the piece was in is no longer occupied
        self.board[pos[0]][pos[1]].occupied = piece  # The tile the piece is moving to is now occupied.
        piece.move(pos)

    def place_wall(self, wall, pos):
        """
        Place wall in pos
        :param wall: Wall that is being placed
        :param pos: row,col that wall is being placed
        :return:
        """
        x,y = pos  # x:row, y:col
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

    def unplace_wall(self, wall):
        """
        Remove wall from board.
        :param wall: Wall that's being removed
        """
        x,y = wall.pos[0]  # row,col of top/left point of wall
        if wall.dir == 1:
            self.board[x][y].walls[0] = 0
            self.board[x-1][y].walls[2] = 0
            self.board[x][y+1].walls[0] = 0
            self.board[x-1][y+1].walls[2] = 0
        else:  # If wall is horizontal
            self.board[x][y].walls[1] = 0
            self.board[x][y-1].walls[3] = 0
            self.board[x+1][y].walls[1] = 0
            self.board[x+1][y-1].walls[3] = 0
        wall.unplace()

    def can_place(self, wall, pos):
        """
        Checks if given wall can be placed in given pos
        :param wall: Given wall
        :param pos: Given position (x,y) on board
        :return: True if wall can be placed, False if not (Doesn't place wall either case)
        """
        x, y = pos
        if wall.dir == 1:
            if x == 0 or x == ROWS or y >= ROWS-1 or y < 0:
                return False
            if self.board[x][y].walls[0] or self.board[x][y+1].walls[0]:  # If there is a wall in the same col and pos
                return False
            if self.board[x-1][y+1].walls[1] and self.board[x][y+1].walls[1]:  # If wall is crossing another wall
                return False
        else:
            if x >= ROWS-1 or x < 0 or y == 0 or y == ROWS:
                return False
            if self.board[x][y].walls[1] or self.board[x+1][y].walls[1]:  # If there is a wall in the same row and pos
                return False
            if self.board[x+1][y-1].walls[0] and self.board[x+1][y].walls[0]:  # If wall is crossing another wall
                return False
        return True

    def find_pieces(self):
        """
        Goes through each tile on the board and looks for the pieces.
        :return: List of positions of both pieces on board (list of 2 tuples)
        """
        x = y = 0
        for i in self.board:
            for j in i:
                if j.occupied:
                    if j.occupied.color == WHITE:
                        x = j.occupied.pos
                    else:
                        y = j.occupied.pos
        return x,y

    def possible_moves(self):
        """
        :return: Dictionary of all possible moves in each tile.
        """
        moves = {}
        for x in range(ROWS):
            for y in range(ROWS):
                moves[(x,y)] = []
                walls = self.board[x][y].walls
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
                if x > 0 and not walls[0]:  # Moving left -> No wall on the left and not on first column
                    if self.board[x-1][y].occupied != 0:  # If the tile to the left is occupied
                        if x-1>0 and not self.board[x-1][y].walls[0]:  # If there's no wall behind the piece to the left
                            moves[(x,y)].append((x-2, y))
                        else:  # If there is a wall (or border) behind the piece to the left
                            if not self.board[x-1][y].walls[1] and y>0:  # If there's no wall above piece to the left
                                moves[(x,y)].append((x-1,y-1))
                            if not self.board[x-1][y].walls[3] and y<ROWS-1:  # If there's no wall below piece to the left
                                moves[(x,y)].append((x-1,y+1))
                    else:  # If the tile to the left is empty
                        moves[(x,y)].append((x-1, y))
                if x < ROWS - 1 and not walls[2]:  # Moving right -> No wall on the right and not on last column
                    if self.board[x+1][y].occupied != 0:  # If the tile to the right is occupied
                        if x+1<ROWS-1 and not self.board[x+1][y].walls[2]:  # If there's no wall behind piece to right
                            moves[(x,y)].append((x+2, y))
                        else:  # If there is a wall (or border) behind piece to right
                            if not self.board[x+1][y].walls[1] and y>0:  # If there's no wall above piece to the right
                                moves[(x,y)].append((x+1,y-1))
                            if not self.board[x+1][y].walls[3] and y<ROWS-1:  # If there's no wall below piece to the right
                                moves[(x,y)].append((x+1,y+1))
                    else:  # If the tile to the right is empty
                        moves[(x,y)].append((x+1, y))

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

    def print_board(self):
        """
        Used only for debugging
        """
        for i in range(ROWS):
            s = ""
            for j in range(ROWS):
                s = s+f"{self.board[j][i]} "
            print(s)
