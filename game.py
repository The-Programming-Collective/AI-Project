from tkinter.font import BOLD
from Globals import *
from tkinter import font
from piece import piece,block
from MiniMaxAlgo import minimax


class game():
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
        self.change_turn(PLAYER_COLOR)
        self.play=True

        
        counter = 0
        for row in range(8):
            self.board.append([])
            for column in range(8):
                if counter % 2 == 0:
                    self.board[row].append(block(self.Frame2,row,column,BLOCK_1_COLOR))
                else:
                    self.board[row].append(block(self.Frame2,row,column,BLOCK_2_COLOR))
                    if(row<3):
                        self.board[row][column].set_piece(piece(row,column,AI_COLOR,self.test))
                    if row > 4:
                        self.board[row][column].set_piece(piece(row,column,PLAYER_COLOR,self.piece_clicked))            
                counter +=1  
            counter+=1

    def test(self,p):
        pass

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
            
        if self.turn == AI_COLOR:
            print("lmao")
            new_board = minimax(self, self.difficulty, AI_COLOR)[1]
            self.AI_move_board(new_board)
            if row == 8-1:
                self.selected.make_king()
                self.player_king_count+=1
            self.change_turn(PLAYER_COLOR)
            
        else:
            if row == 0:
                self.selected.make_king()
                self.AI_king_count+=1
            self.board[row][column].set_piece(self.selected)
            self.change_turn(AI_COLOR)

        
        winner = self.winner()
        if winner != None:
            self.play=False
            f = font.Font(family='Helvetica', size=8, weight='bold')
            self.turn_indicator.config(text=winner+" wins",font=f,fg="gold",)
            self.turn_indicator.update()
        
    
    def change_turn(self,color):
        self.turn = color
        
        if(color == AI_COLOR):
            new_board = minimax(self, self.difficulty, AI_COLOR)[1]
            self.AI_move_board(new_board)
            if row == 8-1:
                self.selected.make_king()
                self.player_king_count+=1
            self.change_turn(PLAYER_COLOR)
        
        self.turn_indicator.config(bg=color)
        self.turn_indicator.update()
    
    
    def remove_skipped(self,row,column):
        try:
            skipped = self.valid_moves[(row, column)]  
            for piece in skipped:
                
                if self.turn==AI_COLOR:
                    self.player_count-=1
                    
                    if self.board[piece.row][piece.column].get_piece().is_king():
                        self.player_king_count-=1
                        
                else:
                    self.AI_count-=1
                    
                    if self.board[piece.row][piece.column].get_piece().is_king():
                        self.AI_king_count-=1
                        
                self.board[piece.row][piece.column].remove_piece()
        except:
            print("Error")
            
    
   
    
    
    def AI_move_board(self, board):
        self.board = board
        

    def board_to_list(self):
        board_list=[]
        
        for row in self.board:
            board_list.append([])
            for i,block in enumerate(row):
                if block.get_piece()==None:
                    board_list[i].append(0)
                else:
                    board_list[i].append(['N',block.get_piece().get_color()])
    
