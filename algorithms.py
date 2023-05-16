from Globals import *
from copy import deepcopy
import random


def minimax(position, depth, max_player):
    if depth == 0 or position.winner() != None:
        return position.evaluate_score(), position
    
    if max_player:
        maxEval = float('-inf')
        best_board = None
        
        all_boards = get_all_boards(position, AI_COLOR)
        
        #TODO this case 
        if not all_boards:
            return  float('-inf'),position
        
        for board in all_boards:
            evaluation = minimax(board, depth-1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_board = board
        
        return maxEval, best_board
    else:
        minEval = float('inf')
        best_board = None
        
        all_boards = get_all_boards(position, PLAYER_COLOR)
        
        #TODO this case 
        if not all_boards:
            return  float('inf'),position
        
        for board in all_boards:
            evaluation = minimax(board, depth-1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_board = board
        
        return minEval, best_board
    
def alphabeta(position, depth, max_player):
    if depth == 0 or position.winner() != None:
        return position.evaluate_score(), position
    if max_player:
        maxVal = float('-inf')
        all_boards = get_all_boards(position, PLAYER_COLOR)
        
        if not all_boards:
            return  float('-inf'),position
        
        index = random.randint(0,len(all_boards)-1)
        best_move = all_boards[index]
        
        for move in all_boards[1:]:
            value = alphabeta(position, depth-1, False)[0]
            maxVal = max(value, maxVal)
            position.alpha = max(position.alpha, maxVal)
            if position.beta <= position.alpha:
                #print("Prune")
                best_move = move
                break
        return maxVal, best_move
    else:
        minVal = float('inf')
        all_boards = get_all_boards(position, AI_COLOR)
        
        if not all_boards:
            return  float('inf'),position
        
        index = random.randint(0,len(all_boards)-1)
        best_move = all_boards[index]
        
        for move in all_boards[1:]:
            value = alphabeta(position, depth-1, True)[0]
            minVal = min(value, minVal)
            position.beta = min( position.beta, minVal)
            if position.beta <=  position.alpha:
                # print("Prune")
                best_move = move
                break
        return minVal, best_move

def simulate_move(piece, move, board,skipped):
    board.move(piece, move,skipped)
    return board


def get_all_boards(board, color):
    boards = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move,skipped in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_board()[piece.row][piece.column]
            new_board = simulate_move(temp_piece, move, temp_board,skipped)
            boards.append(new_board)
    
    return boards