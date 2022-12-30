import random
import pygame

class Food:


    def __init__(self, width, height, snakeBlock) -> None:
        self.snakeBlock = snakeBlock
        self.width = width
        self.height = height
        self.foodX = round(random.randrange(0, width - self.snakeBlock) / self.snakeBlock) * self.snakeBlock
        self.foodY = round(random.randrange(0, height - self.snakeBlock) / self.snakeBlock) * self.snakeBlock
    
    def DropFood(self, display, foodColor):
        pygame.draw.rect(display, foodColor, [self.foodX, self.foodY, self.snakeBlock, self.snakeBlock])
    
    def RandomizePositon(self):
        self.foodX = round(random.randrange(0, self.width - self.snakeBlock) / self.snakeBlock) * self.snakeBlock
        self.foodY = round(random.randrange(0, self.height - self.snakeBlock) / self.snakeBlock) * self.snakeBlock