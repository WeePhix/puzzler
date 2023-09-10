import pygame
from sys import exit


tileSize = 80
tilesX = tilesY = 9


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('puzzler/graphics/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        self.rect = self.image.get_rect()
        
        self.diff = [(-tileSize, -tileSize), (0, -tileSize), (tileSize, -tileSize), (tileSize, 0), (tileSize, tileSize), (0, tileSize), (-tileSize, tileSize), (-tileSize, 0)]
        self.moveDir = [0, 0]
        self.moving = False
        
    def eventHandler(self, events):
        print(f'player.eventHandler: moveDir = {self.moveDir}')
        self.moveDir = list(self.moveDir)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.moveDir[1] -= 1
                if event.key == pygame.K_s:
                    self.moveDir[1] += 1
                if event.key == pygame.K_a:
                    self.moveDir[0] -= 1
                if event.key == pygame.K_d:
                    self.moveDir[0] += 1
    
    def checkMovementOptions(self):
        print(f'player.checkMovementOptions: moveDir = {self.moveDir}')
        
        i = 0
        surr = ['empty'] * 8
        for tile in pygame.sprite.Group.sprites(tileGroup):
            if (tile.rect.center[0] - self.rect.center[0], tile.rect.center[1] - self.rect.center[1]) == self.diff[i]:
                surr.append(tile)
                i += 1
        
        if surr == ['empty'] * 8:
            return 0
        
        if (surr[1] == 'full' and self.moveDir[1] == -1) or (surr[5] == 'full' and self.moveDir[1] == 1):
            self.moveDir[1] = 0
            print('blocked movement vertically')
        if (surr[3] == 'full' and self.moveDir[0] == 1) or (surr[7] == 'full' and self.moveDir[0] == -1):
            self.moveDir[0] = 0
            print('blocked movement horizontally')
            
        if (surr[1] == 'pathNS' and self.moveDir == [0, -1]) or (surr[5] == 'pathNS' and self.moveDir == [0, 1]):
            self.moveDir[1] *= 2
        elif (surr[3] == 'pathWE' and self.moveDir == [1, 0]) or (surr[7] == 'pathWE' and self.moveDir == [-1, 0]):
            self.moveDir[0] *= 2
        # ADD CORNER PATH CHECKS!!!!
        else:
            self.moveDir = (0, 0)
            print('blocked movement')
        
    def move(self):
        print(f'player.move: moveDir = {self.moveDir}')
        self.moving = True
        for _ in range(max(self.moveDir) * 16):            
            screen.fill('black')
            tileGroup.draw(screen)
            player.draw(screen)
            pygame.time.delay(1000//16)
        self.moveDir = [0, 0]
        self.moving = False
    
    def update(self, events):
        if self.moving:
            return 0
        
        self.eventHandler(events)
        self.checkMovementOptions()
        self.move()
        



class Tile(pygame.sprite.Sprite):
    def __init__(self, type, coords):
        super().__init__
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('puzzler/graphics/' + type + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tileSize, tileSize))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = coords[0] * tileSize, coords[1] * tileSize
        
        self.type = type




def levelToTileTypes(level):
    for y in range(tilesY):
        for x in range(tilesX):
            if type(level[y][x]) == int:
                if level[y][x] >= len(tileTypes):
                    return 'ERROR: incorrect tile index!'
                level[y][x] = tileTypes[level[y][x]]
    return level


def tileArrayToGroup(array, group):
    for y in range(len(array)):
        for x in range(len(array[y])):
            if array[y][x] != 'none':
                group.add(Tile(array[y][x], (x, y)))


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((tileSize * tilesX, tileSize * tilesY))

# explanation:         |X|       |\        |/        \|        /|        ||        =
tileTypes = ['none', 'full', 'pathNE', 'pathSE', 'pathSW', 'pathNW', 'pathNS', 'pathWE']

level = [[1] * 9] + [[1, 0, 0, 0, 0, 0, 0, 0, 1]] * 7 + [[1] * 9]

level = levelToTileTypes(level)

tileGroup = pygame.sprite.Group()

player = pygame.sprite.GroupSingle(Player())
player.sprite.rect.center = (tilesX * tileSize / 2, tilesY * tileSize / 2)

tileArrayToGroup(level, tileGroup)

while True:
    screen.fill('black')
    tileGroup.draw(screen)
    player.draw(screen)
    
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:
            events.append(event)
    player.update(events)
    
    pygame.display.update()
    clock.tick(32)