import pygame as pg
from checkwin import *


white = (255 ,255 ,255)
gray = (180 ,180 ,180)
red = (255 ,0 ,0)
green = (0 ,255 ,0)
black = (0 ,0 ,0)
blue = (0, 0, 255)
hover_color = (200, 200, 200)

# proportions & sizes     # modified
width = 630    #300
height = 630  #300
line_width = 5
board_rows = 7  # 3
board_cols = 7  # 3
square_size = height // board_cols
circle_radius = square_size // 3
circle_width = 10
cross_width = 15




def draw_lines (screen, color = white):
    for i in range (1, board_rows+1):
        pg.draw.line(screen, color, (0, square_size * i), (width, square_size * i), line_width)
        pg.draw.line(screen, color, (square_size * i, 0), (square_size * i, height), line_width)

# drawing figures X O
def draw_figures(screen, board, color = white):
    for row in range (board_rows):
        for col in range (board_cols):
            if board[row][col] == 2:
                pg.draw.circle(screen, color, (int(col * square_size + square_size // 2),int(row * square_size + square_size // 2)), circle_radius, circle_width )
            elif board[row][col] == 1:
                pg.draw.line(screen, color, (col * square_size + square_size // 4, row * square_size + square_size //4), (col * square_size + (3 * square_size) // 4 , row * square_size + (3 * square_size) // 4), cross_width)
                pg.draw.line(screen, color, (col * square_size + (3 * square_size) // 4, row * square_size + square_size //4), (col * square_size + square_size // 4 , row * square_size + (3 * square_size) // 4), cross_width)

# marking the square
def mark_square (board, row, col, player):
    board[row][col] = player
    # EMPTY -= 1

def draw_status (screen, current_player, game_over, winner, color=white):
    pg.draw.rect(screen, black, (0, height+5, width//2, 50))
    font = pg.font.SysFont(None, 48)

    # Create text for current player
    if winner != 0:
        player_text = f"Player {winner} wins!"
    elif game_over:
        player_text = "Game Over"
    else:
        player_text = f"Player {current_player}'s turn"
    player_surface = font.render(player_text, True, color)
    screen.blit(player_surface, (10, height + 20))

