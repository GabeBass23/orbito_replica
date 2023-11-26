import numpy
import pygame
import sys
import math
from Board import Board
from enum import Enum

class Directions(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def main():
    # Initialize Pygame
    pygame.init()
    board = Board()
    player1 = 0
    player2 = 1
    mouse_x = None
    mouse_y = None
    dragging = False
    stage = 1
    full_counter = 0
    s2_start = None
    turn = player1

    # Sets up display
    width, height = 600, 800
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Orbito Window')

    draw_board(window, board, width)
    pygame.display.update()
    # Main game loop
    running = True

    while running:
        if stage == 3:
            pygame.time.wait(2000)
            board.rotate()
            draw_board(window, board, width)
            pygame.display.update()

            winner = board.game_over()
            if not winner == -1:
                if winner == 2:
                    print("The game is a draw!")
                else:
                    print("Player", winner + 1, "wins!")
                pygame.time.wait(2000)
                running = False
            turn = not turn
            if not board.full():
                stage = 1
            else:
                full_counter += 1
                # terminates after 5 full rounds
                if full_counter == 5:
                    print("The game is a draw!")
                    pygame.time.wait(2000)
                    running = False
        
        # draw_board(window, board, width)
        # pygame.display.update()
            
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            pygame.display.update()
            # pygame.time.wait(3000)
            if event.type == pygame.MOUSEBUTTONDOWN and stage == 1:
                next_move = move_locator(event, width)
                # need to do error handling later
                if board.add_tile(turn, next_move):
                    stage = 2
            elif event.type == pygame.MOUSEBUTTONDOWN and stage == 2 and not dragging:
                s2_start = move_locator(event, width)
                if board.get_coord(s2_start) == (not turn):
                    board.remove_tile(s2_start)
                    dragging = True
                continue
            elif event.type == pygame.KEYDOWN and stage == 2 and not dragging:
                if event.key == pygame.K_s:
                    # temporary to skip this turn
                    stage = 3
                    continue
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                curr_pos = move_locator(event, width)
                if board.valid_swap(s2_start, curr_pos):
                    board.add_tile(not turn, curr_pos)
                    stage = 3
                else:
                    board.add_tile(not turn, s2_start)
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()

            
            draw_board(window, board, width)
            pygame.display.update()
            if dragging:
                if turn == player1:
                    pygame.draw.circle(window, (0,0,0), (mouse_x, mouse_y), width/12)
                else:
                    pygame.draw.circle(window, (255,255,255), (mouse_x, mouse_y), width/12)
            pygame.display.update()


    # Quit Pygame
    pygame.quit()
    sys.exit()


def draw_board(window, board, width):
    border = 3
    size = math.floor((width - (2 * border))/4)
    size2 = size - (2 * border)
    extra = math.floor(((width - (2 * border)) % 4)/2)
    
    BACKDROP = (200, 50, 50)
    ARROWS = (100, 0, 0)
    # sets background color to black
    window.fill((0,0,0))

    # creates rectangles for gameplay
    for i in range(4):
        for j in range(4):
            top_row = extra + border + 200 + i * (size)
            top_col = extra + border + j * (size)
            row_top = top_row + border
            row_bottom = row_top + size2
            col_left = top_col + border
            col_right = col_left + size2
            pygame.draw.rect(window, BACKDROP, (col_left, row_top, \
                size - 2 * border, size - 2 * border))
            dir = which_triangle((i,j))
            if(dir == Directions.NORTH):
                pygame.draw.polygon(window, ARROWS, ((col_left, row_bottom), \
                    (col_right, row_bottom), (top_col + size/2, row_top)))
            elif(dir == Directions.SOUTH):
                pygame.draw.polygon(window, ARROWS, ((col_left, row_top), \
                    (col_right - 1, row_top), (top_col + size/2, row_bottom)))
            elif(dir == Directions.EAST):
                pygame.draw.polygon(window, ARROWS, ((col_left, row_top), \
                    (col_left, row_bottom), (col_right, top_row + size/2)))
            else:
                pygame.draw.polygon(window, ARROWS, ((col_right, row_top), \
                    (col_right, row_bottom), (col_left, top_row + size/2)))
            
            if board.get_coord((i,j)) == 0:
                pygame.draw.circle(window, (255,255,255), \
                    (top_col + size/2, top_row + size/2), size/3)
            elif board.get_coord((i,j)) == 1:
                pygame.draw.circle(window, (0,0,0), \
                    (top_col + size/2, top_row + size/2), size/3)
            

def move_locator(event, width):
    col = int(math.floor(event.pos[0]/(width/4)))
    row = int(math.floor((event.pos[1] - 200)/(width/4)))
    return (row, col)

def which_triangle(coord):
    row, col = coord
    if (col == 0 and not row == 3) or (col == 1 and row == 1):
        return Directions.SOUTH
    elif (col == 3 and not row == 0) or (col == 2 and row == 2):
        return Directions.NORTH
    elif (row == 3 and not col == 3) or (col == 1 and row == 2):
        return Directions.EAST
    else:
        return Directions.WEST


if __name__ == "__main__":
    main()