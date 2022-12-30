import torch
import random
import numpy as np
from collections import deque
from GamePT import Game, snakeBlock
from model import LinearQNet, QTrainer
from SnakePT import Point, Direction
from Plot import plot
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"



MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self) -> None:
        self.nGames = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount/ random value between 0 and 1 usually around 0.8-0.9
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = LinearQNet(11, 256, 3) #Entry values / hidden values/ output values
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def getState(self, snake, food):
        head = snake.snakeHead
        point_l = Point(head.x - snakeBlock, head.y)
        point_r = Point(head.x + snakeBlock, head.y)
        point_u = Point(head.x, head.y - snakeBlock)
        point_d = Point(head.x, head.y + snakeBlock)
        
        dir_l = snake.direction == Direction.Left
        dir_r = snake.direction == Direction.Right
        dir_u = snake.direction == Direction.Up
        dir_d = snake.direction == Direction.Down

        state = [
            # Danger straight
            (dir_r and snake.isCollision(point_r)) or 
            (dir_l and snake.isCollision(point_l)) or 
            (dir_u and snake.isCollision(point_u)) or 
            (dir_d and snake.isCollision(point_d)),

            # Danger right
            (dir_u and snake.isCollision(point_r)) or 
            (dir_d and snake.isCollision(point_l)) or 
            (dir_l and snake.isCollision(point_u)) or 
            (dir_r and snake.isCollision(point_d)),

            # Danger left
            (dir_d and snake.isCollision(point_r)) or 
            (dir_u and snake.isCollision(point_l)) or 
            (dir_r and snake.isCollision(point_u)) or 
            (dir_l and snake.isCollision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            food.foodX < head.x,  # food left
            food.foodX > head.x,  # food right
            food.foodY < head.y,  # food up
            food.foodY > head.y  # food down
            ]
        #print(state)

        return np.array(state, dtype=int)

    
    def Remember(self, state, action, reward, nextState, done):
        self.memory.append((state, action, reward, nextState, done)) #popleft if MAX_MEMORY is reached

    def TrainLongMemory(self):
        if len(self.memory) > BATCH_SIZE:
            miniSample = random.sample(self.memory, BATCH_SIZE) #list of tuples 
        else:
            miniSample = self.memory
        states, actions, rewards, nextStates, dones = zip(*miniSample)
        self.trainer.TrainStep(states, actions, rewards, nextStates, dones)


    def TrainShortMemory(self, state, action, reward, nextState, done):
        self.trainer.TrainStep(state, action, reward, nextState, done) 

    def GetAction(self, state):
        #random movemnt and exploration
        self.epsilon = 80 - self.nGames
        finalMove = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            finalMove[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            finalMove[move] = 1
        return finalMove

def Train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    while True:

        stateOld = agent.getState(game.snake, game.food)

        finalMove = agent.GetAction(stateOld)

        reward, done, score = game.PlayStep(finalMove)

        stateNew = agent.getState(game.snake, game.food)

        #train short memory
        agent.TrainShortMemory(stateOld, finalMove, reward, stateNew, done)

        agent.Remember(stateOld, finalMove, reward, stateNew, done)

        if done:
            #train long memory
            game.GameReset()
            agent.nGames += 1
            agent.TrainLongMemory()

            if score > record:
                record = score
                agent.model.save()
            print("Game:", agent.nGames, "Score:", score, "Record:", record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.nGames
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)



if __name__ == "__main__":
    Train()