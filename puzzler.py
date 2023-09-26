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
        if self.moving:
            if self.rect.collidelist(collidables) != self.index and not self.movingBack or (self.rect.collidelist(doorList) != -1 and doorList[self.rect.collidelist(doorList)].type == 'door_closed'):
                self.movingBack = True
            if self.movingBack:
                self.moveBack()
            else: self.move()
        else:
            self.direction = movementDict[moveDir]

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
        
        self.type = 'goal'

class Button(Sprite):
    def __init__(self, coords, color, lever):
        Sprite.__init__(self, f'graphics/button/{color}_{lever * "lever" + (not lever) * "button"}.png', tileSize*7/8, tileSize*7/8, coords)
        
        self.images = [self.image, pygame.transform.scale(pygame.image.load(f'graphics/button/{color}_{lever * "lever" + (not lever) * "button"}_active.png').convert_alpha(), (tileSize*7/8, tileSize*7/8))]
        self.state = 0
        self.activated = False
        
        self.lever = lever
        self.color = color
        self.type = 'button'
        
    def update(self):
        if self.rect.collidelist(buttonables) != -1 and not self.activated:
            self.activated = True
            self.state = (self.state + 1) % 2
            self.image = self.images[self.state]
        
        if self.rect.collidelist(buttonables) == -1 and self.activated:
            self.activated = False
            if not self.lever:
                self.state = (self.state + 1) % 2
                self.image = self.images[self.state]
        
        if self.state: buttonColorsActivity[self.color] = True

class Door(Sprite):
    def __init__(self, coords, color):
        Sprite.__init__(self, f'graphics/door/{color}.png', tileSize, tileSize, coords)
        self.images = [self.image, pygame.transform.scale(pygame.image.load(f'graphics/door/{color}_active.png').convert_alpha(), (tileSize, tileSize))]
        
        self.coords = coords
        self.color = color
        self.type = 'door_closed'
        self.closing = False
    
    def update(self):
        if buttonColorsActivity[self.color]:
            self.image = self.images[1]
            self.type = 'door_open'
        else:
            self.closing = True
        
        if self.closing and self.rect.collidelist([player] + boxList) == -1:
            self.image = self.images[0]
            self.type = 'door_closed'
            self.closing = False



def textToTiles(text):
    global player, goal
    row = ''
    y = x = 0
    for ch in text:
        if ch == '\n':
            y += 1
            x = -1
        elif ch == '#':
            wallList.append(Wall((x, y)))
        else:
            if ch == 'b':
                boxList.append(Box((x, y)))
            elif ch == 'P':
                player = Player((x, y))
            elif ch == 'G':
                goal = Goal((x, y))
            elif ch == 'B':
                buttonList.append(Button((x, y), metadata[y][x][0], metadata[y][x][1]))
            elif ch == 'D':
                doorList.append(Door((x, y), metadata[y][x]))
            
            floorList.append(Floor((x, y)))
        
        x += 1


def loadLevel(text):
    global goal, player, boxList, doorList, wallList, floorList, buttonList, globalMovement, moveDir, screen, redActive, blueActive, greenActive, tileSize, tilesX, tilesY
    goal = 0
    player = 0
    boxList = []
    doorList = []
    wallList = []
    floorList = []
    buttonList = []
    globalMovement = False
    tileSize = 80
    tilesX = tilesY = 9
    moveDir = 0
    screen = pygame.display.set_mode((tileSize * tilesX, tileSize * tilesY))
    redActive = blueActive = greenActive = False
    
    textToTiles(text)


textLevel = '''#########
#P  #   #
# # #G# #
#B bB## #
#D# #  b #
# ##  # #
#b   #  #
# #b   ##
### #####'''

metadata = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, ['red', False], 0, 0, ['red', True], 0, 0, 0, 0], [0, 'red', 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

pygame.init()
clock = pygame.time.Clock()

movementDict = {0 : (0, 0), pygame.K_w : (0, -1), pygame.K_s : (0, 1), pygame.K_a : (-1, 0), pygame.K_d : (1, 0), pygame.K_UP : (0, -1), pygame.K_DOWN : (0, 1), pygame.K_LEFT : (-1, 0), pygame.K_RIGHT : (1, 0)}
shouldLoadLevel = True

while True:
    if shouldLoadLevel:
        shouldLoadLevel = False
        loadLevel(textLevel)
    buttonColorsActivity = {'red' : redActive, 'blue' : blueActive, 'green' : greenActive}
        
    allTiles = {'floor' : floorList, 'wall' : wallList, 'button' : buttonList, 'box' : boxList, 'door' : doorList, 'goal' : [goal], 'player' : [player]}
    collidables = allTiles['goal'] + allTiles['wall'] + allTiles['box']
    buttonables = allTiles['box'] + allTiles['player']
    
    for i in range(len(collidables)):
        collidables[i].index = i    
    for key in buttonColorsActivity:
        buttonColorsActivity[key] = False
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
            if event.key == pygame.K_r:
                shouldLoadLevel = True
        
        elif event.type == pygame.KEYDOWN and globalMovement == 0:
            if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                moveDir = event.key
    
    if player.gameWon:
        break

screen.fill('dark green')
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit