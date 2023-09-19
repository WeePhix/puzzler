import pygame
from sys import exit


class Sprite():
    def __init__(self, imgPath, sizeX, sizeY, coords):
        self.type = 'ERROR'
        
        self.image = pygame.image.load(imgPath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (sizeX, sizeY))
        
        self.rect = self.image.get_rect()
        self.rect.center = ((coords[0] + 0.5) * tileSize, (coords[1] + 0.5) * tileSize)
    
    def update(self):
        if self.rect.colliderect(player.rect): player.movingBack = True
    
    def draw(self):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startPosition):
        Sprite.__init__(self, 'graphics/player.png', tileSize*3/4, tileSize*3/4, startPosition)
        self.type = 'Player'
        
        self.moving = False
        self.movingBack = False
        
        self.animCounter = 0
        self.pixelCounter = 0
        self.direction = (0, 0)

        self.index = -1
        self.gameWon = False

    def move(self):        
        self.animCounter += 1
        
        if self.animCounter >= 2:
            self.pixelCounter += 1
            self.animCounter = 0
            self.rect.x += self.direction[0] * tileSize / 16
            self.rect.y += self.direction[1] * tileSize / 16
        
        if self.pixelCounter == 16:
            self.moving = False
            self.pixelCounter = 0
    
    def moveBack(self):
        self.animCounter += 1
        
        if self.animCounter >= 2:
            self.pixelCounter -= 1
            self.animCounter = 0
            self.rect.x -= self.direction[0] * tileSize / 16
            self.rect.y -= self.direction[1] * tileSize / 16
        
        if self.pixelCounter == 0:
            self.moving = False
            self.movingBack = False
    
    def update(self):
        # print(f'direction : {self.direction} \nmoveDir : {moveDir} \nmoving : {self.moving}\nmovingBack : {self.movingBack}')
        
        if self.moving:
            if self.rect.collidelist(collidables) != self.index and not self.movingBack:
                self.movingBack = True
            elif self.movingBack:
                self.moveBack()
            if not self.movingBack: self.move()
        else:
            self.direction = {0 : (0, 0), pygame.K_w : (0, -1), pygame.K_s : (0, 1), pygame.K_a : (-1, 0), pygame.K_d : (1, 0)}[moveDir]

            if self.direction != (0, 0):
                self.moving = True
        
        if self.rect.colliderect(goal):
            self.gameWon = True
        
class Floor(Sprite):
    def __init__(self, coords):
        Sprite.__init__(self, 'graphics/floor.png', tileSize, tileSize, coords)
        self.type = 'Floor'
        
        self.coords = coords
    
    def update(self): return 0


class Wall(Sprite):
    def __init__(self, coords):
        Sprite.__init__(self, 'graphics/wall.png', tileSize, tileSize, coords)
        self.type = 'Wall'
        
        self.coords = coords


class Box(Sprite):
    def __init__(self, coords):
        Sprite.__init__(self, 'graphics/box.png', tileSize*7/8, tileSize*7/8, coords)
        self.type = 'Box'
                
        self.moving = False
        self.movingBack = False

        self.animCounter = 0
        self.pixelCounter = 0
        self.direction = (0, 0)
        
        self.index = -1
    
    def move(self):        
        self.animCounter += 1
        
        if self.animCounter >= 2:
            self.pixelCounter += 1
            self.animCounter = 0
            self.rect.x += self.direction[0] * tileSize / 16
            self.rect.y += self.direction[1] * tileSize / 16
        
        if self.pixelCounter == 16:
            self.moving = False
            self.pixelCounter = 0
    
    def moveBack(self):        
        self.animCounter += 1
        
        if self.pixelCounter == 0:
            self.moving = False
            self.movingBack = False
        
        if self.animCounter >= 2:
            self.pixelCounter -= 1
            self.animCounter = 0
            self.rect.x -= self.direction[0] * tileSize / 16
            self.rect.y -= self.direction[1] * tileSize / 16
    
    def update(self):
        if self.moving:
            if self.rect.collidelistall(collidables) != [self.index] and not self.movingBack:
                self.movingBack = True
            if self.movingBack:
                self.moveBack()
            else: self.move()
        else:
            if self.rect.colliderect(player.rect):
                self.direction = player.direction
                self.moving = True


class Goal(Sprite):
    def __init__(self, coords):
        Sprite.__init__(self, 'graphics/goal.png', tileSize, tileSize, coords)
        
            

def numbersToTiles(array):
    global player, goal
    for y, row in enumerate(array):
        for x, tile in enumerate(row):
            if tile == 1:
                player = Player((x, y))
                floorList.append(Floor((x, y)))
            elif tile == 2:
                goal = Goal((x, y))
                floorList.append(Floor((x, y)))
            elif tile == 3:
                wallList.append(Wall((x, y)))
            elif tile == 4:
                boxList.append(Box((x, y)))
                floorList.append(Floor((x, y)))
            elif tile == 0:
                floorList.append(Floor((x, y)))

def textToNumbers(text):
    y = 0
    array = [[]]
    for i in text:
        if i == '\n':
            y += 1
            array.append([])
        else:
            array[y].append(textToNumDict[i])
    
    return array


textLevel ='''########
#P #G  #
#b b # #
##b #  #
# b # ##
## # b #
##    ##
########'''

textToNumDict = {' ' : 0, 'P' : 1, 'G' : 2, '#' : 3, 'b' : 4}

tileSize = 80
tilesX = tilesY = 8
moveDir = 0
globalMovement = False

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((tileSize * tilesX, tileSize * tilesY))

boxList = []
wallList = []
floorList = []

numbersLevel = textToNumbers(textLevel)
numbersToTiles(numbersLevel)

toPrint = True

while not player.gameWon:
    allTiles = {'floor' : floorList, 'wall' : wallList, 'box' : boxList, 'goal' : [goal]}
    collidables = allTiles['goal'] + allTiles['wall'] + allTiles['box']
    
    for i in range(len(collidables)):
        collidables[i].index = i    
    
    for tileType in allTiles:
        for tile in allTiles[tileType]:
            tile.update()
            tile.draw()
    
    player.update()
    player.draw()
    
    pygame.display.update()
    clock.tick(96)
    
    if globalMovement:
        continue
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        elif event.type == pygame.KEYUP:
            if event.key == moveDir:
                moveDir = 0
        
        elif event.type == pygame.KEYDOWN and globalMovement == 0:
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                moveDir = event.key

screen.fill('dark green')
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit