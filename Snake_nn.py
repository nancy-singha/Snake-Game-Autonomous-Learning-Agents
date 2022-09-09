from asyncio.windows_events import NULL
from math import sqrt
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

coordinates= namedtuple('coord', 'x, y')
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
        self.obstracle= False

        self.head= coordinates(round(BLOCK_SIZE/2), round(BLOCK_SIZE/2))
        self.snake= [self.head]
        self.direction = Direction.RIGHT
        self.food= coordinates(0,0)
        self.generate_snake_food()

        self.distance=0


# ==========================================================

    def show(self):
        for spot in self.snake:
            pygame.draw.rect(dis, white, [spot.x*hr+2, spot.y*wr+2, hr-4, wr-4])
        
        head= self.head
        pygame.draw.rect(dis, blue, [head.x*hr+2, head.y*wr+2, hr-4, wr-4])

        food= self.food
        pygame.draw.rect(dis, green, [food.x*hr+2, food.y*wr+2, hr-4, wr-4])
        


    def is_collision(self, pt=None):
        if(pt is None):
            pt = self.head
        # hit boundary
        if(pt.x >= BLOCK_SIZE or pt.x < 0 or pt.y >= BLOCK_SIZE or pt.y < 0):
            return True
        if (pt in self.snake[:-1]):
            return True
        return False

# ==============================================

    def generate_snake_food(self):
        self.food = coordinates(randint(0, BLOCK_SIZE - 1),randint(0, BLOCK_SIZE - 1))
        if (self.food in self.snake):  # food.obstrucle
            self.generate_snake_food()

    # =============Sanke Movement along the path==============


    def Snake_path(self, action):
        # snake following the path========================================================
        head = self.head
        head_x= head.x
        head_y= head.y
        done = False
        # clock.tick(10)

        clock.tick(30)
        dis.fill(black)
        # Action
        # [1,0,0] -> Straight
        # [0,1,0] -> Right Turn
        # [0,0,1] -> Left Turn

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right Turn
        else:                                       # action== 'Left':
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # Left Turn

        if new_dir == Direction.DOWN: #and (head.y + 1)<BLOCK_SIZE:    # down0
            head_y= head.y + 1
        elif new_dir == Direction.RIGHT: # and (head.x + 1)<BLOCK_SIZE:  # right1
            head_x= head.x + 1
        elif new_dir == Direction.UP: # and (head.y - 1)>=0:  # up2
            head_y=  head.y - 1
        elif new_dir == Direction.LEFT: # and (head.x - 1)>=0:  # left3
            head_x= head.x - 1

        self.head= coordinates(head_x, head_y)
        self.direction= new_dir

        self.snake.insert(0,self.head)


        if not(self.head.x == self.food.x and self.head.y == self.food.y):
            self.snake.pop(0)

    # ========================    NN DFF=====================


    def play_step(self, action):

        self.frame_iteration += 1
        # 1. Collect the user input
        for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                    quit()

        # 2. Move
        self.Snake_path(action)

        self.show()

        pygame.display.flip()  # display snake's movement

        # 3. Check if game Over
        reward = 0  # eat food: +10 , game over: -10 , else: 0
        game_over = False        
        distanceToFood= sqrt((self.head.x - self.food.x) ** 2 + (self.head.y - self.food.y) ** 2)

            # temp_head= new_snake_head[-1]
        if( self.is_collision() or self.frame_iteration > 100*len(self.snake)):
                self.game_over = True
                self.reward = -10
                return self
        
        elif( distanceToFood<self.distance):
            self.reward +=2
        
        self.distance= distanceToFood
        
        # add food to the screen
        if(self.head == self.food):
            self.score += 1
            self.reward += 10
            self.food= self.generate_snake_food()
            self.frame_iteration= self.frame_iteration/2


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

        return self
