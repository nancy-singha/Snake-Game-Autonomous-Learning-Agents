from asyncio.windows_events import NULL
from turtle import distance
import pygame 
import time
import random
from random import randint
from pygame import time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w

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
cols = 20
rows = 20

#Dimentions of the window
display_width = 400
display_height = 400

wr = display_width/cols
hr = display_height/rows

display = pygame.display.set_mode((display_width, display_height))
#pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
clock.tick(10)

snake_block = 10
snake_speed = 10
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, blue)
    display.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width / 6, display_height / 3])
 
 
'''def gameLoop():
    game_over = False
    game_close = False
 
    x1 = display_width / 2
    y1 = display_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
 
    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
 
        while game_close == True:
            display.fill(white)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
 
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        display.fill(white)
        pygame.draw.rect(display, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 '''

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
        pygame.draw.rect(display, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    #defining the immidiate neighbors for each position in the grid
    def add_neighbors(self, grid):
        #print('self_neighbors of:', self.x, self.y )
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
           self.neighbors.append(grid[self.x][self.y + 1])

#==============START================
def Snake():
    grid = [[Snake_Init(i, j) for j in range(cols)] for i in range(rows)]
    #print(grid)
    for i in range(rows):
        for j in range(cols):
            grid[i][j].add_neighbors(grid)

    '''snake_head = [grid[round(rows/2)][round(cols/2)]]
    food = grid[randint(0, rows-1)][randint(0, cols-1)]
    current = snake_head[-1]'''
    
    return grid


#=============Sanke Movement along the path==============

def Snake_path(snake, grid, path_array, food, current):
    #snake following the path========================================================
    done = False
    #clock.tick(10)
    while not done:
        clock.tick(10)
        display.fill(black)
        direction = path_array.pop(-1)
        if direction == 0:    # down
            snake.append(grid[current.x][current.y + 1])
        elif direction == 1:  # right
            snake.append(grid[current.x + 1][current.y])
        elif direction == 2:  # up
            snake.append(grid[current.x][current.y - 1])
        elif direction == 3:  # left
            snake.append(grid[current.x - 1][current.y])
        current = snake[-1]

        if current.x == food.x and current.y == food.y:
            return snake     #Goal achived, next food requested
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
        pygame.display.flip()  #display snake's movement
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
                return [] #terminate, game ended
            elif event.type == KEYDOWN:
                if event.key == K_w and not direction == 0:
                    direction = 2
                elif event.key == K_a and not direction == 1:
                    direction = 3
                elif event.key == K_s and not direction == 2:
                    direction = 0
                elif event.key == K_d and not direction == 3:
                    direction = 1