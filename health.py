import pygame
import config


class Health:
    def __init__(self, screen):
        self.screen = screen
        self.max_hp = 100
        self.current_hp = 100
        self.hp_bar_width = config.WIDTH
        self.hp_bar_height = 5

    def update(self):
        pygame.draw.rect(
            self.screen, config.RED, (0, 0, self.hp_bar_width, self.hp_bar_height)
        )
        ratio = (self.hp_bar_width * self.current_hp) / self.max_hp
        pygame.draw.rect(self.screen, config.GREEN, (0, 0, ratio, self.hp_bar_height))

    def damage(self, amount):
        if self.current_hp - amount >= 0:
            self.current_hp = self.current_hp - amount

    def is_dead(self):
        return self.current_hp <= 0
