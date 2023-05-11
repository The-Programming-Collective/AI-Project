import tkinter as tk
from board import*
from Globals import *
from piece import piece
import copy

def minimax(board , depth , AI_Turn):
    if depth==0 or board.winner() != None:
        return board.evaluate_score() , board
    
    if AI_Turn:
        minEval = float('inf')
        min_move = None
        move_list = get_all_moves(board,AI_COLOR)
        for move in move_list:
            evaluation = minimax(move,depth-1)
            minEval = min(minEval, evaluation, False)[0]
            if minEval==evaluation:
                min_move=move
        return minEval ,min_move
    else:
        maxEval = float('-inf')
        max_move = None
        for move in get_all_moves(board,PLAYER_COLOR):
            evaluation = minimax(move,depth-1)
            maxEval = max(maxEval, evaluation, True)[0]
            if maxEval==evaluation:
                max_move=move
        return maxEval ,max_move


def get_all_moves(board , color):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move in valid_moves.items():
            temp_board = copy.deepcopy(board)
            temp_piece = temp_board[move[0]][move[1]]
            new_board = simulate_move(temp_piece , temp_board)
            moves.append([new_board, piece])
    return moves


def simulate_move(piece,board ):
    board.move(piece)
    return board