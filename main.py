import pygame
from checkers.globals import *
from checkers.board import Board

# Pygame Window Constants
FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("checkers game")

def main():
    run = True
    
    # init fps meassurer
    clock = pygame.time.Clock()

    #init board
    board = Board()
    

    while(run):
        clock.tick(FPS)
        pass

        for event in pygame.event.get():
            
            # if the event was quitting, break the loop
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        
        board.draw_board(WINDOW)
        pygame.display.update()

    pygame.quit()



main()