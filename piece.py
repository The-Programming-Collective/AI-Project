# class block():
#     def __init__(self,parent,row,column,color):
#         self.piece = None
#         self.color = color
#         self.square = tk.Frame(parent,bg=color,width=50,height=50)
        
#         self.square.rowconfigure(0, weight = 1)
#         self.square.columnconfigure(0, weight = 1)
#         self.square.grid_propagate(0)
#         self.square.grid(row=row,column=column)
        
#     def get_piece(self):
#         return self.piece
    
#     def set_piece(self,piece):
#         self.piece = piece
#         self.piece.set_parent(self.square)
#         piece.show()
    
#     def remove_piece(self):
#         try:
#             self.piece.hide()
#             self.piece = None
#         except:
#             raise("lol")

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