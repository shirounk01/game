from typing import Any
import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 200
L_LIMIT, R_LIMIT = -30, 500
FPS = 60
UPDATE_INTERVAL = 60

RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, img, frame_count):
        super().__init__()
        self.img = pygame.image.load(img)
        self.frame_count = frame_count
        self.frame_width = self.img.get_width() / self.frame_count
        self.frame_height = self.img.get_height()
        self.current_frame = 0

    def get_frame(self, flip_frame=False):
        self.current_frame = (self.current_frame + 1) % self.frame_count
        frame = self.current_frame
        rect = pygame.Rect(
            frame * self.frame_width, 0, self.frame_width, self.frame_height
        )
        return pygame.transform.flip(self.img.subsurface(rect), flip_frame, False)

    def animation_status(self):
        return not self.current_frame == self.frame_count - 1

    def get_size(self):
        return (self.frame_width, self.frame_height)


class Health:
    def __init__(self, screen):
        self.screen = screen
        self.max_hp = 100
        self.current_hp = 100
        self.hp_bar_width = WIDTH
        self.hp_bar_height = 5

    def update(self):
        pygame.draw.rect(screen, RED, (0, 0, self.hp_bar_width, self.hp_bar_height))
        ratio = (self.hp_bar_width * self.current_hp) / self.max_hp
        pygame.draw.rect(screen, GREEN, (0, 0, ratio, self.hp_bar_height))

    def damage(self, amount):
        if self.current_hp - amount >= 0:
            self.current_hp = self.current_hp - amount

    def is_dead(self):
        return self.current_hp <= 0


class Player:
    def __init__(self, screen):
        self.idle = Sprite("sprites\player\Idle.png", 6)
        self.walk = Sprite("sprites\player\Walk.png", 8)
        self.run = Sprite("sprites\player\Run.png", 8)
        self.attack = [
            Sprite("sprites\player\Attack_1.png", 4),
            Sprite("sprites\player\Attack_2.png", 3),
        ]
        self.dead = Sprite("sprites\player\Dead.png", 3)
        self.screen = screen
        self.direction = False
        self.attack_lock = False
        self.x = 0
        self.y = HEIGHT - self.idle.get_size()[0]
        self.runnable_distance = 15
        self.sprite = self.idle.get_frame()
        self.last_updated = 0
        self.attack_type = random.randint(0, 1)
        self.hp = Health(self.screen)

    def update(self):
        if pygame.time.get_ticks() - self.last_updated >= UPDATE_INTERVAL:
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
                    ) and self.x - self.runnable_distance >= L_LIMIT:
                        self.x = self.x - self.runnable_distance
                        self.sprite = self.run.get_frame(self.direction)
                    elif self.x - self.runnable_distance // 2 >= L_LIMIT:
                        self.x = self.x - self.runnable_distance // 2
                        self.sprite = self.walk.get_frame(self.direction)
                if keys[pygame.K_RIGHT]:
                    self.direction = False
                    if (
                        keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]
                    ) and self.x + self.runnable_distance <= R_LIMIT:
                        self.x = self.x + self.runnable_distance
                        self.sprite = self.run.get_frame(self.direction)
                    elif self.x + self.runnable_distance // 2 <= R_LIMIT:
                        self.x = self.x + self.runnable_distance // 2
                        self.sprite = self.walk.get_frame(self.direction)

            if keys[pygame.K_x] or self.attack_lock:
                self.attack_lock = self.attack[self.attack_type].animation_status()
                self.sprite = self.attack[self.attack_type].get_frame(self.direction)
                if not self.attack_lock:
                    self.attack_type = random.randint(0, 1)

        rect = (self.x, self.y)
        if pygame.key.get_pressed()[pygame.K_z]:
            self.hp.damage(10)
        self.hp.update()
        screen.blit(self.sprite, rect)
        if not self.dead.animation_status():
            screen.fill(RED)
            global running
            running = False


player = Player(screen)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((44, 44, 44))

    player.update()
    pygame.display.flip()
    clock.tick(FPS)

pygame.time.delay(1000)

pygame.quit()
sys.exit()
