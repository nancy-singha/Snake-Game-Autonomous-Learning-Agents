# reinforcement learning
import timeit
#from Snake_2 import Direction, BLOCK_SIZE, Snake_info, Snake_Init, Snake, generate_snake_food, play_step
from Snake_nn import Snake_info, Direction
from collections import namedtuple
import numpy as np
from collections import deque
from ML_LearningModel1 import Linear_QNet, QTrainer
import torch
import random

import pandas as pd


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent2:
    def __init__(self):
        self.n_game = 0
        self.epsilon = 90  # Randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        # TODO: model,trainer

    # state (11 Values)
    # [ danger straight, danger right, danger left,
    #
    # direction left, direction right,
    # direction up, direction down
    #
    # food left,food right,
    # food up, food down]

    def get_state(self, snake):
        Point = namedtuple('Point', 'x , y')
        head = snake.head
        point_l = Point(head.x - 1, head.y)
        point_r = Point(head.x + 1, head.y)
        point_u = Point(head.x, head.y - 1)
        point_d = Point(head.x, head.y + 1)

        dir_l = snake.direction == Direction.LEFT
        dir_r = snake.direction == Direction.RIGHT
        dir_u = snake.direction == Direction.UP
        dir_d = snake.direction == Direction.DOWN

        danger_r= snake.is_collision( point_r)
        danger_l= snake.is_collision( point_l)
        danger_u= snake.is_collision( point_u)
        danger_d= snake.is_collision( point_d)

        state = [
            # Danger ahead
            (dir_r and danger_r) or
            (dir_u and danger_u) or
            (dir_d and danger_d) or
            (dir_l and danger_l),

            # Danger right
            (dir_u and danger_r) or
            (dir_d and danger_l) or
            (dir_l and danger_u) or
            (dir_r and danger_d),

            # Danger Left
            (dir_u and danger_l) or
            (dir_d and danger_r) or
            (dir_r and danger_u) or
            (dir_l and danger_d),

            # Move Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food Location
            snake.food.x < head.x,  # food is in left
            snake.food.x > head.x,  # food is in right
            snake.food.y < head.y,  # food is up
            snake.food.y > head.y  # food is down
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        # popleft if memory exceed
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if (len(self.memory) > BATCH_SIZE):
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff explotation / exploitation
        self.epsilon = 100 - self.n_game
        final_move = [0, 0, 0]
        if(random.randint(0, 200) < self.epsilon):
            move = random.randint(0, 2)
            final_move[move] = 1
            
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)  # prediction by model
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def start_game():
    total_score = 0
    highest_score=0
    agent = Agent2()
    #snake_grid= Snake()
    snake = Snake_info()
    #snake_head = [snake_grid[round(BLOCK_SIZE/2)][round(BLOCK_SIZE/2)]]
    #food = generate_snake_food(snake_grid, snake_head)
    start_time= timeit.default_timer()
    snake_data=[]
    
    model = Linear_QNet(11, 256, 3)
    model1= torch.load('model.pth')
    model.load_state_dict(model1)
    model.eval()
    agent.model= model
    #agent.model= torch.load('model.pth')
    while agent.n_game<500:       
        state_old = agent.get_state(snake)
        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        snake = snake.play_step(final_move )
        
        state_new = agent.get_state(snake)

        # train short memory
        agent.train_short_memory(state_old, final_move, snake.reward, state_new, snake.game_over)

        # remember
        agent.remember(state_old, final_move, snake.reward, state_new, snake.game_over)
        
        '''if(snake_info.score>1):
            print('xx')'''
        if snake.game_over:
            # Train long memory,plot result
            stop_time= timeit.default_timer()
            total_time= stop_time- start_time
            agent.n_game += 1
            agent.train_long_memory()
            if(snake.score > highest_score):  # new High score
                highest_score = snake.score
                agent.model.save()
            print('Game:', agent.n_game, 'Score:', snake.score, 'time: ', total_time, ' Highest Score:', highest_score)

            #df=pd.read_excel("nn_results.xlsx")
            snake_data.append([agent.n_game, snake.score, highest_score, total_time])

            #plot_scores.append(snake_info.score)
            total_score += snake.score
            mean_score = total_score / agent.n_game
            #plot_mean_scores.append(mean_score)
            # plot(plot_scores,plot_mean_scores)

            #===reset========
            #snake_grid= Snake()
            snake = Snake_info()
            '''snake_head = [snake_grid[round(BLOCK_SIZE/2)][round(BLOCK_SIZE/2)]]
            food = generate_snake_food(snake_grid, snake_head)'''
            start_time= timeit.default_timer()

    df= pd.DataFrame(snake_data, columns=['game_no', 'Score', 'Highest_Score', 'Suvival_time'])
    df.to_excel('nn_results.xlsx', sheet_name='sheet1', index=False)
score = []
start_game()