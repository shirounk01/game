import pygame
import config
import random
from sprite import Sprite
from health import Health

pygame.mixer.init()


class Enemy:
    def __init__(self, screen, x):
        self.idle = Sprite("sprites\enemy\Idle.png", 6)
        self.walk = Sprite("sprites\enemy\Walk.png", 7)
        self.attack = Sprite("sprites\enemy\Attack.png", 11)
        self.die = Sprite("sprites\enemy\Dead.png", 5)
        self.attack_sound = [
            pygame.mixer.Sound("audio\enemy\Attack_1.wav"),
            pygame.mixer.Sound("audio\enemy\Attack_2.wav"),
        ]
        self.death_sound = pygame.mixer.Sound("audio\enemy\Death.wav")
        self.screen = screen
        self.direction = False
        self.x = x - self.walk.get_size()[0] // 2
        self.y = config.HEIGHT - self.walk.get_size()[0]
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
        # update the sprites after a set interval
        if pygame.time.get_ticks() - self.last_updated >= config.UPDATE_INTERVAL:
            self.last_updated = pygame.time.get_ticks()
            # when the player is close, become idle
            if self.is_in_attack_range(player.get_position()):
                self.sprite = self.idle.get_frame(self.direction)
            else:  # otherwise move towards the player
                self.direction = self.check_position(player.get_position())
                self.sprite = self.walk.get_frame(self.direction)
                if self.direction == True:
                    self.x -= config.RUNNABLE_DISTANCE // 4
                else:
                    self.x += config.RUNNABLE_DISTANCE // 4
                self.hp.update_x(self.x, False)
            # when the player is within reach, attack
            if self.can_attack(player.get_position()) or self.attack_lock:
                if not self.attack_lock and self.attack.check_animation_status():
                    self.attack_sound[random.randint(0, 1)].play()
                self.attack_lock = self.attack.check_animation_status()
                self.sprite = self.attack.get_frame(self.direction)
                if not self.attack_lock and self.can_attack(player.get_position()):
                    self.hp.damage(config.DAMAGE_VALUE // 2)
                    player.get_damaged(config.DAMAGE_VALUE)
            # when hp reaches 0, die
            if self.hp.is_dead() or self.has_died:
                if self.die.check_animation_status() and not self.has_died:
                    self.death_sound.play()
                self.has_died = self.die.check_animation_status()
                self.sprite = self.die.get_frame(self.direction)

        rect = (self.x, self.y)

        self.hp.update(self.x + self.sprite.get_width() // 2)
        self.screen.blit(self.sprite, rect)

    # get the direction: left -> True, right -> False
    def check_position(self, x):
        return self.x + self.sprite.get_width() // 2 > x

    # check whether the enemy becomes idle or not
    def is_in_attack_range(self, position):
        return (
            abs(self.x + self.sprite.get_width() // 2 - position) <= config.ATTACK_RANGE
        )

    # check whether the enemy can attack the player at the given position or not
    def can_attack(self, position):
        return (
            abs(self.x + self.sprite.get_width() // 2 - position)
            <= self.sprite.get_width() // 3
        )

    # check if the death animation is ongoing: ongoing -> True, finished -> False
    def check_death_animation_status(self):
        return self.die.check_animation_status()

    # check if the enemy can be attacked by the player
    def is_in_vulnerable_range(self, position):
        return (
            abs(self.x + self.sprite.get_width() // 2 - position)
            <= self.sprite.get_width() // 2
        )

    # change the value of the hp bar based on the incoming damage
    def get_damaged(self, value):
        self.hp.damage(value)
