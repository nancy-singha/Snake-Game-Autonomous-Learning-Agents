from asyncio.windows_events import NULL
from turtle import distance
from pandas import concat
import pygame
import time
import random
from random import randint
from pygame import time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from enum import Enum
import numpy as np
from collections import namedtuple

from regex import B

# import A_Star_path

pygame.init()

# colour values
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# grid size of the game
'''cols = 20
rows = 20'''

BLOCK_SIZE = 20  # rows=cols=BLOCK_SIZE

# Dimentions of the window
display_width = 400
display_height = 400

wr = display_width/BLOCK_SIZE
hr = display_height/BLOCK_SIZE

dis = pygame.display.set_mode((display_width, display_height))
# pygame.display.set_caption('Snake Game by Nancy Singha')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# =====================================================


class Direction(Enum):
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, blue)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 6, display_height / 3])

# ===============Snake initalize========================


class Snake_info:
    def __init__(self):
        self.frame_iteration = 0
        self.score = 0
        self.reward = 0
        self.game_over = False
        self.snake_length = 0
        self.clock = pygame.time.Clock()
        self.last_eight_moves= []
# ==========================================================
class Snake_Init:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.obstrucle = False
        self.direction= Direction.RIGHT
        '''if randint(1, 101) < 3:
            self.obstrucle = True'''
        #print(self.x, self.y, self.f, self.g, self.h,'\n', self.neighbors, '\n', self.camefrom, '\n', self.obstrucle,'\n xxxxxxxxxxxxxxx')

    def show(self, color):
        pygame.draw.rect(dis, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])


    def is_collision(self, snake, pt=None, body=False):
        if(pt is None):
            pt = snake[-1]
        # hit boundary
        if(pt.x >= BLOCK_SIZE or pt.x < 0 or pt.y >= BLOCK_SIZE or pt.y < 0):
            return True
        if (body and pt in snake[:-1]):
            return True
        return False

# ==============START================


def Snake():
    grid = [[Snake_Init(i, j) for j in range(BLOCK_SIZE)]
            for i in range(BLOCK_SIZE)]
    # print(grid)
    return grid

# ==============================================

def generate_snake_food(snake_grid, head):
    food = snake_grid[randint(0, BLOCK_SIZE - 1)][randint(0, BLOCK_SIZE - 1)]
    if (food in head):  # food.obstrucle
        generate_snake_food(snake_grid, head)
    return food

    # =============Sanke Movement along the path==============


def Snake_path(snake_head, snake, action, food):
    # snake following the path========================================================
    head = snake_head[-1]
    done = False
    # clock.tick(10)

    clock.tick(30)
    dis.fill(black)
     # Action
     # [1,0,0] -> Straight
     # [0,1,0] -> Right Turn
     # [0,0,1] -> Left Turn

    clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
    idx = clock_wise.index(head.direction)
    if np.array_equal(action, [1, 0, 0]):
        new_dir = clock_wise[idx]
    elif np.array_equal(action, [0, 1, 0]):
        next_idx = (idx + 1) % 4
        new_dir = clock_wise[next_idx]  # right Turn
    else:                                       # action== 'Left':
        next_idx = (idx - 1) % 4
        new_dir = clock_wise[next_idx]  # Left Turn

    if new_dir == Direction.DOWN and (head.y + 1)<BLOCK_SIZE:    # down0
        snake_head.append(snake[head.x][head.y + 1])
    elif new_dir == Direction.RIGHT and (head.x + 1)<BLOCK_SIZE:  # right1
        snake_head.append(snake[head.x + 1][head.y])
    elif new_dir == Direction.UP and (head.y - 1)>=0:  # up2
        snake_head.append(snake[head.x][head.y - 1])
    elif new_dir == Direction.LEFT and (head.x - 1)>=0:  # left3
        snake_head.append(snake[head.x - 1][head.y])

    else:
        if new_dir == Direction.DOWN:    # down0
            snake_head[-1].y= head.y + 1
        elif new_dir == Direction.RIGHT:  # right1
            snake_head[-1].x= head.x+1
        elif new_dir == Direction.UP:  # up2
            snake_head[-1].y= head.y - 1
        elif new_dir == Direction.LEFT:  # left3
            snake_head[-1].x= head.x-1
        return snake_head, False
    current = snake_head[-1]

    if not(current.x == food.x and current.y == food.y):
        snake_head.pop(0)
    '''else:
        print('food')'''

    for spot in snake_head:
        Snake_Init.show(spot, white)
        spot.direction =new_dir

    food.show(green)
    snake_head[-1].show(blue)
    pygame.display.flip()  # display snake's movement
    return snake_head, True

    # ========================    NN DFF=====================


def play_step(snake_grid, snake_head, action, food, snakeInfo):

    snake_info = snakeInfo
    snake_info.frame_iteration += 1
       # 1. Collect the user input
    for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()

        # 2. Move
    new_snake_head, alive = Snake_path(snake_head, snake_grid, action, food)
        # self.snake.insert(0,self.head)

        # 3. Check if game Over
    reward = 0  # eat food: +10 , game over: -10 , else: 0
    game_over = False
        # temp_head= new_snake_head[-1]
    if(alive== False or Snake_Init.is_collision(new_snake_head, new_snake_head,None ,True) or snake_info.frame_iteration > 100*len(snake_grid)):
            snake_info.game_over = True
            snake_info.reward = -10
            return snake_head,snake_info

    

    #5 check if repetative moves:
    '''snake_info.last_eight_moves.append(new_snake_head[-1].direction)

    if(len(snake_info.last_eight_moves)>8):
        snake_info.last_eight_moves.pop(0)
        if(snake_info.last_eight_moves[0]==snake_info.last_eight_moves[4] and
        snake_info.last_eight_moves[1]==snake_info.last_eight_moves[5] and
        snake_info.last_eight_moves[2]==snake_info.last_eight_moves[6] and
        snake_info.last_eight_moves[3]==snake_info.last_eight_moves[7]):
            snake_info.reward = snake_info.reward -5
            snake_info.last_eight_moves.pop(0)
            snake_info.last_eight_moves.pop(1)
            snake_info.last_eight_moves.pop(2)
            snake_info.last_eight_moves.pop(3)'''

    # 6. Return game Over and Display Score

    return new_snake_head, snake_info
