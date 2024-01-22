from typing import Any
import pygame
import random

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


class Helth:
    def __init__(self, screen):
        self.screen = screen
        self.max_hp = 100

    def update(self):
        pass


class Player:
    def __init__(self, screen):
        self.idle = Sprite("sprites\player\Idle.png", 6)
        self.walk = Sprite("sprites\player\Walk.png", 8)
        self.run = Sprite("sprites\player\Run.png", 8)
        self.attack = [
            Sprite("sprites\player\Attack_1.png", 4),
            Sprite("sprites\player\Attack_2.png", 3),
        ]
        self.screen = screen
        self.direction = False
        self.attack_lock = False
        self.x = 0
        self.y = HEIGHT - self.idle.get_size()[0]
        self.runnable_distance = 15
        self.sprite = self.idle.get_frame()
        self.last_updated = 0
        self.attack_type = random.randint(0, 1)

    def update(self):
        if pygame.time.get_ticks() - self.last_updated >= UPDATE_INTERVAL:
            self.last_updated = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            self.sprite = self.idle.get_frame(self.direction)
            if not self.attack_lock:
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
        screen.blit(self.sprite, rect)


player = Player(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    screen.fill((44, 44, 44))

    player.update()
    pygame.display.flip()
    clock.tick(FPS)
