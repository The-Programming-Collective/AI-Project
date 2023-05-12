import sys
import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the board parameters
SQUARE_SIZE = 100
ROWS = 8
COLS = 8
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the positions of the squares
board = []
for row in range(ROWS):
    board_row = []
    for col in range(COLS):
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        color = BLACK if (row + col) % 2 == 0 else WHITE
        square = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, color, square)
        board_row.append(square)
    board.append(board_row)


# Update the display
pygame.display.update()


class CheckerPiece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.is_king = False
        draw()
    
    def make_king(self):
        self.is_king = True
    
    def move(self, row, col):
        self.row = row
        self.col = col
        
    def draw(self, surface):
        piece_radius = SQUARE_SIZE // 2
        piece_center_x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        piece_center_y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

        pygame.draw.circle(surface, self.color, (piece_center_x, piece_center_y), piece_radius)

        if self.is_king:
            crown_img = pygame.image.load("crown.png")
            crown_size = (piece_radius * 2, piece_radius)
            crown_img = pygame.transform.scale(crown_img, crown_size)
            crown_rect = crown_img.get_rect(center=(piece_center_x, piece_center_y - piece_radius // 2))
            surface.blit(crown_img, crown_rect)
    
    def get_valid_moves(self, board):
        valid_moves = []
        directions = [-1, 1]
        if self.is_king:
            for i in directions:
                for j in directions:
                    if self.row+i < 0 or self.row+i >= len(board) or self.col+j < 0 or self.col+j >= len(board[0]):
                        continue
                    if board[self.row+i][self.col+j] is None:
                        valid_moves.append((self.row+i, self.col+j))
                    elif board[self.row+i][self.col+j].color != self.color:
                        if self.row+i*2 < 0 or self.row+i*2 >= len(board) or self.col+j*2 < 0 or self.col+j*2 >= len(board[0]):
                            continue
                        if board[self.row+i*2][self.col+j*2] is None:
                            valid_moves.append((self.row+i*2, self.col+j*2))
        else:
            direction = 1 if self.color == 'black' else -1
            for i in directions:
                for j in directions:
                    if i == direction or j == direction:
                        continue
                    if self.row+i*direction < 0 or self.row+i*direction >= len(board) or self.col+j < 0 or self.col+j >= len(board[0]):
                        continue
                    if board[self.row+i*direction][self.col+j] is None:
                        valid_moves.append((self.row+i*direction, self.col+j))
                    elif board[self.row+i*direction][self.col+j].color != self.color:
                        if self.row+i*2*direction < 0 or self.row+i*2*direction >= len(board) or self.col+j*2 < 0 or self.col+j*2 >= len(board[0]):
                            continue
                        if board[self.row+i*2*direction][self.col+j*2] is None:
                            valid_moves.append((self.row+i*2*direction, self.col+j*2))
        return valid_moves


# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
