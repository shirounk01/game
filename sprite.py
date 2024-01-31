import pygame


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

    # check if the animation is ongoing: ongoing -> True, finished -> False
    def check_animation_status(self):
        return not self.current_frame == self.frame_count - 1

    # get the width and height of the frame (sprite)
    def get_size(self):
        return (self.frame_width, self.frame_height)
