import random

import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=10, speed=5):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 255, 255), (0, 0, radius * 2, radius * 2))

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.speed_x = random.choice([-1, 1]) * speed
        self.speed_y = random.choice([-1, 1]) * speed
        self.serve_direction = random.choice([-1, 1])
        self.waiting_to_serve = False

    def serve(self):
        if self.waiting_to_serve:
            self.speed_x = self.serve_direction * self.speed
            self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])
            self.waiting_to_serve = False

    def reset(self, x, y, serve_direction):
        self.rect.center = (x, y)
        self.speed_x = 0
        self.speed_y = 0
        self.serve_direction = serve_direction
        self.waiting_to_serve = True

    def check_collision(self, paddle_rects, bump_sound=None):
        for paddle in paddle_rects:
            if self.rect.colliderect(paddle):
                self.speed_x *= -1
                if bump_sound:
                    bump_sound.play()
                break

    def update(self, screen_width, screen_height, paddle_rects, bump_sound=None, wall_bump_sound=None):
        if self.waiting_to_serve:
            return

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1
            if wall_bump_sound:
                wall_bump_sound.play()

        self.check_collision(paddle_rects, bump_sound)
