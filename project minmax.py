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
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15

# AI portion definition
MAXIMIZER = True
MINIMIZER = False

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
                pg.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE //4), (col * SQUARE_SIZE + (3 * SQUARE_SIZE) // 4 , row * SQUARE_SIZE + (3 * SQUARE_SIZE) // 4), CROSS_WIDTH)
                pg.draw.line(screen, color, (col * SQUARE_SIZE + (3 * SQUARE_SIZE) // 4, row * SQUARE_SIZE + SQUARE_SIZE //4), (col * SQUARE_SIZE + SQUARE_SIZE // 4 , row * SQUARE_SIZE + (3 * SQUARE_SIZE) // 4), CROSS_WIDTH)
                
# marking the square
def mark_square (row, col, player):
    board[row][col] = player

# checking if available square
def is_available (row, col):
    return board[row][col] == 0

# checking if board is full 
def is_full_board (board = board):
    for row in range (BOARD_ROWS):
        for col in range (BOARD_COLS):
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
DEPTH_LIMIT = 2
DEPTH_LIMIT_1 = 2
DEPTH_LIMIT_2 = 2

def min_max(board, depth , alpha, beta, is_maximizer):
    if check_win(2, board):
        return 100- depth 
    elif check_win(1, board):
        return -100 + depth
    elif is_full_board(board) or depth >= DEPTH_LIMIT:
        return 0  

    if is_maximizer == MAXIMIZER:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = min_max(board, depth + 1, alpha, beta, MINIMIZER) 
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
                    score = min_max(board, depth + 1, alpha, beta, MAXIMIZER) 
                    board[row][col] = 0
                    worst_score = min(worst_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:  # Alpha cutoff
                        break
        return worst_score


# Choosing the best move
def best_move(player):
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = min_max(board, 0, -float("inf"), float("inf"), MINIMIZER)
                board[row][col] = 0
                print(score)
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

# function for restarting the game 
def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range (BOARD_ROWS):
        for col in range (BOARD_COLS):
            board[row][col] = 0

# start positions as initialization
player = 1
game_over = False

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

# Create buttons
buttonPvP = Button(130, 80, 400, 80, "Player vs. Player", (51,101,0), HOVER_COLOR)
buttonPvC = Button(130, 180, 400, 80, "Player vs. Computer", (153,153,0), HOVER_COLOR)
buttonCvC = Button(130, 280, 400, 80, "Computer vs. Computer", (153,0,0), HOVER_COLOR)
buttonEasy = Button(130, 80, 400, 80, "Easy", (220,43,5), HOVER_COLOR)
buttonMedium = Button(130, 180, 400, 80, "medium", (33,44,56), HOVER_COLOR)
buttonHard = Button(130, 280, 400, 80, "Hard", (87,200,38), HOVER_COLOR)
buttonRestart = Button(350, 640, 300, 50, "Restart" , BLACK, HOVER_COLOR)
buttonStr = Button(10, 640, 200, 50, "score= "+ str(DEPTH_LIMIT) , BLACK, HOVER_COLOR)

mode_selected = False
mode = 0

# Main loop for mode selection
while not mode_selected:
    screen.fill(BLACK)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if buttonPvP.is_clicked(event):
            print("Player vs. Player mode selected!")
            mode = 1
            mode_selected = True
        if buttonPvC.is_clicked(event):
            print("Player vs. Computer mode selected!")
            mode = 2
            mode_selected = True
        if buttonCvC.is_clicked(event):
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
    screen.blit(title_surface, (WIDTH // 3.2, 20))
    while not difficulty_selected:
        buttonEasy.draw(screen)
        buttonMedium.draw(screen)
        buttonHard.draw(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if buttonEasy.is_clicked(event):
                DEPTH_LIMIT = 1
                difficulty_selected = True
            if buttonMedium.is_clicked(event):
                DEPTH_LIMIT = 2
                difficulty_selected = True
            if buttonHard.is_clicked(event):
                DEPTH_LIMIT = 3
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
            if buttonEasy.is_clicked(event):
                DEPTH_LIMIT_2 = 1
                difficulty_selected = True
            if buttonMedium.is_clicked(event):
                DEPTH_LIMIT_2 = 2
                difficulty_selected = True
            if buttonHard.is_clicked(event):
                DEPTH_LIMIT_2 = 3
                difficulty_selected = True
        DEPTH_LIMIT_1 = DEPTH_LIMIT
        pg.display.flip()



# infinite loop (main of the game)
if mode_selected == 1:
    while True:
        screen.fill(BLACK)
        draw_lines()
        buttonRestart.draw(screen)
        buttonStr.draw(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            
            if buttonRestart.is_clicked(event):
                    restart_game()
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
                                DEPTH_LIMIT = DEPTH_LIMIT_1
                            else:
                                DEPTH_LIMIT = DEPTH_LIMIT_2
                        if best_move(player):
                            print ("ai is here")
                            if check_win(player) or is_full_board():
                                game_over = True
                        player = player % 2 + 1
                        print (player)

                if buttonRestart.is_clicked(event):
                    restart_game()
                    game_over = False
                    player = 1
                    pg.display.flip()

                elif mode == 1  or (mode == 2 and player ==1):
                    if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                        mouseX = event.pos[0] // SQUARE_SIZE
                        mouseY = event.pos[1] // SQUARE_SIZE
                        if is_available(mouseY, mouseX):
                            mark_square(mouseY, mouseX, player)
                            if check_win(player) or is_full_board():  # i can also make or full board 
                                game_over = True
                            player = player % 2 + 1
                            print(player)

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
