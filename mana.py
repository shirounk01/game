import pygame
import config


class Mana:
    def __init__(self, screen):
        self.screen = screen
        self.max_mana = 100
        self.current_mana = 0
        self.mana_bar_width = config.WIDTH
        self.mana_bar_height = 5
        self.power_up = False

    def update(self):
        if self.power_up:
            self.current_mana -= 0.25
            pygame.draw.rect(
                self.screen, (255, 0, 0, 128), (0, 0, config.WIDTH, config.HEIGHT)
            )
            if self.current_mana == 0:
                self.power_up = False
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

    def is_full(self):
        return self.current_mana == self.max_mana

    def set_power_up(self):
        self.power_up = True

    def has_power_up(self):
        return self.power_up
