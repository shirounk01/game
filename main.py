from typing import Any
import pygame
import sys
import config
from player import Player

pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

player = Player(screen)

while not player.is_dead():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((44, 44, 44))

    player.update()
    pygame.display.flip()
    clock.tick(config.FPS)

pygame.time.delay(1000)

pygame.quit()
sys.exit()
