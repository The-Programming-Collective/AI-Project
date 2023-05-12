import pygame
from .globals import RED, BLACK, SQUARE_SIZE, GREY, CHESS_GREY

class Piece:

   PADDING = 15
   OUTLINE = 1

   def __init__(self, row, col, color):
      self.row = row
      self.col = col
      self.color = color
      self.king = False
      
      if self.color == RED:
         self.direction  = -1 # move up 
      else:
         self.direction = 1 # move down 
      self.x = 0
      self.y = 0
      self.calculate_position()

   
   def calculate_position(self):
      # equation that puts piece right in the middle of its square.
      self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
      self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
   
   def becomeKing(self):
      self.king = True
   
   def drawPiece(self, window):
      pieceRadius = SQUARE_SIZE // 2 - self.PADDING
      pygame.draw.circle(window, CHESS_GREY, (self.x, self.y), pieceRadius + self.OUTLINE)
      pygame.draw.circle(window, self.color, (self.x, self.y), pieceRadius)

   
   def __repr__(self) -> str:
      return str(self.color)