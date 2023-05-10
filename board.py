from tkinter.font import BOLD
from Globals import *
from tkinter import font
from piece import piece,block


class board():
    def __init__(self,Frame,turn_indicator,algorithm,difficulty):
        self.Frame2 = Frame 
        self.turn_indicator = turn_indicator
        self.reset_board()
        self.selected = None
        self.valid_moves = {}
        self.difficulty = difficulty
        self.algorithm = algorithm
        print(self.difficulty.get())
        print(self.algorithm.get())

        
    def reset_obj(self):
        self.__init__(self.Frame2,self.turn_indicator,self.algorithm,self.difficulty)
        print("reset")
        
        
    def reset_board(self):
        self.player_1_count = 12
        self.player_2_count = 12
        self.player_1_king_count=0
        self.player_2_king_count=0
        self.change_turn(PLAYER_1_COLOR)
        self.play=True
        self.board = []
        
        counter = 0
        for row in range(8):
            self.board.append([])
            for column in range(8):
                if counter % 2 == 0:
                    self.board[row].append(block(self.Frame2,row,column,BLOCK_1_COLOR))
                else:
                    self.board[row].append(block(self.Frame2,row,column,BLOCK_2_COLOR))
                    if(row<3):
                        self.board[row][column].set_piece(piece(row,column,PLAYER_1_COLOR,self.piece_clicked))
                    if row > 4:
                        self.board[row][column].set_piece(piece(row,column,PLAYER_2_COLOR,self.piece_clicked))            
                counter +=1  
            counter+=1


    def piece_clicked(self,P):
        if not self.play:
            return
        
        self.remove_valid_moves()
        
        if self.turn!=P.color:
            return

        self.selected = P
        self.valid_moves = self.get_valid_moves(P)
        self.draw_valid_moves()
            
    
    def remove_valid_moves(self):
        for move in self.valid_moves:
            self.board[move[0]][move[1]].remove_piece()
        self.valid_moves={}
            
            
    def draw_valid_moves(self):
        for move in self.valid_moves:
            self.board[move[0]][move[1]].set_piece(piece(move[0],move[1],VALID_COLOR,self.move))
        
        
    def move(self,P):
        row = P.row
        column = P.column
        original_row,original_col=self.selected.get_position()
        
        self.board[original_row][original_col].remove_piece()
        self.selected.row=row
        self.selected.column=column
        
        self.remove_skipped(row,column)
        
        self.remove_valid_moves()
            
        if self.turn == PLAYER_1_COLOR:
            if row == 8-1:
                self.selected.make_king()
                self.player_1_king_count+=1
            self.change_turn(PLAYER_2_COLOR)
            
        else:
            if row == 0:
                self.selected.make_king()
                self.player_2_king_count+=1
            self.change_turn(PLAYER_1_COLOR)

        self.board[row][column].set_piece(self.selected)
        
        winner = self.winner()
        if winner != None:
            self.play=False
            f = font.Font(family='Helvetica', size=8, weight='bold')
            self.turn_indicator.config(text=winner+" wins",font=f,fg="gold",)
            self.turn_indicator.update()
        
    
    def change_turn(self,color):
        self.turn = color
        
        self.turn_indicator.config(bg=color)
        self.turn_indicator.update()
    
    
    def remove_skipped(self,row,column):
        try:
            skipped = self.valid_moves[(row, column)]  
            for piece in skipped:
                
                if self.turn==PLAYER_1_COLOR:
                    self.player_2_count-=1
                    
                    if self.board[piece.row][piece.column].get_piece().is_king():
                        self.player_2_king_count-=1
                        
                else:
                    self.player_1_count-=1
                    
                    if self.board[piece.row][piece.column].get_piece().is_king():
                        self.player_1_king_count-=1
                        
                self.board[piece.row][piece.column].remove_piece()
        except:
            print("Error")
            
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.color == PLAYER_2_COLOR or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == PLAYER_1_COLOR or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, 8), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, 8), 1, piece.color, right))
        return moves
        
        
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left].get_piece()
            if current == None:
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
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves


    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= 8:
                break
            
            current = self.board[r][right].get_piece()
            if current == None:
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
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    
    def winner(self):
        if self.player_1_count <= 0:
            return PLAYER_2_COLOR
        elif self.player_2_count <= 0:
            return PLAYER_1_COLOR
        return None 