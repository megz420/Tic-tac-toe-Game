import sys
import numpy as np
import pygame as pg
import random
from minimax import best_move
from button import Button
from checkwin import *
from draw import *


pg.init()

# colors
WHITE = (255 ,255 ,255)
GRAY = (180 ,180 ,180)
RED = (255 ,0 ,0)
GREEN = (0 ,255 ,0)
BLACK = (0 ,0 ,0)
BLUE = (0, 0, 255)
HOVER_COLOR = (200, 200, 200)

# proportions & sizes     # modified
WIDTH = 630    #300
HEIGHT = 630  #300
LINE_WIDTH = 5
BOARD_ROWS = 7  # 3
BOARD_COLS = 7  # 3
SQUARE_SIZE = HEIGHT // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15

# # AI portion definition
# MAXIMIZER = True
# MINIMIZER = False

# Empty spaces tracker
EMPTY = 49

depth_limit = 2
depth_limit_1 = 2
depth_limit_2 = 2


# screen
screen = pg.display.set_mode ((WIDTH,HEIGHT+70))
pg.display.set_caption('Tic Tac Toe Game')


# defining board array
board = np.zeros((BOARD_ROWS,BOARD_COLS))


# checking if available square
def is_available (row, col):
    return board[row][col] == 0




# function for restarting the game 
def restart_game(screen):
    global EMPTY
    EMPTY = 49
    screen.fill(BLACK)
    draw_lines(screen)
    for row in range (BOARD_ROWS):
        for col in range (BOARD_COLS):
            board[row][col] = 0

# start positions as initialization
player = 1
game_over = False


# Define fonts
font = pg.font.SysFont(None, 48)


# Create buttons
buttonPvP = Button(130, 80, 400, 80, "Player vs. Player", (51,101,0), HOVER_COLOR)
buttonPvC = Button(130, 180, 400, 80, "Player vs. Computer", (153,153,0), HOVER_COLOR)
buttonCvC = Button(130, 280, 400, 80, "Computer vs. Computer", (153,0,0), HOVER_COLOR)
buttonEasy = Button(130, 180, 400, 80, "Easy", (220,43,5), HOVER_COLOR)
buttonMedium = Button(130, 280, 400, 80, "medium", (33,44,56), HOVER_COLOR)
buttonHard = Button(130, 380, 400, 80, "Hard", (87,200,38), HOVER_COLOR)
buttonRestart = Button(350, 640, 300, 50, "Restart" , BLACK, HOVER_COLOR)
#buttonStr = Button(10, 640, 200, 50, "score= "+ str(depth_limit) , BLACK, HOVER_COLOR)

mode_selected = False
mode = 0

# Main loop for mode selection
while not mode_selected:
    screen.fill(BLACK)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if buttonPvP.is_clicked(event, pg.MOUSEBUTTONDOWN):
            print("Player vs. Player mode selected!")
            mode = 1
            mode_selected = True
        if buttonPvC.is_clicked(event, pg.MOUSEBUTTONDOWN):
            print("Player vs. Computer mode selected!")
            mode = 2
            mode_selected = True
        if buttonCvC.is_clicked(event, pg.MOUSEBUTTONDOWN):
            print("Computer vs. Computer mode selected!")
            mode = 3
            mode_selected = True

    # Draw the buttons
    buttonPvP.draw(screen)
    buttonPvC.draw(screen)
    buttonCvC.draw(screen)

    pg.display.flip()

# Difficulty selection loop
if mode in (2, 3):
    difficulty_selected = False
    title_text = "Computer Level"
    title_surface = font.render(title_text, True, WHITE)
    screen.fill(BLACK)
    screen.blit(title_surface, (WIDTH // 3.2, 80))
    while not difficulty_selected:
        buttonEasy.draw(screen)
        buttonMedium.draw(screen)
        buttonHard.draw(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if buttonEasy.is_clicked(event, pg.MOUSEBUTTONDOWN):
                depth_limit = 2
                difficulty_selected = True
            if buttonMedium.is_clicked(event, pg.MOUSEBUTTONDOWN):
                depth_limit = 3
                difficulty_selected = True
            if buttonHard.is_clicked(event, pg.MOUSEBUTTONDOWN):
                depth_limit = 4
                difficulty_selected = True

        pg.display.flip()

if mode == 3:
    difficulty_selected = False
    title_text = "Computer 2 Level"
    title_surface = font.render(title_text, True, WHITE)
    screen.fill(BLACK)
    screen.blit(title_surface, (WIDTH // 3.5, 20))
    while not difficulty_selected:
        buttonEasy.draw(screen)
        buttonMedium.draw(screen)
        buttonHard.draw(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if buttonEasy.is_clicked(event, pg.MOUSEBUTTONDOWN):
                depth_limit_2 = 1
                difficulty_selected = True
            if buttonMedium.is_clicked(event, pg.MOUSEBUTTONDOWN):
                depth_limit_2 = 2
                difficulty_selected = True
            if buttonHard.is_clicked(event, pg.MOUSEBUTTONDOWN):
                depth_limit_2 = 2
                difficulty_selected = True
        depth_limit_1 = depth_limit
        pg.display.flip()



# infinite loop (main of the game)
if mode_selected == 1:
    while True:
        screen.fill(BLACK)
        draw_lines(screen)
        buttonRestart.draw(screen)
        #buttonStr.draw(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if buttonRestart.is_clicked(event, pg.MOUSEBUTTONDOWN):
                restart_game(screen)
                game_over = False
                player = 1
                pg.display.flip()

            while True:
                if game_over == True:
                    break
                if (mode == 2 and player ==2) or mode == 3:
                    if not game_over:
                        if mode == 3:
                            if player == 1:
                                depth_limit = depth_limit_1
                            else:
                                depth_limit = depth_limit_2
                        if best_move(player, board, EMPTY, depth_limit):
                            EMPTY -= 1
                            if check_win(player, board) or is_full_board(EMPTY):
                                game_over = True
                        player = player % 2 + 1
                        print (player)

                if buttonRestart.is_clicked(event, pg.MOUSEBUTTONDOWN):
                    restart_game(screen)
                    game_over = False
                    player = 1
                    pg.display.flip()

                elif mode == 1  or (mode == 2 and player ==1):
                    if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                        mouseX = event.pos[0] // SQUARE_SIZE
                        mouseY = event.pos[1] // SQUARE_SIZE
                        if is_available(mouseY, mouseX):
                            mark_square(board, mouseY, mouseX, player)
                            if check_win(player, board) or is_full_board(EMPTY):  # i can also make or full board 
                                game_over = True
                            player = player % 2 + 1
                            print(player)

                if not game_over:
                    draw_figures(screen, board)
                    draw_status(screen, player, game_over, 0, white)

                else:
                    if check_win(1, board):
                        draw_figures(screen,board, GREEN)
                        draw_lines(screen, GREEN)
                        draw_status(screen, player, game_over, 1, GREEN)
                    elif check_win(2, board):
                        draw_figures(screen, board, RED)
                        draw_lines(screen, RED)
                        draw_status(screen, player, game_over, 2, RED)
                    else:
                        draw_figures(screen, board, GRAY)
                        draw_lines(screen, GRAY)
                        draw_status(screen, player, game_over, 0, GRAY)

                pg.display.update()
                if mode ==1 or mode ==2:
                    break
