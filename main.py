import pygame
from random import randint as rint
from quoridor.constants import *
from quoridor.game import Game

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Quoridor')
game = Game(WIN)


def main():
    run = True
    while run:

        if game.winner() is not None:
            print(game.winner())
            run = False

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
                if event.key == pygame.K_BACKSPACE:
                    game.flip()

        game.update(pygame.mouse.get_pos())


main()
