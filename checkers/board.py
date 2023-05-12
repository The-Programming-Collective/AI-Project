import pygame
from .globals import *
from .Piece import Piece

class Board:
    # constructor && variable definitions
    def __init__(self):
        self.board = []
        self.chosenPiece = None
        self.whitePiecesCount = 12
        self.redPiecesCount = 12
        self.whiteKings = 0
        self.redKings = 0
        self.init_board()


    def draw_squares(self, window):
        
        # fill the whole window black
        window.fill(CHESS_GREEN)
        for row in range(ROWS):
            # then draw the red squares in their respective places.
            # itll be a red/black chess board style
            for col in range(row % 2, ROWS, 2):   
                pygame.draw.rect(window, CHESS_BEIGE,(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



    # initializes the board list with correct pieces position
    def init_board(self):
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLUMNS):
                if column % 2 == ((row + 1) % 2):
                    # if in first 3 rows, place white pieces
                    if row < 3:
                        self.board[row].append(Piece(row, column, WHITE))

                    # if in first 3 rows, place red pieces
                    elif row > 4:
                        self.board[row].append(Piece(row, column, CHESS_GREY))
                    
                    # mark non-piece square as empty (0)
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)


    # draws the whole board
    def draw_board(self, window):
        # first draw squares
        self.draw_squares(window)

        # draw pieces on the squares marked as pieces from the init_board function
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.drawPiece(window)


