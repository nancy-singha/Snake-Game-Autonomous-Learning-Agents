import Snake as SnakeGame
from random import randint

score=0

def get_path(snake_head, food):
    print('in get path- A* search')


snake= SnakeGame.Snake()
current = snake.snake_head[-1]
path_array = get_path(snake.food, snake.snake_head) #dir_array
food_array = [snake.food]
#while not achived
while SnakeGame.Snake_path(snake.snake_head, snake.grid, path_array, food_array):
    score= score+1
    food = snake.grid[randint(0, SnakeGame.rows - 1)][randint(0, SnakeGame.cols - 1)]
    if not (food.obstrucle or food in snake):
        break
    food_array.append(food)
    dir_array = get_path(food, snake)#return
    print(dir_array)
    


