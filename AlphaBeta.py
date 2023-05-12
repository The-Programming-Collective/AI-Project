from Globals import *
from copy import deepcopy



# TODO fix alphabeta not moving pieces
# Check if returns board
def alphabeta(position, depth, max_player, alpha, beta):
    if depth == 0 or position.winner() != None:
        return position.evaluate_score(), position
    val_counter = 0
    if max_player:
        maxVal = float('-inf')
        best_move = None
        for move in get_all_moves(position, PLAYER_COLOR):
            value = alphabeta(position, depth-1, False, alpha, beta)[0]
            maxVal = max(value, maxVal)
            # print("value: ", value)
            # print("maxVal: ", maxVal)
            # print("alpha: ", alpha)
            alpha = max(alpha, maxVal)
            if maxVal == value:
                best_move = move
            if beta <= alpha:
                print("Prune")
                break
        return maxVal, best_move
    else:
        minVal = float('inf')
        best_move = None
        for move in get_all_moves(position, AI_COLOR):
            value = alphabeta(position, depth-1, True, alpha, beta)[0]
            minVal = min(value, minVal)
            # print("value: ", value)
            # print("minVal: ", minVal)
            # print("beta: ", beta)
            beta = min(beta, minVal)
            if minVal == value:
                best_move = move
            if beta <= alpha:
                print("Get Pruned")
                break
        return minVal, best_move


def simulate_move(piece, move, board,skipped):
    board.move(piece, move,skipped)
    return board


def get_all_moves(board, color):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move,skipped in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_board()[piece.row][piece.column]
            new_board = simulate_move(temp_piece, move, temp_board,skipped)
            moves.append(new_board)
    
    return moves