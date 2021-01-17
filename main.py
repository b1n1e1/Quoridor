import pygame
import copy
from datetime import datetime
from random import randint as rint
from quoridor.constants import *
from quoridor.game import Game

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Quoridor')
game = Game(WIN, False)

quoridor = FONT.render('Quoridor!', True, BLACK)
click = FONT.render('Click here to start game.', True, WHITE, BLACK)

WIN.fill(TAN)
WIN.blit(quoridor, ((WIDTH - quoridor.get_size()[0]) // 2, 240))
WIN.blit(click, ((WIDTH - click.get_size()[0]) //2, 300))


def main():
    run = True
    while run:
        if not game.started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    game.init()
                if event.type == pygame.KEYDOWN:
                    WIN.fill(TAN)
                    rules = FONT.render('RULES', True, BLACK)
                    WIN.blit(rules, ((WIDTH-rules.get_size()[0]) //2, 100))
            pygame.display.update()

        else:
            if game.winner():
                print('White wins.') if game.winner()==WHITE else print('Black wins.')
                run = False
            if run:  # change to if game.turn == WHITE
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        game.select(pos)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:
                            if game.wall_selected:
                                game.wall_selected = None
                            else:
                                game.lift_wall(pygame.mouse.get_pos())
                        if event.key == pygame.K_f:
                            game.flip()
                        if event.key == pygame.K_g:
                            time = datetime.now()
                            print(game.all_possible_moves())
                            print(datetime.now()-time)
                        if event.key == pygame.K_l:
                            time = datetime.now()
                            global x
                            x = copy.deepcopy(game.board)
                            print(datetime.now()-time)
                        if event.key == pygame.K_t:
                            game.board = x

            elif not run:
                if game.turn == BLACK:
                    if rint(0, 1) and game.walls_remaining[1] > 0:
                        game.lift_wall((0, 0))
                        a = rint(0, 1)
                        if a == 1:
                            game.flip()
                        x, y = rint(1, 7), rint(1, 7)
                        while not game.place((x, y)) and game.walls_remaining[1] > 0:
                            x, y = rint(1, 7), rint(1, 7)
                    else:
                        piece = game.board.find_pieces()[1]
                        game.select((piece[0]*TILE_WIDTH+1, piece[1]*TILE_HEIGHT+1+MARGIN))
                        moves = game.valid_moves
                        x = rint(0, len(moves)-1)
                        game.select((moves[x][0]*TILE_WIDTH+1, moves[x][1]*TILE_HEIGHT+1+MARGIN))
                else:
                    if rint(0, 1) and game.walls_remaining[0] > 0:
                        game.lift_wall((0, 0))
                        a = rint(0, 1)
                        if a == 1:
                            game.flip()
                        x, y = rint(1, 7), rint(1, 7)
                        while not game.place((x, y)) and game.walls_remaining[0] > 0:
                            x, y = rint(1, 7), rint(1, 7)
                    else:
                        piece = game.board.find_pieces()[0]
                        game.select((piece[0]*TILE_WIDTH+1, piece[1]*TILE_HEIGHT+1+MARGIN))
                        moves = game.valid_moves
                        x = rint(0, len(moves)-1)
                        game.select((moves[x][0]*TILE_WIDTH+1, moves[x][1]*TILE_HEIGHT+1+MARGIN))

            game.update(pygame.mouse.get_pos())


if __name__ == '__main__':
    start = datetime.now()
    main()
    print(datetime.now()-start)
