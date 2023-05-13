from tkinter.font import BOLD
from Globals import *
from tkinter import font
from board import board
import tkinter as tk

class game():
    def __init__(self,Frame,turn_indicator,algorithm,difficulty):
        self.turn = False
        self.run = True
        self.Frame2 = Frame 
        self.algorithm = algorithm
        self.difficulty = difficulty
        self.board = board()
        self.previous_board = None
        self.turn_indicator = turn_indicator
        self.change_turn_indicator(PLAYER_COLOR)
        self.draw_board()
        self.moves_counter = 0
        self.death_counter = 0
        self.previous_ai_pieces_counter = 12
        self.previous_player_pieces_counter = 12


    def get_previous_board(self):
        if self.previous_board and self.moves_counter > 0:
            self.moves_counter -= 1
            self.board = self.previous_board
            self.previous_board = None
            self.change_turn()
            self.draw_board()
        
        
    def play(self):
        if not self.run:
            return
        
        new_board=self.board.ai_move(int(self.difficulty.get()),self.algorithm.get(),self.turn)
        if(not new_board or new_board==self.board):
            self.draw_winner(self.board.evaluate_winner())
            return
        
        self.previous_ai_pieces_counter = self.board.AI_count
        self.previous_player_pieces_counter = self.board.player_count
        self.previous_ai_kings_counter = self.board.AI_king_count
        self.previous_player_kings_counter = self.board.player_king_count
        
        self.previous_board = self.board
        self.board = new_board
        self.draw_board()
        
        self.change_turn()
            
        self.moves_counter += 1
        if self.moves_counter >= 70:
            if (self.previous_ai_pieces_counter==self.board.AI_count and
            self.previous_player_pieces_counter==self.board.player_count and 
            self.previous_ai_kings_counter==self.board.AI_king_count and
            self.previous_player_kings_counter==self.board.player_king_count):
                self.death_counter += 1
            else:
                self.death_counter = 0
        else:
            self.death_counter = 0
        
        if self.death_counter >= 20:
            self.draw_winner(self.board.evaluate_winner())
        

    def reset_obj(self):
        self.__init__(self.Frame2,self.turn_indicator,self.algorithm,self.difficulty)
        print("reset")
    
    
    def reset_frame(self):
        for item in self.Frame2.winfo_children():
            item.destroy()

    
    def draw_board(self):
        self.reset_frame()
        counter = 0
        for i,row in enumerate(self.board.get_board()):
            for j,piece in enumerate(row):
                if counter % 2:
                    square = self.square(BLOCK_2_COLOR,i,j)
                else:
                    square = self.square(BLOCK_1_COLOR,i,j)
                    
                if piece != 0 and piece.get_color() != VALID_COLOR:
                    self.piece(square,piece)
                elif piece !=0 and piece.get_color() == VALID_COLOR:
                    self.piece(square,piece)
                
                counter += 1
            counter += 1


    def square(self,color,row,column):
        square = tk.Frame(self.Frame2,bg=color,width=50,height=50)
        
        square.rowconfigure(0, weight = 1)
        square.columnconfigure(0, weight = 1)
        square.grid_propagate(0)
        square.grid(row=row,column=column)
        
        return square


    def piece(self,parent,p):   
        self.button = tk.Label(parent,background=p.get_color(),border=0)
        
        if p.is_king():
            f = font.Font(family='Helvetica', size=14, weight='bold')
            self.button.config(text="K",font=f ,fg="gold")
        self.button.grid(sticky="NWSE",padx=10,pady=10)
       
                  
    def change_turn(self):
        self.turn = not self.turn
        if self.turn:
            self.change_turn_indicator(AI_COLOR)
        else:
            self.change_turn_indicator(PLAYER_COLOR)    
        
        
    def change_turn_indicator(self,color):
        winner_color = self.board.winner()
        
        if winner_color!=None:
            self.draw_winner(winner_color)
            return 
            
        self.turn_indicator.config(bg=color,text="Next ->",fg="white")
        self.turn_indicator.update()
    
    
    def draw_winner(self,winner_color):
        self.run=False
        f = font.Font(family='Helvetica', size=8, weight='bold')
        self.turn_indicator.config(text= winner_color +" wins",font=f,fg="gold",bg=winner_color)
        self.turn_indicator.update()