import pygame
import config


class Health:
    def __init__(self, screen, x=0, y=0, width=config.WIDTH, sprite_width=config.WIDTH):
        self.hp_bar_height = 5
        self.max_hp = 100
        self.screen = screen
        self.current_hp = 100
        self.hp_bar_width = width
        self.sprite_width = sprite_width
        self.x = x
        self.y = y

    def update(self):
        # compute the percentage of hp left
        ratio = (self.hp_bar_width * self.current_hp) / self.max_hp

        red_rect = pygame.Rect(self.x, self.y, self.hp_bar_width, self.hp_bar_height)
        red_rect.centerx = self.x + self.sprite_width // 2
        green_rect = pygame.Rect(self.x, self.y, ratio, self.hp_bar_height)
        green_rect.topleft = red_rect.topleft

        pygame.draw.rect(
            self.screen,
            config.RED,
            red_rect,
        )
        pygame.draw.rect(
            self.screen,
            config.GREEN,
            green_rect,
        )

    def damage(self, amount):
        if self.current_hp - amount >= 0:
            self.current_hp = self.current_hp - amount

    def is_dead(self):
        return self.current_hp <= 0

    def update_x(self, x, direction):
        self.x = x
