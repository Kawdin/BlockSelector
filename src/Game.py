import pygame

from .MyTypes import Sprite, Image, Level, Clock, Group, Entity, NewGame, RunGame
from .ents.Hero import Hero
from .ents.Items import Gun
from .ents.Bullet import Bullet
from .Shadow import Shadow
from .Map import Map

class Game(object):
    def __init__(self):
        pygame.init()
        self.mapa: Level = Map()
        self.tela = pygame.display.set_mode([514, 512])
        self.camera = pygame.Surface([1088, 1088])
        pygame.display.set_caption('BlockDeath')
        self.fps_clock: Clock = pygame.time.Clock()
        self.GAMELOOP: bool = True

    def new(self)-> NewGame:
        self.enemys_group: Group = pygame.sprite.Group()
        self.tiles_group: Group = pygame.sprite.Group()
        self.bullet_group: Group = pygame.sprite.Group()
        self.items_group: Group = pygame.sprite.Group()
        self.hero_group: Group = pygame.sprite.Group()
        self.shadow_group: Group = pygame.sprite.Group()
        self.shadow: Entity = Shadow(self.shadow_group)
        self.Hero: Player = Hero(self.shadow, self.hero_group)
        self.mapa.create_level(self.tiles_group, self.items_group, self.enemys_group)

    def run(self)-> RunGame:
        self.new()
        while self.GAMELOOP:
            self.fps_clock.tick(60)
            self.events()
            self.draw()
            self.update()
            self.colisions()

    def events(self)-> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAMELOOP = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and self.Hero.animations['GunPerma']:
                    self.Hero.animations['Gun'] = not self.Hero.animations['Gun']
                    if self.Hero.animations['Gun'] and self.Hero.animations['GunPerma']:
                        self.Hero.sprite_anim: Sprite = 'HeroGun'
                    else:
                        self.Hero.sprite_anim: Sprite = 'HeroRun'
            if event.type == pygame.MOUSEBUTTONDOWN and self.Hero.animations['Gun'] == True:
                Bullet(self.Hero.rect.x, self.Hero.rect.y, pygame.mouse.get_pos(), self.bullet_group)

    def draw(self)-> None:
        self.camera.fill([36, 48, 65])
        self.shadow_group.draw(self.camera)
        self.enemys_group.draw(self.camera)
        self.bullet_group.draw(self.camera)
        self.items_group.draw(self.camera)
        self.hero_group.draw(self.camera)
        self.tiles_group.draw(self.camera)
        self.tela.blit(self.camera, (0,0), [self.Hero.rect.x-257, self.Hero.rect.y-256, 514, 512])

    def update(self)-> None:
        self.shadow_group.update()
        self.enemys_group.update()
        self.bullet_group.update()
        self.items_group.update()
        self.hero_group.update()
        pygame.display.flip()

    def colisions(self)-> None:
        for item in pygame.sprite.spritecollide(self.Hero, self.items_group, True):
            if item.type == 'Gun':
                self.Hero.animations['Gun']: Sprite = item.Pickup()[1]
                self.Hero.animations[item.perma_item] = item.Pickup()[1]
                self.Hero.sprite_anim: Sprite = item.Pickup()[0]

        for tile in pygame.sprite.spritecollide(self.Hero, self.tiles_group, False):
            if(tile.rect.left == self.Hero.rect.right-4):
                self.Hero.rect.x -= 4
                self.Hero.la_x += 0
                self.Hero.lado_x = [True, False]
                self.Hero.lado_y = [True, True]

            if(tile.rect.right == self.Hero.rect.left+4):
                self.Hero.rect.x += 4
                self.Hero.la_x += 0
                self.Hero.lado_x = [False, True]
                self.Hero.lado_y = [True, True]

            if(tile.rect.bottom == self.Hero.rect.top+4):
                self.Hero.rect.y += 4
                self.Hero.la_y += 0
                self.Hero.lado_x = [True, True]
                self.Hero.lado_y = [True, False]

            if(tile.rect.top == self.Hero.rect.bottom-4):
                self.Hero.rect.y -= 4
                self.Hero.la_y += 0
                self.Hero.lado_x = [True, True]
                self.Hero.lado_y = [False, True]