import pygame
from sys import exit


class Sprite():
    def __init__(self, imgPath, sizeX, sizeY, coords):
        self.image = pygame.image.load(imgPath).convert_alpha()
        self.image = pygame.transform.scale(self.image, (sizeX, sizeY))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] * tileSize, coords[1] * tileSize)
    
    def update(self):
        return 0
    
    def draw(self):
        screen.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, startPosition):
        Sprite.__init__(self, 'graphics/player.png', tileSize, tileSize, startPosition)
        
        self.moving = False
        self.surrWalls = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.moveFreedom = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.animCounter = 0
        self.pixelCounter = 0
        self.direction = (0, 0)
        
    def checkMoveOptions(self, walls):
        self.surrWalls = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.moveFreedom = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        
        for wall in walls:
            if wall.rect.centery - self.rect.centery == -tileSize:
                if wall.rect.centerx - self.rect.centerx == -tileSize:
                    self.surrWalls[0][0] = wall
                elif wall.rect.centerx - self.rect.centerx == 0:
                    self.surrWalls[0][1] = wall
                elif wall.rect.centerx - self.rect.centerx == tileSize:
                    self.surrWalls[0][2] = wall
            elif wall.rect.centery - self.rect.centery == 0:
                if wall.rect.centerx - self.rect.centerx == -tileSize:
                    self.surrWalls[1][0] = wall
                elif wall.rect.centerx - self.rect.centerx == 0:
                    self.surrWalls[1][1] = wall
                elif wall.rect.centerx - self.rect.centerx == tileSize:
                    self.surrWalls[1][2] = wall
            elif wall.rect.centery - self.rect.centery == tileSize:
                if wall.rect.centerx - self.rect.centerx == -tileSize:
                    self.surrWalls[2][0] = wall
                elif wall.rect.centerx - self.rect.centerx == 0:
                    self.surrWalls[2][1] = wall
                elif wall.rect.centerx - self.rect.centerx == tileSize:
                    self.surrWalls[2][2] = wall
        
        for y in range(3):
            for x in range(3):
                if x != 1 and y != 1:
                    self.moveFreedom[y][x] = not(self.surrWalls[y][1] or self.surrWalls[1][x] or self.surrWalls[y][x])
                elif self.surrWalls[y][x] == 0:
                    self.moveFreedom[y][x] = 1
                self.moveFreedom[y][x] = 1 if self.moveFreedom[y][x] else 0
        
        
    def defineMoveDir(self):
        global moveDir
        moveVec = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        moveVec[moveDir[1] + 1][moveDir[0] + 1] = 1
        
        moveVec[0][1] = moveVec[0][0] or moveVec[0][1] or moveVec[0][2]
        moveVec[2][1] = moveVec[2][0] or moveVec[2][1] or moveVec[2][2]
        moveVec[1][0] = moveVec[0][0] or moveVec[1][0] or moveVec[2][0]
        moveVec[1][2] = moveVec[0][2] or moveVec[1][2] or moveVec[2][2]
        
        for y in [0, 2, 1]:
            if self.moving: break
            for x in [0, 2, 1]:
                if moveVec[y][x] == self.moveFreedom[y][x] == 1 and (x != 1 or y != 1):
                    self.direction = (x-1, y-1)
                    self.moving = True
                    break

    def move(self):
        print(self.animCounter, self.pixelCounter)
        self.animCounter += 1
        self.pixelCounter += 1
        if self.animCounter >= 2:
            self.animCounter = 0
            self.rect.x += self.direction[0] * tileSize / 8
            self.rect.y += self.direction[1] * tileSize / 8
        
        if self.pixelCounter == 16:
            self.moving = False
            self.pixelCounter = 0
    
    def update(self):
        self.checkMoveOptions(wallList)
        self.defineMoveDir()
        if self.moving: self.move()

class Floor(Sprite):
    def __init__(self, coords):
        Sprite.__init__(self, 'graphics/floor.png', tileSize, tileSize, coords)
        
        self.coords = coords


class Wall(Sprite):
    def __init__(self, coords):
        Sprite.__init__(self, 'graphics/wall.png', tileSize, tileSize, coords)
        
        self.coords = coords

    
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

def levelWallsAndFloor(array):
    for y, row in enumerate(array):
        for x, tile in enumerate(row):
            if tile == 1:
                wallList.append(Wall((x, y)))
            elif tile == 0:
                floorList.append(Floor((x, y)))


level = [[1] * 9] + [[1, 0, 0, 0, 0, 0, 0, 0, 1]] * 7 + [[1] * 9]

tileSize = 80
tilesX = tilesY = 9
global moveDir
moveDir = [0, 0]

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((tileSize * tilesX, tileSize * tilesY))

wallList = []
floorList = []
player = Player((4, 7))

levelWallsAndFloor(level)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moveDir[1] -= 1
            elif event.key == pygame.K_s:
                moveDir[1] += 1
            elif event.key == pygame.K_a:
                moveDir[0] -= 1
            elif event.key == pygame.K_d:
                moveDir[0] += 1
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moveDir[1] += 1
            elif event.key == pygame.K_s:
                moveDir[1] -= 1
            elif event.key == pygame.K_a:
                moveDir[0] += 1
            elif event.key == pygame.K_d:
                moveDir[0] -= 1
    
    for tile in wallList + floorList:
        tile.update()
        tile.draw()
    
    player.update()
    player.draw()
    
    pygame.display.update()
    clock.tick(64)