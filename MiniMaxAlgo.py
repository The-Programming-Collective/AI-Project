from copy import deepcopy
import tkinter as tk
from board import*
from Globals import *


AI_color = AI_COLOR
Player_color = PLAYER_COLOR


def minimax(board , depth , AI_Turn):
    if depth==0 or board.winner(board) != None:
        return board.evaluate_score , board
    if AI_Turn:
        minEval = float('+inf')
        min_move = None
        for move in get_all_moves(board,AI_COLOR):
            evaluation = minimax(move,depth-1)
            minEval = min(minEval, evaluation, False)[0]
            if minEval==evaluation:
                min_move=move
        return minEval ,min_move
    else:
        maxEval = float('-inf')
        max_move = None
        for move in get_all_moves(board,Player_color):
            evaluation = minimax(move,depth-1)
            maxEval = max(maxEval, evaluation, True)[0]
            if maxEval==evaluation:
                max_move=move
        return maxEval ,max_move



def get_all_moves(board , color):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece)
            new_board = simulate_move(temp_piece , temp_board)
            moves.append([new_board, piece])
    return moves

def simulate_move(piece,board ):
    board.move(piece)
    return board