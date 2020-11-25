import pygame
from quoridor.constants import *
from quoridor.game import Game

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Quoridor')
game = Game(WIN)


def main():
    run = True
    while run:

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[0] // TILE_WIDTH
                col = (pos[1] - MARGIN) // TILE_HEIGHT
                game.select((row, col))
        game.update()


main()
