import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
FPS = 60

BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    
    screen.fill(BLACK)

    clock.tick(FPS)
