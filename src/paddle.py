import pygame


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=10, height=100, speed=5):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.up_key = None
        self.down_key = None

        self.prev_y = y
        self.velocity_y = 0

    def set_controls(self, up_key, down_key):
        self.up_key = up_key
        self.down_key = down_key

    def update(self, screen_height):
        self.prev_y = self.rect.y

        keys = pygame.key.get_pressed()
        if self.up_key and keys[self.up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.down_key and keys[self.down_key] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

        self.velocity_y = self.rect.y - self.prev_y
