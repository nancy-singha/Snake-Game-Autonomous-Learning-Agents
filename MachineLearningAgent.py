# reinforcement learning
import timeit
from Snake_2 import Direction, BLOCK_SIZE, Snake_info, Snake_Init, Snake, generate_snake_food, play_step
from collections import namedtuple
import numpy as np
from collections import deque
from ML_LearningModel1 import Linear_QNet, QTrainer
import torch
import random

import pandas as pd
import openpyxl


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent2:
    def __init__(self):
        self.n_game = 0
        self.epsilon = 0  # Randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(11, 300, 3)
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

    def get_state(self, game, food):
        Point = namedtuple('Point', 'x , y')
        head = game[-1]
        point_l = Point(head.x - 1, head.y)
        point_r = Point(head.x + 1, head.y)
        point_u = Point(head.x, head.y - 1)
        point_d = Point(head.x, head.y + 1)

        dir_l = head.direction == Direction.LEFT
        dir_r = head.direction == Direction.RIGHT
        dir_u = head.direction == Direction.UP
        dir_d = head.direction == Direction.DOWN

        danger_r= head.is_collision( [head], point_r)
        danger_l= head.is_collision( [head], point_l)
        danger_u= head.is_collision( [head], point_u)
        danger_d= head.is_collision( [head], point_d)

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
            food.x < head.x,  # food is in left
            food.x > head.x,  # food is in right
            food.y < head.y,  # food is up
            food.y > head.y  # food is down
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
            state0 = torch.tensor(state, dtype=torch.float).cuda()
            prediction = self.model(state0).cuda()  # prediction by model
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def start_game():
    total_score = 0
    highest_score=0
    agent = Agent2()
    snake_grid= Snake()
    snake_info = Snake_info()
    snake_head = [snake_grid[round(BLOCK_SIZE/2)][round(BLOCK_SIZE/2)]]
    food = generate_snake_food(snake_grid, snake_head)
    start_time= timeit.default_timer()
    snake_data=[]

    while agent.n_game<100:       
        state_old = agent.get_state(snake_head, food)
        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        snake_head, snake_info = play_step(snake_grid, snake_head, final_move, food, snake_info )

        # add food to the screen
        if(snake_head[-1] == food and snake_info.score==0):
            snake_info.reward = 5
        if(snake_head[-1] == food):
            snake_info.score += 1
            snake_info.reward += 5
            food= generate_snake_food(snake_grid, snake_head )
        
        state_new = agent.get_state(snake_head, food)

        # train short memory
        agent.train_short_memory(state_old, final_move, snake_info.reward, state_new, snake_info.game_over)

        # remember
        agent.remember(state_old, final_move, snake_info.reward, state_new, snake_info.game_over)

        '''if(snake_info.score>1):
            print('xx')'''
        stop_time= timeit.default_timer()
        if snake_info.game_over:
            # Train long memory,plot result
            total_time= stop_time- start_time
            agent.n_game += 1
            agent.train_long_memory()
            if(snake_info.score > highest_score):  # new High score
                highest_score = snake_info.score
                agent.model.save()
            print('Game:', agent.n_game, 'Score:', snake_info.score, 'time: ', total_time, ' Highest Score:', highest_score)

            #df=pd.read_excel("nn_results.xlsx")
            snake_data.append([agent.n_game, snake_info.score, highest_score, total_time])

            #plot_scores.append(snake_info.score)
            total_score += snake_info.score
            mean_score = total_score / agent.n_game
            #plot_mean_scores.append(mean_score)
            # plot(plot_scores,plot_mean_scores)

            #===reset========
            snake_grid= Snake()
            snake_info = Snake_info()
            snake_head = [snake_grid[round(BLOCK_SIZE/2)][round(BLOCK_SIZE/2)]]
            food = generate_snake_food(snake_grid, snake_head)
            start_time= timeit.default_timer()

    df= pd.DataFrame(snake_data, columns=['game_no', 'Score', 'Highest_Score', 'Suvival_time'])
    df.to_excel('nn_results.xlsx', sheet_name='sheet1', index=False)
score = []
start_game()