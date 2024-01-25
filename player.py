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
        self.attack_sound = [
            pygame.mixer.Sound("audio\player\Attack_1.wav"),
            pygame.mixer.Sound("audio\player\Attack_2.wav"),
        ]
        self.dead = Sprite("sprites\player\Dead.png", 3)
        self.power_up = pygame.mixer.Sound("audio\player\Power_up.wav")
        self.screen = screen
        self.direction = False
        self.attack_lock = False
        self.x = 0
        self.y = config.HEIGHT - self.idle.get_size()[0]
        self.runnable_distance = config.RUNNABLE_DISTANCE
        self.sprite = self.idle.get_frame()
        self.last_updated = 0
        self.attack_type = random.randint(0, 1)
        self.hp = Health(self.screen)
        self.has_died = False
        self.mana = Mana(self.screen)

    def is_dead(self):
        return self.has_died

    def update(self, enemy):
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

            if keys[pygame.K_z] or self.attack_lock:
                try:
                    if (
                        not self.attack_lock
                        and self.attack[self.attack_type].animation_status()
                    ):
                        self.attack_sound[self.attack_type].play()
                        if enemy.is_in_vulnerable_range(self.get_position()):
                            damage_value = (
                                config.DAMAGE_VALUE
                                if not self.mana.has_power_up()
                                else config.DAMAGE_VALUE * 2
                            )
                            enemy.get_damaged(damage_value)
                            if not self.mana.has_power_up():
                                self.mana.recover(config.MANA_RECOVER_VALUE)
                except:
                    pass
                self.attack_lock = self.attack[self.attack_type].animation_status()
                self.sprite = self.attack[self.attack_type].get_frame(self.direction)
                if not self.attack_lock:
                    self.attack_type = random.randint(0, 1)

            if keys[pygame.K_x] and self.mana.is_full():
                self.power_up.play()
                self.mana.set_power_up()

        rect = (self.x, self.y)
        self.mana.update()
        self.hp.update()
        self.screen.blit(self.sprite, rect)
        if not self.dead.animation_status():
            self.screen.fill(config.RED)
            self.has_died = True

    def get_position(self):
        return self.x + self.sprite.get_width() // 2

    def get_damaged(self, value):
        if not self.mana.has_power_up():
            self.hp.damage(value)

    def is_attacking(self):
        return self.attack_lock
