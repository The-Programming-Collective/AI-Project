from tkinter.font import BOLD
from Globals import *
from tkinter import font
from board import board
from MiniMaxAlgo import minimax
import tkinter as tk

class game():
    def __init__(self,Frame,turn_indicator,algorithm,difficulty):
        self.Frame2 = Frame 

        self.board = board().reset_board()
        self.selected = None
        self.difficulty = difficulty
        self.algorithm = algorithm
        
        self.play=True
        self.turn = self.board.turn
        
        print(self.difficulty.get())
        print(self.algorithm.get())
        
        self.turn_indicator = turn_indicator
        self.change_turn_indicator()
        self.draw_board()

        
    def reset_obj(self):
        self.__init__(self.Frame2,self.turn_indicator,self.algorithm,self.difficulty)
        print("reset")
    
    
    def reset(self):
        for item in self.Frame2.winfo_children():
            item.destroy()
    
    
    def draw_board(self):
        self.reset()
        counter = 0
        for i,row in enumerate(self.board.get_board()):
            for j,piece in enumerate(row):
                if counter % 2:
                    square = self.square(BLOCK_2_COLOR,i,j)
                else:
                    square = self.square(BLOCK_1_COLOR,i,j)
                    
                if piece != 0 and piece.get_color() != VALID_COLOR:
                    self.piece(square,piece,self.piece_clicked)
                elif piece !=0 and piece.get_color() == VALID_COLOR:
                    self.piece(square,piece,self.move_piece)
                
                counter += 1
            counter += 1


    def square(self,color,row,column):
        square = tk.Frame(self.Frame2,bg=color,width=50,height=50)
        
        square.rowconfigure(0, weight = 1)
        square.columnconfigure(0, weight = 1)
        square.grid_propagate(0)
        square.grid(row=row,column=column)
        
        return square


    def piece(self,parent,p,function):   
        self.button = tk.Button(parent,background=p.get_color(), command=lambda: function(p),border=0)
        
        if p.is_king():
            f = font.Font(family='Helvetica', size=14, weight='bold')
            self.button.config(text="K",font=f ,fg="gold")
        self.button.grid(sticky="NWSE",padx=10,pady=10)


    def piece_clicked(self,p):
        if not self.play:
            return
        
        self.board.get_valid_moves(p)
        self.draw_board()

        self.selected = p


    def move_piece(self,p):
        self.board.move(p)
        self.draw_board()
        
        winner = self.board.winner()
        if winner==None:
            self.change_turn_indicator()
        else:
            self.play=False
            f = font.Font(family='Helvetica', size=8, weight='bold')
            self.turn_indicator.config(text=winner+" wins",font=f,fg="gold",)
            self.turn_indicator.update()
                      
        
    def change_turn_indicator(self):
        self.turn_indicator.config(bg=self.board.turn,text="")
        self.turn_indicator.update()
    
    # if winner != None:
    # self.play=False
    # f = font.Font(family='Helvetica', size=8, weight='bold')
    # self.turn_indicator.config(text=winner+" wins",font=f,fg="gold",)
    # self.turn_indicator.update()
        
    
    def AI_move_board(self, board):
        self.board = board