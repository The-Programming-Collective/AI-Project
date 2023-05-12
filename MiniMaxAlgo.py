from Globals import *
from copy import deepcopy

counter = 0
def minimax(position, depth, max_player):
    global counter 
    counter +=1
    if depth == 0 or position.winner() != None:
        return position.evaluate_score(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, AI_COLOR):
            evaluation = minimax(move, depth-1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, PLAYER_COLOR):
            evaluation = minimax(move, depth-1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board):
    board.move(piece, move[0], move[1])
    return board


def get_all_moves(board, color):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move in valid_moves:
            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_board()[piece.row][piece.column]
            new_board = simulate_move(temp_piece, move, temp_board)
            moves.append(new_board)
    
    return moves



# def pprint(list):
#     for i in range(8):
#         for j in range(8):
#             if list[i][j]==0:
#                 print("0 ,",end="")
#             elif list[i][j].get_color()==PLAYER_COLOR:
#                 print("P1 ,",end="")
#             elif list[i][j].get_color()==AI_COLOR:
#                 print("A1 ,",end="")
#         print()
#     print("====================================")