import pygame


class Paddle:
    def __init__(self, x, y, width=10, height=100, speed=5):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, up, down, screen_height):
        keys = pygame.key.get_pressed()
        if keys[up] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
