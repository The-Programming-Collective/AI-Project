from Globals import *
class piece():
    def __init__(self,row,column,color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False
       
    
    def move(self,row,column):
        self.row=row
        self.column=column
    
    
    def is_king(self):
        return self.king
    
    
    def make_king(self):
        self.king=True
        
    
    def get_position(self):
        return self.row,self.column
    
    
    def set_position(self,row,column):
        self.row=row
        self.column=column
    

    def get_color(self):
        return self.color
    

    def __repr__(self) -> str:
        if self.color==AI_COLOR:
            return "AI"
        elif self.color==PLAYER_COLOR:
            return "PL"