from Globals import *
from piece import piece
from MiniMaxAlgo import minimax

class board():
    def __init__(self):
        self.AI_count = 12
        self.player_count = 12
        self.AI_king_count=0
        self.player_king_count=0
        self.valid_moves={}
        self.turn=None
        self.reset_board()
        
        
    def reset_board(self):
        self.board=[]
        self.change_turn(PLAYER_COLOR)
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
        return self
    
    def get_board(self):
        return self.board
        
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
        self.remove_valid_moves()
        
        if self.turn!=piece.get_color():
            return
        
        self.selected = piece
        moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.get_color() == PLAYER_COLOR or piece.is_king():
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.get_color() == AI_COLOR or piece.is_king():
            moves.update(self._traverse_left(row +1, min(row+3, 8), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, 8), 1, piece.color, right))
        
        self.valid_moves = moves
        self.apply_valid_moves()
        
    
    def remove_valid_moves(self):
        for move in self.valid_moves:
            self.board[move[0]][move[1]]=0
        self.valid_moves={}
        
    def apply_valid_moves(self):
        for move in self.valid_moves:
            self.board[move[0]][move[1]]=piece(move[0],move[1],VALID_COLOR)
        
        
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
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
    
    
    def remove_skipped(self,row,column):
        try:
            skipped = self.valid_moves[(row, column)]  
            for piece in skipped:
                piece_row,piece_column=piece.get_position()
                if self.turn==AI_COLOR:
                    self.player_count-=1
                    
                    if self.board[piece_row][piece_column].is_king():
                        self.player_king_count-=1
                        
                else:
                    self.AI_count-=1
                    
                    if self.board[piece_row][piece_column].is_king():
                        self.AI_king_count-=1
                        
                self.board[piece_row][piece_column]=0
        except:
            print("Error")
        
        
    # def move(self,P):
    #     row = P.row
    #     column = P.column
    #     original_row,original_col=self.selected.get_position()
        
    #     self.board[original_row][original_col]=0
    #     self.selected.set_position(row,column)
        
    #     self.remove_skipped(row,column)
        
    #     self.remove_valid_moves()
            
    #     if self.turn == AI_COLOR:
    #         print("lmao")
    #         new_board = minimax(self, self.difficulty, AI_COLOR)[1]
    #         self.AI_move_board(new_board)
    #         if row == 8-1:
    #             self.selected.make_king()
    #             self.player_king_count+=1
    #         self.change_turn(PLAYER_COLOR)
            
    #     else:
    #         if row == 0:
    #             self.selected.make_king()
    #             self.AI_king_count+=1
    #         self.board[row][column]=self.selected
    #         self.change_turn(AI_COLOR)

        
    #     self.winner = self.winner()
    
    def move(self,P):
        row = P.row
        column = P.column
        original_row,original_col=self.selected.get_position()
        
        self.board[original_row][original_col]=0
        self.selected.row=row
        self.selected.column=column
        
        self.remove_skipped(row,column)
        
        self.remove_valid_moves()
            
        if self.turn == AI_COLOR:
            if row == ROWS-1:
                self.selected.make_king()
                self.AI_king_count+=1
            self.change_turn(PLAYER_COLOR)
            
        else:
            if row == 0:
                self.selected.make_king()
                self.player_king_count+=1
            self.change_turn(AI_COLOR)
        self.board[row][column]=self.selected
        
        winner = self.winner()

        
    def change_turn(self,color):
        self.turn = color
        
        # if color == AI_COLOR:
        #     new_board = minimax(self, self.difficulty, AI_COLOR)[1]
        #     self.AI_move_board(new_board)
        #     self.change_turn(PLAYER_COLOR)
        
        
    def winner(self):
        if self.AI_count <= 0:
            return PLAYER_COLOR
        elif self.player_count <= 0:
            return AI_COLOR
        return None 