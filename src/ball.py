import random

import pygame


class Ball:
    def __init__(self, x, y, radius=10, speed=5):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.speed_x = random.choice([-1, 1]) * speed
        self.speed_y = random.choice([-1, 1]) * speed
        self.radius = radius

    def check_collision(self, paddle_rects):
        for paddle in paddle_rects:
            if self.rect.colliderect(paddle):
                self.speed_x *= -1
                break

    def update(self, screen_width, screen_height, paddle_rects):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

        self.check_collision(paddle_rects)

        # TODO: Add scoring

    def draw(self, surface):
        pygame.draw.ellipse(surface, (255, 255, 255), self.rect)
