from copy import deepcopy
from Globals import *
from piece import piece
from algorithms import *


class board():
    def __init__(self):
        self.AI_count = 12
        self.player_count = 12
        self.AI_king_count=0
        self.player_king_count=0
        self.reset_board()
        self.alpha = float('-inf')
        self.beta = float('inf')
        
    def reset_board(self):
        """ Function to reset board to starting state

        Returns:
            board: Reset board 
        """
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
        return self
    
    def get_board(self):
        """ Board getter

        Returns:
            board object
        """
        return self.board
        

    def get_all_pieces(self, color):
        """ Function to return all pieces

        Args:
            color (String): Either black or red

        Returns:
            Array: Array that contains all pieces
        """
        all_pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.get_color() == color:
                    all_pieces.append(piece)
                    
        return all_pieces
   
    
    def evaluate_score(self):
        """ Evaluation function to evaluate each move

        Returns:
            double: evaluation
        """
        score=0
        if self.winner() == PLAYER_COLOR :
            score+=1000
        elif self.winner() == AI_COLOR :
            score-=1000        
        score+=self.AI_count - self.player_count 
        score+=self.AI_king_count * 0.5 - self.player_king_count * 0.5
        return score


    def get_valid_moves(self, piece):
        """ Gets all valid moves for a piece

        Args:
            piece (piece)

        Returns:
            dict: set of all valid moves
        """
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
            
        # try:
        #     del moves[(piece.previous_position[0],piece.previous_position[1])]
        # except:
        #     pass
            
        return moves
        
        
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """ Traverses piece left diagonally

        Args:
            start (int): description
            stop (int): description
            step (int): description
            color (String): description
            left (int): description
            skipped (list, optional): The pieces skipped over when making this move. Defaults to [].

        Returns:
            (_dict_): Set of moves
        """
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
        """ Traverses piece right diagonally

        Args:
            start (int): description
            stop (int): description
            step (int): description
            color (String): description
            right (int): description
            skipped (list, optional): The pieces skipped over when making this move. Defaults to [].

        Returns:
            (_dict_): Set of moves
        """
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
    
    
    def remove_skipped(self,skipped):
        """ Removes skipped pieces from board

        Args:
            skipped (array): Skipped pieces
        """
        try: 
            for piece in skipped:
                piece_row,piece_column=piece.get_position()
                if piece.get_color()==PLAYER_COLOR:
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


    def move(self,piece,new_position,skipped):
        """ Moves piece to a position on the board

        Args:
            piece (piece)
            new_position (array): Array that contains row and column
            skipped (array)
        """
        original_row,original_col=piece.get_position()
        piece.previous_position=[original_row,original_col]
        row = new_position[0]
        column = new_position[1]
        self.board[original_row][original_col]=0
        
        self.remove_skipped(skipped)
        
        if piece.get_color() == AI_COLOR:
            if row == ROWS-1 and not piece.is_king():
                piece.make_king()
                self.AI_king_count+=1
            piece.set_position(row,column)
            self.board[row][column]=piece
            
        else:
            if row == 0 and not piece.is_king():
                piece.make_king()
                self.player_king_count+=1
            piece.set_position(row,column)
            self.board[row][column]=piece

    
    def ai_move(self,difficulty,algorithm,player):
        """ Function that decides which move the agent will make based on diffuiculty and algorithm selected

        Args:
            difficulty (integer): Depth of search for moves
            algorithm (String): MiniMax or MiniMax with AlphaBeta
            player (boolean): Which color turn is it to move
        Returns:
            _type_: _description_
        """
        if algorithm == "MiniMax":
            temp = minimax(self,difficulty, player)
            return temp[1]
        else:
            temp = alphabeta(self, difficulty, not player)
            return temp[1]
    
    def winner(self):
        """ Default function to check for winner if one side takes all the other sides' pieces.

        Returns:
            string: Winner's color
        """
        if self.AI_count <= 0:
            return PLAYER_COLOR
        elif self.player_count <= 0:
            return AI_COLOR
        return None
    
    def evaluate_winner(self):
        """ Gets winner when there are no legal moves by counting the pieces on the board. 

        Returns:
            string: Winner's color
        """
        if self.AI_count > self.player_count:
            return AI_COLOR
        return PLAYER_COLOR