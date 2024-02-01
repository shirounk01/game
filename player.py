import pygame
import random
import config
from sprite import Sprite
from health import Health
from mana import Mana

pygame.mixer.init()


class Player:
    def __init__(self, screen):
        self.idle = Sprite("sprites\player\Idle.png", 6)
        self.walk = Sprite("sprites\player\Walk.png", 8)
        self.run = Sprite("sprites\player\Run.png", 8)
        self.attack = [
            Sprite("sprites\player\Attack_1.png", 4),
            Sprite("sprites\player\Attack_2.png", 3),
        ]
        self.die = Sprite("sprites\player\Dead.png", 3)
        self.attack_sound = [
            pygame.mixer.Sound("audio\player\Attack_1.wav"),
            pygame.mixer.Sound("audio\player\Attack_2.wav"),
        ]
        self.power_up = pygame.mixer.Sound("audio\player\Power_up.wav")
        self.screen = screen
        self.direction = False
        self.attack_lock = False
        self.sprite = self.idle.get_frame()
        self.x = 0
        self.y = config.HEIGHT - self.sprite.get_width()
        self.last_updated = 0
        self.attack_type = random.randint(0, 1)
        self.hp = Health(self.screen)
        self.has_died = False
        self.mana = Mana(self.screen)

    def update(self, enemy):
        # update the sprites after a set interval
        if pygame.time.get_ticks() - self.last_updated >= config.UPDATE_INTERVAL:
            self.last_updated = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            # when not doing anything, become idle
            self.sprite = self.idle.get_frame(self.direction)

            if self.hp.is_dead():
                self.sprite = self.die.get_frame(self.direction)
            elif not self.attack_lock:
                # move left
                if keys[pygame.K_LEFT]:
                    self.direction = True
                    # sprint when either shifts are held down, keep the player inside the window boundaries
                    if (
                        keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]
                    ) and self.x - config.RUNNABLE_DISTANCE >= config.L_LIMIT:
                        self.x = self.x - config.RUNNABLE_DISTANCE
                        self.sprite = self.run.get_frame(self.direction)
                    elif self.x - config.RUNNABLE_DISTANCE // 2 >= config.L_LIMIT:
                        self.x = self.x - config.RUNNABLE_DISTANCE // 2
                        self.sprite = self.walk.get_frame(self.direction)
                # move right
                if keys[pygame.K_RIGHT]:
                    self.direction = False
                    # sprint when either shifts are held down, keep the player inside the window boundaries
                    if (
                        keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]
                    ) and self.x + config.RUNNABLE_DISTANCE <= config.R_LIMIT:
                        self.x = self.x + config.RUNNABLE_DISTANCE
                        self.sprite = self.run.get_frame(self.direction)
                    elif self.x + config.RUNNABLE_DISTANCE // 2 <= config.R_LIMIT:
                        self.x = self.x + config.RUNNABLE_DISTANCE // 2
                        self.sprite = self.walk.get_frame(self.direction)
            # when Z is pressed, attack
            if keys[pygame.K_z] or self.attack_lock:
                # when the animation is performed and an enemy is within reach, damage the enemy
                # otherwise just play the animation and sound effect
                try:
                    if (
                        not self.attack_lock
                        and self.attack[self.attack_type].check_animation_status()
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
                self.attack_lock = self.attack[
                    self.attack_type
                ].check_animation_status()
                self.sprite = self.attack[self.attack_type].get_frame(self.direction)
                # randomly pick the next type of attack to be performed
                if not self.attack_lock:
                    self.attack_type = random.randint(0, 1)
            # when X is pressed and the mana bar is full, gain the power up
            if keys[pygame.K_x] and self.mana.is_full():
                self.power_up.play()
                self.mana.set_power_up()
                self.hp.regenerate_over_time(50)

        rect = (self.x, self.y)

        self.mana.update()
        self.hp.update()
        self.screen.blit(self.sprite, rect)
        # after the death animation, make the screen red
        if not self.die.check_animation_status():
            self.screen.fill(config.RED)
            self.has_died = True

    # check whether the player is already dead or not
    def is_dead(self):
        return self.has_died

    # get the X coordinate of the center of the player
    def get_position(self):
        return self.x + self.sprite.get_width() // 2

    # damage the player by a given amount
    def get_damaged(self, value):
        if not self.mana.has_power_up():
            self.hp.damage(value)

    # check if the player is
    def is_attacking(self):
        return self.attack_lock
