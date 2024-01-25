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
enemies = [Enemy(screen)]

while not player.is_dead():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(config.GREY)

    for enemy in enemies:
        if enemy.has_died and not enemy.check_death_animation_status():
            enemies.remove(enemy)
            del enemy
        else:
            player.update(enemy)
            enemy.update(player)
    else:
        player.update(None)
    pygame.display.flip()
    clock.tick(config.FPS)

pygame.time.delay(1000)

pygame.quit()
sys.exit()
