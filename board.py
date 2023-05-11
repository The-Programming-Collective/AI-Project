from Globals import *
from piece import piece


class board():
    def __init__(self):
        self.AI_count = 12
        self.player_count = 12
        self.AI_king_count=0
        self.player_king_count=0

        self.reset_board()
        
        #print(self.board[0])
        
        print(self.get_valid_moves(self.board[2][1]))
        
        
    def reset_board(self):
        self.board=[]
        counter = 0
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLUMNS):
                if counter % 2:
                    if(row<3):
                        self.board[row].append(piece(row,column,AI_COLOR))
                    elif(row>4):
                        self.board[row].append(piece(row,column,PLAYER_COLOR))
                    else:
                        self.board[row].append(0)    
                else: 
                    self.board[row].append(0)
                counter += 1
            counter += 1
        
        
    def get_all_pieces(self, color):
        all_pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.get_color() == color:
                    all_pieces.append(piece)
        return all_pieces
        
        
    def evaluate_score(self):
        return self.player_count - self.AI_count + (self.player_king_count * 0.5 - self.AI_king_count*0.5)
    
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.get_color() == PLAYER_COLOR or piece.is_king():
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.get_color == AI_COLOR or piece.is_king():
            moves.update(self._traverse_left(row +1, min(row+3, 8), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, 8), 1, piece.color, right))
        return moves
        
        
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < COLUMNS:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, 8)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.get_color() == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves


    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLUMNS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, 8)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.get_color() == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
        
    def winner(self):
        if self.AI_count <= 0:
            return PLAYER_COLOR
        elif self.player_count <= 0:
            return AI_COLOR
        return None 