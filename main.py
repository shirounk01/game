from typing import Any
import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
FPS = 15
FRAME_INTERVAL = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, img, frame_count):
        super().__init__()
        self.img = pygame.image.load(img)
        self.frame_count = frame_count
        self.frame_width = self.img.get_width()/self.frame_count
        self.frame_height = self.img.get_height()
        self.current_frame = 0
    
    def get_frame(self, flip_frame):
        self.current_frame = (self.current_frame+1)%self.frame_count
        frame=self.current_frame
        rect = pygame.Rect(frame*self.frame_width, 0, self.frame_width, self.frame_height)
        return pygame.transform.flip(self.img, flip_frame, False).subsurface(rect)
    
    def animation_status(self):
        return not self.current_frame == self.frame_count-1
    
    def get_size(self):
        return (self.frame_width, self.frame_height)



class Player():
    def __init__(self, screen):
        self.idle = Sprite("sprites\player\Idle.png", 6)
        self.run = Sprite("sprites\player\Run.png", 8)
        self.attack = Sprite("sprites\player\Attack.png", 4)
        self.screen = screen
        self.direction = False
        self.attack_lock = False
        self.x = 0
        self.y = HEIGHT - self.idle.get_size()[0]
        self.runnable_distance = 10

    def update(self):
        keys = pygame.key.get_pressed()
        sprite = self.idle.get_frame(self.direction)
        if not self.attack_lock:
            if keys[pygame.K_LEFT] and self.x-self.runnable_distance >= 0:
                self.x = self.x-self.runnable_distance
                self.direction = True
                sprite = self.run.get_frame(self.direction)
            if keys[pygame.K_RIGHT]:                
                self.x = self.x+self.runnable_distance
                self.direction = False
                sprite = self.run.get_frame(self.direction)
        if keys[pygame.K_x] or self.attack_lock:
            self.attack_lock = self.attack.animation_status()
            sprite = self.attack.get_frame(self.direction)
        
        rect = (self.x, self.y)
        print(rect)
        screen.blit(sprite, rect)




player = Player(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    screen.fill((44,44,44))

    player.update()
    pygame.display.flip()
    clock.tick(FPS)
