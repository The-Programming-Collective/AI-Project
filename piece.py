import tkinter as tk
from tkinter import font

class block():
    def __init__(self,parent,row,column,color):
        self.piece = None
        self.color = color
        self.square = tk.Frame(parent,bg=color,width=50,height=50)
        
        self.square.rowconfigure(0, weight = 1)
        self.square.columnconfigure(0, weight = 1)
        self.square.grid_propagate(0)
        self.square.grid(row=row,column=column)
        
    def get_piece(self):
        return self.piece
    
    def set_piece(self,piece):
        self.piece = piece
        self.piece.set_parent(self.square)
        piece.show()
    
    def remove_piece(self):
        try:
            self.piece.hide()
            self.piece = None
        except:
            raise("lol")


class piece():
    def __init__(self,row,column,color,piece_clicked):
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        self.piece_clicked = piece_clicked
        self.parent = None
        self.show()
        
    def show(self):
        if self.color == None or self.parent == None:
            return
        
        self.button = tk.Button(self.parent,background=self.color, command=lambda: self.piece_clicked(self),border=0)
        
        if self.king:
            f = font.Font(family='Helvetica', size=14, weight='bold')
            self.button.config(text="K",font=f ,fg="gold")

        self.button.grid(sticky="NWSE",padx=10,pady=10)
       
    def hide(self):
        self.button.grid_forget()
        
    def move(self,parent,row,column):
        self.parent=parent
        self.row=row
        self.column=column
    
    def is_king(self):
        return self.king
    
    def make_king(self):
        self.king=True
        
    def get_position(self):
        return self.row,self.column
    
    def get_color(self):
        return self.color
    
    def set_parent(self,parent):
        self.parent = parent