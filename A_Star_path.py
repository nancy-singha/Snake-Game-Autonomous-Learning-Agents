from importlib.resources import path
from operator import le
from pandas import isnull
import Snake as SnakeGame
from random import randint
from numpy import empty, sqrt
from Snake import Direction, Your_score
import timeit
import pandas as pd 
import pygame

global screen_counter

def get_path(food, snake_head):
    #print('in get path- A* search')
    #f(n)= g(n) + h(n)
    #h(n)= sqrt( (x_start- x_destination)^2 + (y_start- y_destination)^2 )- Ecludian distance
    head= snake_head[:]
    food.camefrom = []
    for s in snake_head:
        s.camefrom = []
    openset = [head.pop()]
    closedset = []
    dir_array1 = []
    while 1:
        try:
            current1 = min(openset, key=lambda x: x.f)  #~takes the index of an item f in list x, sets that as the key
        except ValueError:
            return dir_array1
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        for neighbor in current1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake_head:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food.x) ** 2 + (neighbor.y - food.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1
        if current1 == food:
            break
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(Direction.UP)
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(Direction.DOWN)
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(Direction.LEFT)
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(Direction.RIGHT)
        current1 = current1.camefrom
    #print(dir_array1)
    for i in range(SnakeGame.BLOCK_SIZE):
        for j in range(SnakeGame.BLOCK_SIZE):
            snake_grid[i][j].camefrom = []
            snake_grid[i][j].f = 0
            snake_grid[i][j].h = 0
            snake_grid[i][j].g = 0
    return dir_array1

def start_game(screen_counter):
    score=0
    snake_head = [snake_grid[round(SnakeGame.BLOCK_SIZE/2)][round(SnakeGame.BLOCK_SIZE/2)]]
    food= SnakeGame.generate_snake_food(snake_grid, snake_head)
    current = snake_head[-1]

    path_array = get_path(food, snake_head) #dir_array
    if len(path_array)==0:
        print(path_array)
    food_array = [food]
    #print(path_array)
    screen_counter= screen_counter+len(path_array)
    new_snake_head= SnakeGame.Snake_path(snake_head, snake_grid, path_array, food, current, screen_counter, score)
    
    #while not achived
    while new_snake_head!=[]:
        score= score+1
        Your_score(score)
        pygame.display.update()
        current = new_snake_head[-1]
        food= SnakeGame.generate_snake_food(snake_grid, new_snake_head)
        food_array.append(food)
        path_array = get_path(food, new_snake_head)#return
        if path_array==[]:
            break
        #print(path_array)
        screen_counter= screen_counter+len(path_array)
        new_snake_head= SnakeGame.Snake_path(new_snake_head, snake_grid, path_array, food, current, screen_counter, score)
    return score, screen_counter

#Start
snake_grid= SnakeGame.Snake()
score=[]
result_data=[]
screen_counter=0
for i in range(0,500):
    Your_score(score)
    pygame.display.update()
    start_time= timeit.default_timer()
    results=start_game(screen_counter)
    total_time= timeit.default_timer()-start_time
    score.append(results[0])
    screen_counter=results[1]
    result_data.append([i, results[0], max(score), total_time])
    print('Game:', i, ' Score:', results[0], ' Survival_time:', total_time, ' Highest Score:', max(score))
df= pd.DataFrame(result_data, columns=['game_no', 'Score', 'Highest_Score', 'Survival_time'])

df.to_excel('AStar_results.xlsx', sheet_name='Sheet1', index=False)



