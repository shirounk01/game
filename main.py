from typing import Any
import pygame
import sys
import config
from player import Player
from enemy import Enemy

pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Kazan no Hibana")

clock = pygame.time.Clock()
bg_image = pygame.transform.scale_by(
    pygame.image.load("sprites\game\Background.jpg"), config.ZOOM
)
bg_music = pygame.mixer.music.load("audio\game\Background.ogg")
pygame.mixer.music.play(-1)

player = Player(screen)
enemies = []

while not player.is_dead():
    for event in pygame.event.get():
        # exit game when the X button is pressed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # spawn an enemy when a left click is registered
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            enemies.append(Enemy(screen=screen, x=event.pos[0]))

    screen.blit(bg_image, (0, 0))

    # loop through the enemies and create the interaction between them and the player
    for enemy in enemies:
        if enemy.has_died and not enemy.check_death_animation_status():
            enemies.remove(enemy)
            del enemy
        else:
            enemy.update(player)
            player.update(enemy)
    else:
        player.update(None)

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.time.delay(1000)

pygame.quit()
sys.exit()
