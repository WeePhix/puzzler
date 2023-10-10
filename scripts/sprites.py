import pygame

images = {'wall' : [pygame.image.load("../graphics/basic/wall.png")],
          'floor' : [pygame.image.load("../graphics/basic/floor")],
          'cracked' : [pygame.image.load("../graphics/basic/cracked0.png"), pygame.image.load("../graphics/basic/cracked1.png"), pygame.image.load("../graphics/basic/cracked2.png")],
          'crate' : [pygame.image.load("../graphics/basic/crate.png")],
          'goal' : [pygame.image.load('../graphics/basic/goal.png')],
          'button' : {'red' : [pygame.image.load('../graphics/buttons/red0.png'), pygame.image.load('../graphics/buttons/red1.png')],
                      'blue' : [pygame.image.load('../graphics/buttons/blue0.png'), pygame.image.load('../graphics/buttons/blue1.png')],
                      'green' : [pygame.image.load('../graphics/buttons/green0.png'), pygame.image.load('../graphics/buttons/green1.png')]},
          'lever' : {'red' : [pygame.image.load('../graphics/levers/red0.png'), pygame.image.load('../graphics/levers/red1.png')],
                      'blue' : [pygame.image.load('../graphics/levers/blue0.png'), pygame.image.load('../graphics/levers/blue1.png')],
                      'green' : [pygame.image.load('../graphics/levers/green0.png'), pygame.image.load('../graphics/levers/green1.png')]},
          'door' : {'red' : [pygame.image.load('../graphics/doors/red0.png'), pygame.image.load('../graphics/doors/red1.png')],
                      'blue' : [pygame.image.load('../graphics/doors/blue0.png'), pygame.image.load('../graphics/doors/blue1.png')],
                      'green' : [pygame.image.load('../graphics/doors/green0.png'), pygame.image.load('../graphics/doors/green1.png')]},
          'player' : [[], [], [], []]}

class Sprite():
    def __init__(self, game, coords) -> None:
        self.game = game
        
        self.images = images
        self.coords = coords
        self.animType = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = ((coords[0] + 0.5) * game.tileScreenSize, (coords[1] + 0.5) * game.tileScreenSize)
        self.methods = [self.draw()]
        
        if self.__class__.__name__ == 'Wall':
            self.type = 'wall'
            dimensions = (game.tileScreenSize, game.tileScreenSize)
        elif self.__class__.__name__ == 'Floor':
            self.type = 'floor'
            dimensions = (game.tileScreenSize, game.tileScreenSize)
        elif self.__class__.__name__ == 'Crate':
            self.type = 'crate'
            dimensions = (game.tileScreenSize * 7 / 8, game.tileScreenSize * 7 / 8)
        elif self.__class__.__name__ == 'Button':
            self.type = 'button'
            self.animType = 1
            dimensions = (game.tileScreenSize * 7 / 8, game.tileScreenSize * 7 / 8)
        elif self.__class__.__name__ == 'Lever':
            self.type = 'lever'
            self.animType = 1
            dimensions = (game.tileScreenSize * 7 / 8, game.tileScreenSize * 7 / 8)
        elif self.__class__.__name__ == 'Door':
            self.type = 'door'
            self.animType = 1
            dimensions = (game.tileScreenSize, game.tileScreenSize)
        elif self.__class__.__name__ == 'Player':
            self.type = 'player'
            self.animType = 2
            dimensions = (game.tileScreenSize * 3 / 4, game.tileScreenSize * 3 / 4)
        elif self.__class__.__name__ == 'Goal':
            self.type = 'goal'
            dimensions = (game.tileScreenSize, game.tileScreenSize)
        
        for i in range(len(self.images)):
            if type(self.images) == type([]):
                for j in range(len(self.images)):
                    self.images[i][j] = pygame.transform.scale(self.image[i][j], dimensions).convert_alpha()
            else:
                self.images[i] = pygame.transform.scale(self.image[i][j], dimensions).convert_alpha()
    
    def animatePlayer(self):
        pass
    
    def draw(self):
        self.game.screen.blit(self.image, self.rect)
    
    def playerMove(self, moveDir):
        pass
        
    def playerCheckMove(self):
        self.moveAttempt = [False, False, False, False]
        
        surrTiles = {'NW' : self.game.tileset[self.coords[1] - 1][self.coords[0] - 1], 'N' : self.game.tileset[self.coords[1] - 1][self.coords[0]], 'NE' : self.game.tileset[self.coords[1] - 1][self.coords[0] + 1],
                     'W' : self.game.tileset[self.coords[1]][self.coords[0] - 1], '0' : self.game.tileset[self.coords[1]][self.coords[0]], 'W' : self.game.tileset[self.coords[1]][self.coords[0] + 1],
                     'SW' : self.game.tileset[self.coords[1] + 1][self.coords[0] - 1], 'S' : self.game.tileset[self.coords[1] + 1][self.coords[0]], 'SE' : self.game.tileset[self.coords[1] + 1][self.coords[0] + 1]}
        
        for input in self.game.inputs:
            self.moveAttempt[0] = (self.moveAttempt[0] or input == 'N') and (tile.playerStop == False for tile in surrTiles['N'])
            self.moveAttempt[1] = (self.moveAttempt[1] or input == 'E') and (tile.playerStop == False for tile in surrTiles['E'])
            self.moveAttempt[2] = (self.moveAttempt[2] or input == 'S') and (tile.playerStop == False for tile in surrTiles['S'])
            self.moveAttempt[3] = (self.moveAttempt[3] or input == 'W') and (tile.playerStop == False for tile in surrTiles['W'])
        
        if self.moveAttempt[0] and self.moveAttempt[2]: self.moveAttempt[0]  = self.moveAttempt[2] = False
        if self.moveAttempt[1] and self.moveAttempt[3]: self.moveAttempt[1]  = self.moveAttempt[3] = False
        



class Wall(Sprite):
    def __init__(self, game, coords) -> None:
        super().__init__(game, coords, game.tileScreenSize,)