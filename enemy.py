import pygame
import config
from sprite import Sprite
from health import Health


class Enemy:
    def __init__(self, screen):
        # self.idle = Sprite("sprites\player\Idle.png", 6)
        self.walk = Sprite("sprites\enemy\Walk.png", 7)
        self.screen = screen
        self.direction = False
        self.x = 200
        self.y = config.HEIGHT - self.walk.get_size()[0]
        self.runnable_distance = config.RUNNABLE_DISTANCE
        self.sprite = self.walk.get_frame()
        self.last_updated = 0
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
            self.direction = player.check_position(
                self.x + self.sprite.get_width() // 2
            )
            self.sprite = self.walk.get_frame(self.direction)
            if self.direction == True:
                self.x -= config.RUNNABLE_DISTANCE // 4
            else:
                self.x += config.RUNNABLE_DISTANCE // 4
            self.hp.update_x(self.x, False)

        rect = (self.x, self.y)

        self.hp.update()
        self.screen.blit(self.sprite, rect)
