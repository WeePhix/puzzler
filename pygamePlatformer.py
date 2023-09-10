import pygame
from sys import exit


tileSize = 80
tilesX = tilesY = 9
global moveDir
moveDir = [0, 0]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        
        self.moving = False
        self.surrWalls = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.moveFreedom = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.animCounter = 0
        self.pixelCounter = 0
        
    def checkMoveOptions(self, walls):
        self.surrWalls = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        moveFreedom = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        
        for wall in pygame.sprite.Group.sprites(walls):
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
                    self.moveFreedom[x][y] = not(self.surrWalls[y][1] or self.surrWalls[1][x] or self.surrWalls[x][y])
                elif self.surrWalls[y][x] == 0:
                    self.moveFreedom[y][x] = 1
        
    def defineMoveDir(self):
        moveVec = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        moveVec[moveDir[1] + 1][moveDir[0] + 1] = 1
        
        moveVec[0][1] = moveVec[0][0] or moveVec[0][1] or moveVec[0][2]
        moveVec[2][1] = moveVec[2][0] or moveVec[2][1] or moveVec[2][2]
        moveVec[1][0] = moveVec[0][0] or moveVec[1][0] or moveVec[2][0]
        moveVec[1][2] = moveVec[0][2] or moveVec[1][2] or moveVec[2][2]
        
        for x in [0, 2, 1]:
            if self.moving: break
            for y in [0, 2, 1]:
                if moveVec[y][x] and self.moveFreedom[y][x]:
                    self.direction = (x-1, y-1)
                    self.moving = True
                    break

    def move(self):
        self.animCounter += 1
        self.pixelCounter += 1
        if self.animCounter >= 2:
            self.animCounter = 0
            self.rect.x += self.direction * tileSize / 16
        
        if self.pixelCounter == 16:
            self.moving = False
    
    def update(self):
        self.checkMoveOptions(pygame.sprite.Group.sprites(wallGroup))
        self.defineMoveDir()
        if self.moving: self.move()

class Floor(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('graphics/floor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = coords[0] * tileSize, coords[1] * tileSize
        
        self.coords = coords


class Wall(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('graphics/wall.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = coords[0] * tileSize, coords[1] * tileSize
        
        self.coords = coords

    
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

def levelWallsAndFloor(array):
    for y, row in enumerate(array):
        for x, tile in enumerate(row):
            if tile == 1:
                wallGroup.add(Wall((x, y)))
            elif tile == 0:
                floorGroup.add(Floor((x, y)))


level = [[1] * 9] + [[1, 0, 0, 0, 0, 0, 0, 0, 1]] * 7 + [[1] * 9]

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((tileSize * tilesX, tileSize * tilesY))

wallGroup = pygame.sprite.Group()
floorGroup = pygame.sprite.Group()
player = pygame.sprite.GroupSingle(Player())

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
    
    player.update()
    wallGroup.draw(screen)
    floorGroup.draw(screen)
    player.draw(screen)
    
    pygame.display.update()
    clock.tick(64)