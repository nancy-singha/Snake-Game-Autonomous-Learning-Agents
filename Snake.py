from asyncio.windows_events import NULL
from importlib.resources import path
from turtle import distance
from pandas import concat
import pygame 
import time
import random
from random import randint
from pygame import time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from enum import Enum

from regex import B

#import A_Star_path 
 
pygame.init()

#colour values
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

#grid size of the game
'''cols = 20
rows = 20'''

BLOCK_SIZE=20 #rows=cols=BLOCK_SIZE

#Dimentions of the window
display_width = 400
display_height = 400

wr = display_width/BLOCK_SIZE
hr = display_height/BLOCK_SIZE

dis = pygame.display.set_mode((display_width, display_height))
#pygame.display.set_caption('Snake Game by Nancy Singha')
 
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 20)

#=====================================================
class Direction(Enum):
    DOWN = 0
    RIGHT = 1
    UP = 2
    LEFT = 3
 
def Your_score(score):
    value = score_font.render("Score: " + str(score), True, red)
    dis.blit(value, [0, 0])
 
'''

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 6, display_height / 3])'''

#===============Snake initalize========================
class Snake_Init:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False
        '''if randint(1, 101) < 3:
            self.obstrucle = True'''
        #print(self.x, self.y, self.f, self.g, self.h,'\n', self.neighbors, '\n', self.camefrom, '\n', self.obstrucle,'\n xxxxxxxxxxxxxxx')

    def show(self, color):
        pygame.draw.rect(dis, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    #defining the immidiate neighbors for each position in the grid
    def add_neighbors(self, grid):
        #print('self_neighbors of:', self.x, self.y )
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < BLOCK_SIZE - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < BLOCK_SIZE - 1:
           self.neighbors.append(grid[self.x][self.y + 1])

    def is_collision(self,pt=None):
        if(pt is None):
            pt = self.head
        #hit boundary
        if(pt.x>display_width-BLOCK_SIZE or pt.x<0 or pt.y>display_height - BLOCK_SIZE or pt.y<0):
            return True
        if(pt in self.snake[1:]):
            return True
        return False

def generate_snake_food(snake_grid, head):
    food = snake_grid[randint(0, BLOCK_SIZE - 1)][randint(0, BLOCK_SIZE - 1)]
    if ( food in head):   #food.obstrucle
        food= generate_snake_food(snake_grid, head)
    if(food.x== 10 and food.y==10 and head[-1].x==10 and head[-1].y==10):
        print('issue')
        food= generate_snake_food(snake_grid, head)
    return food

#==============START================
def Snake():
    grid = [[Snake_Init(i, j) for j in range(BLOCK_SIZE)] for i in range(BLOCK_SIZE)]
    #print(grid)
    for i in range(BLOCK_SIZE):
        for j in range(BLOCK_SIZE):
            grid[i][j].add_neighbors(grid)
    return grid

#=============Sanke Movement along the path==============
'''def is_collision(self,pt=None):
        if(pt is None):
            pt = self.head
        #hit boundary
        if(pt.x>self.w-rows or pt.x<0 or pt.y>self.h - cols or pt.y<0):
            return True
        if(pt in self.snake[1:]):
            return True
        return False'''

def Snake_path(snake, grid, path_array, food, current, screen_counter,score):
    #snake following the path========================================================
    done = False
    
    while not done:
        clock.tick(40)
        dis.fill(black)
        direction = path_array.pop(-1)
        if direction == Direction.DOWN:    # down0
            snake.append(grid[current.x][current.y + 1])
        elif direction == Direction.RIGHT:  # right1
            snake.append(grid[current.x + 1][current.y])
        elif direction == Direction.UP:  # up2
            snake.append(grid[current.x][current.y - 1])
        elif direction == Direction.LEFT:  # left3
            snake.append(grid[current.x - 1][current.y])
        current = snake[-1]

        if current.x == food.x and current.y == food.y:
            return snake     #Goal achived, next food requested
        elif len(path_array)==0:
            done=True
            return []
        else:
            snake.pop(0)

        for spot in snake:
            Snake_Init.show(spot, white)
        '''for i in range(rows):
            for j in range(cols):
                if grid[i][j].obstrucle:
                    grid[i][j].show(RED)'''

        food.show(green)
        snake[-1].show(blue)

        Your_score(score)

        pygame.display.flip()  #display snake's movement

        #Storing screen frames
        '''screen_name= 'Frames/screen_'+ str(screen_counter)+'.jpg'
        pygame.image.save(pygame.display.get_surface(), screen_name)
        screen_counter += 1'''

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
                return [] #terminate, game ended