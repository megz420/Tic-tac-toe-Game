board_rows = 7
board_cols = 7

def check_win(player, board):
    # Check vertical win
    for col in range(board_cols):
        for row in range(0, board_rows - 3):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check horizontal win
    for row in range(board_rows):
        for col in range(0, board_cols - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check diagonal win (top-left to bottom-right)
    for i in range(3, -1, -1):
        for j in range(i, board_rows - 3):
            if ((board[j - i][j] == player and board[j - i + 1][j + 1] == player and board[j - i + 2][j + 2] == player and board[j - i + 3][j + 3] == player) or
                (board[j][j - i] == player and board[j + 1][j - i + 1] == player and board[j + 2][j - i + 2] == player and board[j + 3][j - i + 3] == player)):
                return True

    # Check diagonal win (bottom-left to top-right)
    shift = 0
    for i in range(3, board_rows):
        m = i 
        for j in range(i, board_rows - 5, -1):
            if ((board[i - j][j] == player and board[i - j + 1][j - 1] == player and board[i - j + 2][j - 2] == player and board[i - j + 3][j - 3] == player) or
                (board[i + j - shift][m - shift] == player and board[i + j - shift - 1][m - shift + 1] == player and board[i + j - shift - 2][m - shift + 2] == player and board[i + j - shift - 3][m - shift + 3] == player)):
                return True
            m += 1
        shift += 2

    return False

def is_full_board(EMPTY):
    # Check if the board is full (no empty spaces left)
    return EMPTY == 0
