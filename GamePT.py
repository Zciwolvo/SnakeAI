import pygame
from collections import namedtuple
from SnakePT import SnakePT, Direction
from Food import Food
import numpy as np


Point = namedtuple("Point", "x, y")

pygame.init()


#Display size options
width = 600
height = 600
display = pygame.display.set_mode((width, height))

pygame.display.update()

#Window caption
pygame.display.set_caption("Snake")


#Colors
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

clock = pygame.time.Clock()


#Gamechanging variables 
snakeBlock = 30
snakeSpeed = 100


font = pygame.font.SysFont(None, 50)

#Color options
boardColor = blue
snakeColor = black
foodColor = green
fontColor = red

class Game:

    def __init__(self) -> None:
        self.snake = SnakePT(width, height, snakeBlock)
        self.food = Food(self.snake.width, self.snake.height, self.snake.snakeBlock)
        self.gameOver = False
        self.score = 0
        self.reward = 0
        self.goodDir = False
        self.speed = snakeSpeed
        self.snakeBlock = snakeBlock

    def GameReset(self):
        self.snake = SnakePT(width, height, snakeBlock)
        self.food = Food(self.snake.width, self.snake.height, self.snake.snakeBlock)
        self.gameOver = False
        self.score = 0

    def Message(self, msg, color):
        mesg = font.render(msg, True, color)
        display.blit(mesg, [100, 100])

    def DisplayScore(self, score, color):
        scoreNumber = font.render(("Score: " + str(score)), True, color)
        display.blit(scoreNumber, [20, 20])

    def Movement(self, action):
        clockWise = [Direction.Right, Direction.Down, Direction.Left, Direction.Up]
        idx = clockWise.index(self.snake.direction)
        if np.array_equal(action, [1, 0, 0]):
            newDir = clockWise[idx] #no change
        elif np.array_equal(action, [0, 1, 0]):
            nextIdx = (idx+1) % 4
            newDir = clockWise[nextIdx] #right turn
        else: #[0,0,1]
            nextIdx = (idx-1) % 4
            newDir = clockWise[nextIdx] #left turn
        self.snake.direction = newDir
        
        x = self.snake.snakeHead.x
        y = self.snake.snakeHead.y

        if self.snake.direction == Direction.Right:
            x += self.snakeBlock
        elif self.snake.direction == Direction.Left:
            x -= self.snakeBlock
        elif self.snake.direction == Direction.Down:
            y += self.snakeBlock
        elif self.snake.direction == Direction.Up:
            y -= self.snakeBlock
        self.snake.snakeHead = Point(x, y)

    def PlayStep(self, action):
        self.snake.frameIteration += 1

        #Game inputs/Snake movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.Movement(action)
        foodDir = self.snake.FoodDirection(self.food)
        if self.snake.direction in foodDir:
            self.snake.reward = 5
        else:
            self.snake.reward = -5
        
        Rays = self.snake.GenerateRays(self.snake.direction)

        for r in Rays:
            if r in self.snake.snakeList[:-1]:
                self.snake.reward = -5
        
        #Checking if board border has been touched
        self.gameOver = self.snake.BorderTouch()

        display.fill(boardColor)

        #Respawning food
        self.food.DropFood(display, foodColor)

        #Checking if head ate its tail
        if self.gameOver != True:
            self.gameOver = self.snake.HeadMovement()
        
        #Regenerating snake
        self.snake.Snake(snakeBlock=snakeBlock, display=display, snakeColor=snakeColor)
        self.DisplayScore(self.score, fontColor)

        pygame.display.update()

        #Checking if food has been eaten
        if self.snake.snakeHead.x == self.food.foodX and self.snake.snakeHead.y == self.food.foodY:
            #If true generating new food positon and increasing snake's length/score
            self.food.RandomizePositon()
            self.snake.snakeLength += 1
            self.score += 1
            self.snake.reward = 10
            self.goodDir = self.snake.FoodDirection(self.food)
            return self.snake.reward, self.gameOver, self.score
        
        self.goodDir = self.snake.FoodDirection(self.food)
        clock.tick(self.speed)
        return self.snake.reward, self.gameOver, self.score
    


    def Game(self, action):
        self.GameReset()
        while not self.gameOver:
            self.PlayStep(action)
        pygame.quit()
        quit()
