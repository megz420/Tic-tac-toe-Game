#MINIMAX functions 
import random
from checkwin import *
from draw import *

maximizer = True
minimizer = False
board_rows = 7
board_cols = 7

def mini_max(board, depth , alpha, beta, is_maximizer, depth_limit, EMPTY):
    if check_win(2, board):
        return 100- depth 
    elif check_win(1, board):
        return -100 + depth
    elif is_full_board(EMPTY) or depth >= depth_limit:
        return 0

    if is_maximizer == maximizer:
        best_score = -1000
        for row in range(board_rows):
            for col in range(board_cols):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = mini_max(board, depth + 1, alpha, beta, minimizer, depth_limit, EMPTY) 
                    board[row][col] = 0
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:  # Beta cutoff
                        break
        return best_score

    else:  # MINIMIZER's move
        worst_score = 1000
        for row in range(board_rows):
            for col in range(board_cols):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = mini_max(board, depth + 1, alpha, beta, maximizer, depth_limit, EMPTY) 
                    board[row][col] = 0
                    worst_score = min(worst_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:  # Alpha cutoff
                        break
        return worst_score


# Choosing the best move
def best_move(player, board, empty, depth_limit):
    best_score = -1000
    move = (-1, -1)
    if empty == 49:
        mark_square(board, random.randint(2, 4), random.randint(2,4), player)
        return True
    for row in range(board_rows):
        for col in range(board_cols):
            useful_move = False
            for row2 in range(row-1, row+2):
                for col2 in range(col-1, col+2):
                    if row2 < 0 or col2 < 0 or row2 >= board_rows or col2 >= board_cols:
                        continue
                    if board[row2][col2] != 0:
                        useful_move = True
                        break
                if useful_move:
                    break
            if board[row][col] == 0 and useful_move:
                board[row][col] = 2
                score = mini_max(board, 0, -float("inf"), float("inf"), minimizer, depth_limit, empty)
                board[row][col] = 0
                print(score)
                if best_score < score:
                    best_score = score
                    move = (row, col)
    if best_score == -1000:
        for row in range(board_rows):
            for col in range(board_cols):
                if board[row][col] == 0:
                    board[row][col] = 2
                    return True
    if move != (-1, -1):
        print (move)
        mark_square(board, move[0], move[1], player)
        return True
    print(move)
    return False
