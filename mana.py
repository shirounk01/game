import pygame
import config


class Mana:
    def __init__(self, screen):
        self.screen = screen
        self.max_mana = 100
        self.current_mana = 0
        self.mana_bar_width = config.WIDTH
        self.mana_bar_height = 5

    def update(self):
        pygame.draw.rect(
            self.screen,
            config.DARK_BLUE,
            (0, 5, self.mana_bar_width, self.mana_bar_height),
        )
        ratio = (self.mana_bar_width * self.current_mana) / self.max_mana
        pygame.draw.rect(self.screen, config.LIGHT_BLUE, (0, 6, ratio, 3))

    def recover(self, amount):
        if self.current_mana + amount <= self.max_mana:
            self.current_mana = self.current_mana + amount
