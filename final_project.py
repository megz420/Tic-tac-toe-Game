import sys
import numpy as np
import pygame as pg

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
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# AI portion definition
MAXIMIZER = True
MINIMIZER = False
player_move = (0,0)

# screen
screen = pg.display.set_mode ((WIDTH,HEIGHT+70))
pg.display.set_caption('Tic Tac Toe Game')


# defining board array
board = np.zeros((BOARD_ROWS,BOARD_COLS))

# drawing lines 
def draw_lines (color = WHITE):
    for i in range (1, BOARD_ROWS+1):
        pg.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pg.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

# drawing figures X O
def draw_figures(color = WHITE):
    for row in range (BOARD_ROWS):
        for col in range (BOARD_COLS):
            if board[row][col] == 2:
                pg.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH )
            elif board[row][col] == 1:
                pg.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE //4), (col * SQUARE_SIZE + (3 * SQUARE_SIZE) // 4 , row * SQUARE_SIZE + (3 * SQUARE_SIZE) // 4), 15)
                pg.draw.line(screen, color, (col * SQUARE_SIZE + (3 * SQUARE_SIZE) // 4, row * SQUARE_SIZE + SQUARE_SIZE //4), (col * SQUARE_SIZE + SQUARE_SIZE // 4 , row * SQUARE_SIZE + (3 * SQUARE_SIZE) // 4),15)
                
# marking the square
def mark_square (row, col, player):
    board[row][col] = player

# checking if available square
def is_available (row, col):
    return board[row][col] == 0

# checking if board is full 
def is_full_board (board = board):
    for row in range (board.shape[0]):
        for col in range (board.shape[1]):
            if board[row][col] == 0:
                return False
    return True

# checking if win       # modified
def check_win (player, board = board):
    for col in range (BOARD_COLS):
        for row in range (0 , BOARD_ROWS-3):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player :
                return True
    for row in range (BOARD_ROWS):
        for col in range (0 , BOARD_COLS-3):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player :
                return True
    for i in range(3, -1, -1):
        for j in range (i,BOARD_ROWS-3):
            if ((board[(j-i)][j] == player and board[(j-i)+1][j+1] == player and board[(j-i)+2][j+2] == player and board[(j-i)+3][j+3] == player) or
                (board[j][(j-i)] == player and board[j+1][(j-i)+1] == player and board[j+2][(j-i)+2] == player and board[j+3][(j-i)+3] == player)):
                return True  
    shift = 0
    for i in range(3,BOARD_ROWS):
        m = i 
        for j in range (i,BOARD_ROWS-5,-1):
            if ((board[(i-j)][j] == player and board[(i-j)+1][j-1] == player and board[(i-j)+2][j-2] == player and board[(i-j)+3][j-3] == player) or
                (board[(i+j-shift)][(m-shift)] == player and board[(i+j-shift)-1][(m-shift)+1] == player and board[(i+j-shift)-2][(m-shift)+2] == player and board[(i+j-shift)-3][(m-shift)+3] == player)):
                return True
            m = m + 1
        shift += 2
    return False 


# MINMAX function for AI part
# Depth limit for Minimax
Hard = 0
DEPTH_LIMIT = 2
DEPTH_LIMIT_1 =2
DEPTH_LIMIT_2 =2

def min_max(board ,BOARD_ROWS,BOARD_COLS, depth , alpha, beta, is_maximizer,depth_limit):
    if check_win(2,board):
        return 100- depth 
    elif  check_win(1,board):
        return -100 + depth
    elif is_full_board(board) or depth >= depth_limit:
        return 0 

    if is_maximizer == MAXIMIZER:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = min_max(board ,BOARD_ROWS,BOARD_COLS, depth + 1, alpha, beta, MINIMIZER,depth_limit) 
                    board[row][col] = 0
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:  # Beta cutoff
                        break
        return best_score

    else:  # MINIMIZER's move
        worst_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = min_max(board, BOARD_ROWS, BOARD_COLS, depth + 1, alpha, beta, MAXIMIZER,depth_limit) 
                    board[row][col] = 0
                    worst_score = min(worst_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:  # Alpha cutoff
                        break
        return worst_score
empty = 49
# Choosing the best move
def best_move(player,depth_limit):
    print ("Hard ", Hard) 
    best_score = -1000
    move = (-1, -1)    
    if empty == 48 :
        if player_move[0] == 0:
            mark_square( int(player_move[0])+1, int(player_move[1]),player)
        else:
            mark_square( int(player_move[0])-1, int(player_move[1]),player)
        return True
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            useful_move = False
            for row2 in range(row-1, row+2):
                for col2 in range(col-1, col+2):
                    if row2 < 0 or col2 < 0 or row2 >= BOARD_ROWS or col2 >= BOARD_COLS:
                        continue
                    if board[row2][col2] != 0:
                        useful_move = True
                        break
                if useful_move:
                    break
            if board[row][col] == 0  and useful_move:
                board[row][col] = 2
                score = min_max(board,BOARD_ROWS,BOARD_COLS, 0, -float("inf"), float("inf"), MINIMIZER,depth_limit)
                board[row][col] = 0
                print (score)
                if Hard == 1 and empty <=30:
                    depth_limit = 4
                if Hard == 1 and empty <=20:
                    depth_limit = 5
                if best_score < score:
                    best_score = score
                    move = (row, col)
    if best_score == -1000:
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    return True
    if move != (-1, -1):
        print (move)
        mark_square(move[0], move[1], player)
        return True
    print(move)
    return False


# start positions as initialization
player = 1
game_over = False

# function for restarting the game 
def restart_game():
    screen.fill(BLACK)
    draw_lines()
    empty =49
    for row in range (BOARD_ROWS):
        for col in range (BOARD_COLS):
            board[row][col] = 0

# start positions as initialization


# Buttons part
# Define fonts
font = pg.font.SysFont(None, 48)

# Class for button
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        # Check if the mouse is over the button
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pg.draw.rect(screen, self.hover_color, self.rect)
        else:
            pg.draw.rect(screen, self.color, self.rect)

        # Render the text on the button
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# score that shown in gui while playing 
score = np.zeros((2,))

# Create buttons
button1 = Button(130, 80, 400, 80, "Player vs. Player", (51,101,0), HOVER_COLOR)
button2 = Button(130, 180, 400, 80, "Player vs. Computer", (153,153,0), HOVER_COLOR)
button3 = Button(130, 280, 400, 80, "Computer vs. Computer", (153,0,0), HOVER_COLOR)
button4 = Button(130, 80, 400, 80, "Easy", (220,43,5), HOVER_COLOR)
button5 = Button(130, 180, 400, 80, "medium", (33,44,56), HOVER_COLOR)
button6 = Button(130, 280, 400, 80, "Hard", (87,200,38), HOVER_COLOR)
button9 = Button(350, 640, 300, 50, "Restart",BLACK, HOVER_COLOR)

# for selecting the mode of players
mode_selected = 0
mode = 0

# score that shown in gui while playing 
score = np.zeros((2,))
        
# Main loop
running = True
while running:
    screen.fill(BLACK)
    screen.fill(BLACK)
    title_text = "Choose Mode"
    title_surface = font.render(title_text, True, WHITE)
    screen.blit(title_surface, (WIDTH // 3, 20))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if button1.is_clicked(event):
            print("Player vs. Player mode selected!")
            mode_selected = 1
            mode = 1
            running = False ; break
        if button2.is_clicked(event):
            print("Player vs. Computer mode selected!")
            mode_selected = 1
            mode = 2
            running = False ; break
        if button3.is_clicked(event):
            print("Computer vs. Computer mode selected!")
            mode_selected = 1 
            mode = 3
            running = False ; break

    # Draw the buttons
    button1.draw(screen)
    button2.draw(screen)
    button3.draw(screen)


    pg.display.flip()
running = True
while running:
    if mode == 1:
        running = False
    screen.fill(BLACK)
    title_text = "Computer Level"
    title_surface = font.render(title_text, True, WHITE)
    screen.blit(title_surface, (WIDTH // 3.2, 20))
    button4.draw(screen)
    button5.draw(screen)
    button6.draw(screen)
    for event in pg.event.get():
        if button4.is_clicked(event):
            print("Easy")
            DEPTH_LIMIT_1 = 1
            Hard =0
            running = False
        if button5.is_clicked(event):
            print("Medium")
            DEPTH_LIMIT_1 = 2
            Hard = 0
            running = False
        if button6.is_clicked(event):
            print("Hard")
            DEPTH_LIMIT_1 = 3
            Hard = 1
            running = False
        if event.type == pg.QUIT:
            running = False
        pg.display.flip()

if mode ==3:
    running = True
    while running:
        screen.fill(BLACK)
        title_text = "Computer_2 Level"
        title_surface = font.render(title_text, True, WHITE)
        screen.blit(title_surface, (WIDTH // 3.2, 20))
        button4.draw(screen)
        button5.draw(screen)
        button6.draw(screen)
        for event in pg.event.get():
            if button4.is_clicked(event):
                print("Easy")
                DEPTH_LIMIT_2 = 1
                Hard =0
                running = False
            if button5.is_clicked(event):
                print("Medium")
                DEPTH_LIMIT_2 = 2
                Hard = 0
                running = False
            if button6.is_clicked(event):
                print("Hard")
                DEPTH_LIMIT_2 = 3
                Hard = 1
                running = False
            if event.type == pg.QUIT:
                running = False
            pg.display.flip()


# infinite loop (main of the game)
if mode_selected == 1:
    while True:
        screen.fill(BLACK)
        draw_lines()
        button9.draw(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if button9.is_clicked(event):
                restart_game()
                game_over = False
                empty = 49
                player = 1
                pg.display.flip()
                break
                            
                            
            while True:
                if game_over == True:
                    break
                if button9.is_clicked(event):
                    restart_game()
                    game_over = False
                    empty = 49
                    player = 1
                    pg.display.flip()
                    break        
                                
                if (mode == 2 and player ==2) or mode == 3:
                    if not game_over:
                        if player == 2 and mode == 3:
                            DEPTH_LIMIT = DEPTH_LIMIT_2
                        elif (mode == 3 and player ==1) or (mode == 2 and player ==2):
                            DEPTH_LIMIT = DEPTH_LIMIT_1
                        elif mode == 2:
                            DEPTH_LIMIT
                        if best_move(player,DEPTH_LIMIT):
                            print ("ai is here")
                            if check_win(player):
                                game_over = True
                                score[player-1] +=1
                            elif is_full_board():
                                game_over = True
                        player = player % 2 + 1
                        empty -=1
                        print (player)
                        
                if mode == 1  or (mode == 2 and player ==1):
                    if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                        mouseX = event.pos[0] // SQUARE_SIZE
                        mouseY = event.pos[1] // SQUARE_SIZE
                        if is_available(mouseY, mouseX):
                            mark_square(mouseY, mouseX, player)
                            if check_win(player):  # i can also make or full board 
                                game_over = True
                                score[player-1] +=1
                            elif is_full_board():
                                game_over = True
                            player = player % 2 + 1
                            empty -=1
                            player_move = (mouseY,mouseX)
                            print(player)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        restart_game()
                        game_over = False
                        player = 1

                if not game_over:
                    draw_figures()
                else:
                    if check_win(1):
                        draw_figures(GREEN)
                        draw_lines(GREEN)
                    elif check_win(2):
                        draw_figures(RED)
                        draw_lines(RED)
                    else:
                        draw_figures(GRAY)
                        draw_lines(GRAY)
                
                pg.display.update()
                if mode ==1 or mode ==2:
                    break
