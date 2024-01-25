import pygame
import config
import random
from sprite import Sprite
from health import Health


class Enemy:
    def __init__(self, screen, x):
        self.idle = Sprite("sprites\enemy\Idle.png", 6)
        self.walk = Sprite("sprites\enemy\Walk.png", 7)
        self.attack = Sprite("sprites\enemy\Attack.png", 11)
        self.dead = Sprite("sprites\enemy\Dead.png", 5)
        self.screen = screen
        self.direction = False
        self.x = x
        self.y = config.HEIGHT - self.walk.get_size()[0]
        self.runnable_distance = config.RUNNABLE_DISTANCE
        self.sprite = self.walk.get_frame()
        self.last_updated = 0
        self.attack_lock = False
        self.hp = Health(
            self.screen,
            x=self.x,
            y=self.y,
            width=self.sprite.get_width() // 2,
            sprite_width=self.sprite.get_width(),
        )
        self.has_died = False

    def update(self, player):
        if pygame.time.get_ticks() - self.last_updated >= config.UPDATE_INTERVAL:
            self.last_updated = pygame.time.get_ticks()
            if self.is_in_attack_range(player.get_position()):
                self.sprite = self.idle.get_frame(self.direction)
            else:
                self.direction = self.check_position(player.get_position())
                self.sprite = self.walk.get_frame(self.direction)
                if self.direction == True:
                    self.x -= config.RUNNABLE_DISTANCE // 4
                else:
                    self.x += config.RUNNABLE_DISTANCE // 4
                self.hp.update_x(self.x, False)
            if self.can_attack(player.get_position()) or self.attack_lock:
                self.attack_lock = self.attack.animation_status()
                self.sprite = self.attack.get_frame(self.direction)
                if not self.attack_lock:
                    self.hp.damage(config.DAMAGE_VALUE // 2)
                    player.get_damaged(config.DAMAGE_VALUE)
            if self.hp.is_dead() or self.has_died:
                self.has_died = self.dead.animation_status()
                self.sprite = self.dead.get_frame(self.direction)

        rect = (self.x, self.y)

        self.hp.update()
        self.screen.blit(self.sprite, rect)

    def check_position(self, x):
        return self.x + self.sprite.get_width() // 2 > x

    def is_in_attack_range(self, position):
        return (
            abs(self.x + self.sprite.get_width() // 2 - position) <= config.ATTACK_RANGE
        )

    def can_attack(self, position):
        return (
            abs(self.x + self.sprite.get_width() // 2 - position)
            <= self.sprite.get_width() // 4
        )

    def check_death_animation_status(self):
        return self.dead.animation_status()

    def is_in_vulnerable_range(self, position):
        return (
            abs(self.x + self.sprite.get_width() // 2 - position)
            <= self.sprite.get_width() // 2
        )

    def get_damaged(self, value):
        self.hp.damage(value)
