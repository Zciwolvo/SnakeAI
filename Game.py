import pygame
import random
from Snake import Snake
from SnakePT import SnakePT
from Food import Food

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
snakeSpeed = 15


font = pygame.font.SysFont(None, 50)

#Color options
boardColor = blue
snakeColor = black
foodColor = green
fontColor = red

class Game:

    def Message(self, msg, color):
        mesg = font.render(msg, True, color)
        display.blit(mesg, [100, 100])

    def DisplayScore(self, score, color):
        scoreNumber = font.render(("Score: " + str(score)), True, color)
        display.blit(scoreNumber, [20, 20])

    def Game(self):

        #snake and food initiation
        snake = Snake(width, height, snakeBlock)
        food = Food(width, height, snakeBlock)

        #Must-be-like-that variables
        gameOver = False
        gameClose = False

        #Score counter
        score = 0

        #Game loop
        while not gameOver:
            snake.frameIteration += 1
            #Beggining screen/End screen inputs
            while gameClose == True: 
                self.Game()
                """display.fill(boardColor)
                self.DisplayScore(score, fontColor)
                self.Message("Q - to quit | C - to continue", fontColor)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameOver = True
                            gameClose = False
                        if event.key == pygame.K_c:
                            self.Game()"""
            
            #Game inputs/Snake movement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = True
                elif event.type == pygame.KEYDOWN:
                    snake.Movement(event.key)
            snake.x += snake.xChange
            snake.y += snake.yChange

            
            #Checking if board border has been touched
            gameClose = snake.BorderTouch()

            display.fill(boardColor)

            #Respawning food
            food.DropFood(display, foodColor)

            #Checking if head ate its tail
            if gameClose != True:
                gameClose = snake.HeadMovement()

            #Regenerating snake
            snake.Snake(snakeBlock=snakeBlock, display=display, snakeColor=snakeColor)
            self.DisplayScore(score, fontColor)

            pygame.display.update()

            #Checking if food has been eaten
            if snake.x == food.foodX and snake.y == food.foodY:
                #If true generating new food positon and increasing snake's length/score
                food.RandomizePositon()
                snake.snakeLength += 1
                score += 1
                snake.reward += 10

            clock.tick(snakeSpeed)

        pygame.quit()
        quit()

gra = Game()

gra.Game()  