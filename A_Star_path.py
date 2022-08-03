from importlib.resources import path
from pandas import isnull
import Snake as SnakeGame
from random import randint
from numpy import empty, sqrt

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
            dir_array1.append(2)
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)
        current1 = current1.camefrom
    #print(dir_array1)
    for i in range(SnakeGame.rows):
        for j in range(SnakeGame.cols):
            snake_grid[i][j].camefrom = []
            snake_grid[i][j].f = 0
            snake_grid[i][j].h = 0
            snake_grid[i][j].g = 0
    return dir_array1

def start_game(screen_counter):
    score=0
    snake_head = [snake_grid[round(SnakeGame.rows/2)][round(SnakeGame.cols/2)]]
    food = snake_grid[randint(0, SnakeGame.rows-1)][randint(0, SnakeGame.cols-1)]
    current = snake_head[-1]

    path_array = get_path(food, snake_head) #dir_array

    food_array = [food]
    #print(path_array)
    screen_counter= screen_counter+len(path_array)
    new_snake_head= SnakeGame.Snake_path(snake_head, snake_grid, path_array, food, current, screen_counter)

    #while not achived
    while new_snake_head!=[]:
        score= score+1
        
        current = new_snake_head[-1]
        while 1:
            food = snake_grid[randint(0, SnakeGame.rows - 1)][randint(0, SnakeGame.cols - 1)]
            if not ( food in new_snake_head):   #food.obstrucle or
                break
        food_array.append(food)
        path_array = get_path(food, new_snake_head)#return
        if path_array==[]:
            break
        #print(path_array)
        screen_counter= screen_counter+len(path_array)
        new_snake_head= SnakeGame.Snake_path(new_snake_head, snake_grid, path_array, food, current, screen_counter)
    return score, screen_counter

#Start
snake_grid= SnakeGame.Snake()
score=[]
screen_counter=0
for i in range(0,20):
    results=start_game(screen_counter)
    score.append(results[0])
    screen_counter=results[1]
    print('score for game no',i, ': ', score)
print('Highest Score: ', max(score))


