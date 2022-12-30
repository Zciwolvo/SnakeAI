from pickle import NONE
import pygame
from collections import namedtuple
from enum import Enum
import numpy as np

class Direction(Enum):
    Right = 1
    Left = 2
    Up = 3
    Down = 4

Point = namedtuple("Point", "x, y")

class SnakePT:


    def __init__(self, width, height, block) -> None:
        self.width = width
        self.height = height
        self.snakeBlock = block
        self.x = self.width/2
        self.y = self.height/2
        self.snakeHead = Point(self.width/2, self.height/2)
        self.snakeList = []
        self.snakeLength = 1
        self.frameIteration = 0
        self.reward = 0
        self.direction = Direction.Right
    

    def Snake(self, snakeBlock, display, snakeColor):
        for e in self.snakeList:
            pygame.draw.rect(display, snakeColor, [e[0], e[1], snakeBlock, snakeBlock])


    def HeadMovement(self, pt=None):
        if pt is None:
            pt = self.snakeHead
        self.snakeList.append(pt)
        if len(self.snakeList) > self.snakeLength or self.frameIteration > 100*len(self.snakeList):
            del self.snakeList[0]
        for x in self.snakeList[:-1]:
            if x == pt:
                self.reward = -10
                return True
        return False


    def BorderTouch(self):
        if self.snakeHead.x >= self.width or self.snakeHead.x < 0 or self.snakeHead.y >= self.height or self.snakeHead.y < 0:
            self.reward = -10
            return True
        return False

    def isCollision(self, point):
        output = False
        if point.x > self.width - self.snakeBlock or point.x < 0 or point.y > self.height - self.snakeBlock or point.y < 0:
            output = True
            self.reward = -5
        for x in self.snakeList[:-1]:
            if x == point:
                output = True
                self.reward = -5
        return output
        
    def FoodDirection(self, food):
        Dirs = []
        if food.foodX < self.snakeHead.x:
            Dirs.append(Direction.Left)
        else:
           Dirs.append(Direction.Right)

        if food.foodY < self.snakeHead.y:
            Dirs.append(Direction.Up)
        else:
            Dirs.append(Direction.Down)
        return Dirs

    def GenerateRays(self, dir):
        ListOfPoints = []
        if dir == Direction.Right:
            for p in range(int((self.width - self.snakeHead.x)/ self.snakeBlock)):
                ListOfPoints.append(Point(self.snakeHead.x + (self.snakeBlock * p), self.snakeHead.y))
        elif dir == Direction.Down:
            for p in range(int((self.height - self.snakeHead.y)/ self.snakeBlock)):
                ListOfPoints.append(Point(self.snakeHead.x, self.snakeHead.y + (self.snakeBlock * p)))
        elif dir == Direction.Left:
            for p in range(int((self.snakeHead.x)/ self.snakeBlock)):
                ListOfPoints.append(Point(self.snakeHead.x - (self.snakeBlock * p), self.snakeHead.y))
        elif dir == Direction.Up:
            for p in range(int((self.snakeHead.y)/ self.snakeBlock)):
                ListOfPoints.append(Point(self.snakeHead.x, self.snakeHead.y - (self.snakeBlock * p)))
        return(ListOfPoints)