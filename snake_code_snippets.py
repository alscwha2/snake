#!/usr/bin/env python3

"""
Welcome to command line snake! 

How to play:
    Steer with WASD.
    Press q at any time to exit.

Modes:
    Regular mode:
        Steer with WASD, each tick the snake will advance one tile.

    Manual mode:
        Steer with WASD. Each time a key is pressed, the snake will advance one tile.
        Any key can be pressed to advance the snake. j and k work well.

    Solve:
        Sit back and relax while the game plays itself in front of your eyes!
        Exit early with CTRL+C



usage: snake [-h] [--mode {regular,manual,solver}] [-r] [-m] [-s] [-a]

Play snake from the command line

options:
  -h, --help            show this help message and exit
  --mode {regular,manual,solver}
                        play game in specified game mode defaults to manual
  -r                    play game in regular mode
  -m                    play game in manual mode
  -s                    watch as the game plays itself
  -a, --auto            automatically start a new game on crash

open an issue at https://github.com/alscwha2/scripts/issues

TODO:
    [] find a way to make the output display normally when using threads
    [] implement regular mode with one thread
    [] track high scores
    [] allow array keys to be used instead of WASD
    [] ensure that the game works with odd sized boards

Notes:
    * Collision and eating checks are done in the move_head function
"""
import os
import termios
import tty
import sys
import random
import argparse
from threading import Thread
from time import sleep

################################################################################
########################### Constants ##########################################
################################################################################

# directions
UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)

# snake pieces
HORIZONTAL, VERTICAL = '\u2550', '\u2551'
BOTTOM_LEFT, BOTTOM_RIGHT, TOP_LEFT, TOP_RIGHT = '\u255A', '\u255D', '\u2554', '\u2557'

# game parameters
BOARD_SIZE = 18
INITIAL_SNAKE_LENGTH = 5
SOLVER_TICK_SPEED = 0.05
TICK = 0.2
AUTO_NEW_GAME = False # may be changed by supplying -a --auto argument


################################################################################
########################### GLOBAL VARIABLES ###################################
################################################################################

board = [[]]
empty_tiles = []

head = (0, 0)
tail = (0, 0)

next_direction = RIGHT
head_direction = RIGHT
tail_direction = RIGHT

crashed = False
ate = False
snake_length = INITIAL_SNAKE_LENGTH

################################################################################
########################### FUNCTION DEFINITIONS ###############################
################################################################################

############################### BOARD ##########################################


def place_food():
    new_food_tile = random.choice(empty_tiles)
    write_board_char(new_food_tile, "X")


################################# SNAKE #######################################


def move(end, direction):
    return end[0] + direction[0], end[1] + direction[1]


######################################## HEAD ##################################
def check_ate():
    global ate
    ate = read_board_char(head) == 'X'


def check_crash():
    global crashed
    crashed = read_board_char(head) not in {" ", "X"}


def move_head(direction):
    global head, head_direction

    # if you're changing direction, bend the snake's neck in that direction
    write_board_char(head, bend_neck(direction))

    head_direction = direction
    head = move(head, direction)

    # before overwriting the piece, check if it's food or a crash
    check_ate()
    check_crash()

    # place head piece in the new head
    write_board_char(head, VERTICAL if head_direction in {UP, DOWN} else HORIZONTAL)

    if not crashed:
        empty_tiles.remove(head)


##################################### TAIL #####################################


def update_tail():
    if not ate:
        global tail, tail_direction
        # increment tail
        write_board_char(tail, ' ')
        empty_tiles.append(tail)
        tail = move(tail, tail_direction)

        # check if tail is changing direction, update accordingly
        tail_char = read_tail_char()
        if tail_char in {BOTTOM_RIGHT, BOTTOM_LEFT, TOP_RIGHT, TOP_LEFT}:
            update_tail_direction(tail_char)


############################# GAME INITIALIZATION ###############################

def initialize_game():
    initialize_variables()
    initialize_empty_board()
    initialize_snake()
    place_food()

############################# DRAW GAME ########################################

def print_game():
    draw_board()
    print_score()


############################# EXECUTE COMMANDS #################################


def change_direction(command):
    global next_direction
    if command == 'w' and head_direction != DOWN:
        next_direction = UP
    elif command == 'a' and head_direction != RIGHT:
        next_direction = LEFT
    elif command == 's' and head_direction != UP:
        next_direction = DOWN
    elif command == 'd' and head_direction != LEFT:
        next_direction = RIGHT


def execute(command):
    if command in {'w', 'a', 's', 'd'}:
        change_direction(command)
    if command == 'q':
        sys.exit(0)


def watch_and_execute_commands():
    while not crashed:
        command = get_char()
        execute(command)


############################## RUN GAME ########################################


def update_game():
    move_head(next_direction)
    update_tail()
    if ate:
        global snake_length
        snake_length += 1
        try:
            place_food()
        except IndexError:
            global crashed
            crashed = True
            print_game()
            print("You Win!")


def update_game_loop():
    while not crashed:
        print_game()
        sleep(TICK)
        update_game()

################################################################################
############################# PLAY GAME ########################################
################################################################################

def regular_mode():
    Thread(target=update_game_loop, daemon=True).start()
    Thread(target=watch_and_execute_commands).start()

def manual_mode():
    while True:
        if crashed:
            if AUTO_NEW_GAME:
                initialize_game()
            else:
                ask_play_again()
                initialize_game()

        print_game()
        command = get_char()
        execute(command)
        update_game()


################################################################################
############################# SOLVER ###########################################
################################################################################


def get_next_solution_step():
    row, column = head

    top_row = 1
    leftmost_column = 1
    second_row = 2
    bottom_row = BOARD_SIZE - 2
    rightmost_column = BOARD_SIZE - 2

    if head_direction == RIGHT:
        return   DOWN if row == second_row \
            else UP if row == bottom_row \
            else UP if column == rightmost_column \
            else RIGHT

    elif head_direction == DOWN:
        return   RIGHT if row == bottom_row \
            else DOWN

    elif head_direction == LEFT:
        return   DOWN if column == leftmost_column \
            else LEFT

    elif head_direction == UP:
        return   LEFT if row == top_row \
            else UP if column == rightmost_column \
            else RIGHT if row == second_row \
            else UP


def solve():
    global next_direction
    while not crashed:
        print_game()
        sleep(SOLVER_TICK_SPEED)
        next_direction = get_next_solution_step()
        update_game()


################################################################################
############################# APPLICATION LOGIC ################################
################################################################################

def main():
    args = parse_args()
    global AUTO_NEW_GAME
    AUTO_NEW_GAME = args.auto

    initialize_game()
    if args.mode == 'manual':
        manual_mode()
    elif args.mode == 'solver':
        solve()
    elif args.mode == 'regular':
        regular_mode()

main()
