from typing import Any
import pygame
import sys
import config
from player import Player
from enemy import Enemy

pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

player = Player(screen)
enemy = Enemy(screen)

while not player.is_dead():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(config.GREY)

    player.update(enemy)
    enemy.update(player)
    pygame.display.flip()
    clock.tick(config.FPS)

pygame.time.delay(1000)

pygame.quit()
sys.exit()
