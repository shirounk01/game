import pygame
import random
import config
from sprite import Sprite
from health import Health
from mana import Mana


class Player:
    def __init__(self, screen):
        self.idle = Sprite("sprites\player\Idle.png", 6)
        self.walk = Sprite("sprites\player\Walk.png", 8)
        self.run = Sprite("sprites\player\Run.png", 8)
        self.attack = [
            Sprite("sprites\player\Attack_1.png", 4),
            Sprite("sprites\player\Attack_2.png", 3),
        ]
        self.dead = Sprite("sprites\player\Dead.png", 3)
        self.screen = screen
        self.direction = False
        self.attack_lock = False
        self.x = 0
        self.y = config.HEIGHT - self.idle.get_size()[0]
        self.runnable_distance = 15
        self.sprite = self.idle.get_frame()
        self.last_updated = 0
        self.attack_type = random.randint(0, 1)
        self.hp = Health(self.screen)
        self.has_died = False
        self.mana = Mana(self.screen)

    def is_dead(self):
        return self.has_died

    def update(self):
        if pygame.time.get_ticks() - self.last_updated >= config.UPDATE_INTERVAL:
            self.last_updated = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            self.sprite = self.idle.get_frame(self.direction)
            if self.hp.is_dead():
                self.sprite = self.dead.get_frame(self.direction)
            elif not self.attack_lock:
                if keys[pygame.K_LEFT]:
                    self.direction = True
                    if (
                        keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]
                    ) and self.x - self.runnable_distance >= config.L_LIMIT:
                        self.x = self.x - self.runnable_distance
                        self.sprite = self.run.get_frame(self.direction)
                    elif self.x - self.runnable_distance // 2 >= config.L_LIMIT:
                        self.x = self.x - self.runnable_distance // 2
                        self.sprite = self.walk.get_frame(self.direction)
                if keys[pygame.K_RIGHT]:
                    self.direction = False
                    if (
                        keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]
                    ) and self.x + self.runnable_distance <= config.R_LIMIT:
                        self.x = self.x + self.runnable_distance
                        self.sprite = self.run.get_frame(self.direction)
                    elif self.x + self.runnable_distance // 2 <= config.R_LIMIT:
                        self.x = self.x + self.runnable_distance // 2
                        self.sprite = self.walk.get_frame(self.direction)

            if keys[pygame.K_x] or self.attack_lock:
                self.attack_lock = self.attack[self.attack_type].animation_status()
                self.sprite = self.attack[self.attack_type].get_frame(self.direction)
                if not self.attack_lock:
                    self.attack_type = random.randint(0, 1)

        rect = (self.x, self.y)
        if pygame.key.get_pressed()[pygame.K_z]:
            self.hp.damage(10)
        if pygame.key.get_pressed()[pygame.K_x]:
            self.mana.recover(10)
        self.hp.update()
        self.mana.update()
        self.screen.blit(self.sprite, rect)
        if not self.dead.animation_status():
            self.screen.fill(config.RED)
            self.has_died = True
