import random

import pygame


class Ball:
    def __init__(self, x, y, radius=10, speed=5):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.speed_x = random.choice([-1, 1]) * speed
        self.speed_y = random.choice([-1, 1]) * speed
        self.radius = radius

    def update(self, screen_width, screen_height):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

        # TODO: Add paddle collision and scoring

    def draw(self, surface):
        pygame.draw.ellipse(surface, (255, 255, 255), self.rect)
