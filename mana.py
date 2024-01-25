import pygame
import config


class Mana:
    def __init__(self, screen):
        self.screen = screen
        self.max_mana = 100
        self.current_mana = 0
        self.mana_bar_width = config.WIDTH
        self.mana_bar_height = 7
        self.mana_bar_color = config.LIGHT_BLUE
        self.power_up = False
        self.last_updated = 0

    def update(self):
        if pygame.time.get_ticks() - self.last_updated >= config.UPDATE_INTERVAL:
            self.last_updated = pygame.time.get_ticks()
            if self.power_up:
                self.current_mana -= 1
                self.mana_bar_color = config.YELLOW
                if self.current_mana == 0:
                    self.power_up = False
                    self.mana_bar_color = config.LIGHT_BLUE
        pygame.draw.rect(
            self.screen,
            config.DARK_BLUE,
            (0, 5, self.mana_bar_width, self.mana_bar_height),
        )
        ratio = (self.mana_bar_width * self.current_mana) / self.max_mana
        pygame.draw.rect(self.screen, self.mana_bar_color, (0, 6, ratio, 4))

    def recover(self, amount):
        if self.current_mana + amount <= self.max_mana:
            self.current_mana = self.current_mana + amount

    def is_full(self):
        return self.current_mana == self.max_mana

    def set_power_up(self):
        self.power_up = True

    def has_power_up(self):
        return self.power_up
