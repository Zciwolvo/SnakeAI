import pygame


class Snake:

    snakeLength = 1
    snakeList = []
    snakeHead = []
    x = 0
    y = 0
    width = 0
    height = 0
    snakeBlock = 0
    reward = 0
    frameIteration = 0

    def __init__(self, width, height, snakeBlock) -> None:
        self.width = width
        self.height = height
        self.snakeBlock = snakeBlock
        self.x = width/2
        self.y = height/2
        self.snakeHead = []
        self.snakeList = []
        self.snakeLength = 1
        self.frameIteration = 0

    xChange = 0
    yChange = 0
    direction = ""

    def Snake(self, snakeBlock, display, snakeColor):
        for e in self.snakeList:
            pygame.draw.rect(display, snakeColor, [e[0], e[1], snakeBlock, snakeBlock])

    def Movement(self, key):
        if key == pygame.K_LEFT and self.direction != "right":
            self.xChange = -self.snakeBlock
            self.yChange = 0
            self.direction = "left"
        elif key == pygame.K_RIGHT and self.direction != "left":
            self.xChange = self.snakeBlock
            self.yChange = 0
            self.direction = "right"
        elif key == pygame.K_UP and self.direction != "down":
            self.yChange = -self.snakeBlock
            self.xChange = 0
            self.direction = "up"
        elif key == pygame.K_DOWN and self.direction != "up":
            self.yChange = self.snakeBlock
            self.xChange = 0
            self.direction = "down"

    def HeadMovement(self):
        self.snakeHead = []
        self.snakeHead.append(self.x)
        self.snakeHead.append(self.y)
        self.snakeList.append(self.snakeHead)
        if len(self.snakeList) > self.snakeLength or self.frameIteration > 100*self.snakeLength:
            del self.snakeList[0]
        for x in self.snakeList[:-1]:
            if x == self.snakeHead:
                self.reward -= 10
                return True
        return False


    def BorderTouch(self, head=None):
        if head == None:
            if self.x >= self.width or self.x < 0 or self.y >= self.height or self.y < 0:
                self.reward -= 10
                return True
            else:
                return False
        else:
            if head[0] >= self.width or head[0] < 0 or head[1] >= self.height or head[1] < 0:
                self.reward -= 10
                return True
            else:
                return False
        
    def isCollision(self, head):
        W1 = self.BorderTouch(head=head)
        W2 = False
        for x in self.snakeList[:-1]:
            if x == self.snakeHead:
                self.reward -= 10
                W2 = True
        if W1 is True or W2 is True:
            return True
        return False

