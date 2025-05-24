import math
import random

import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=10, speed=5):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 255, 255), (0, 0, radius * 2, radius * 2))

        self.rect = self.image.get_rect(center=(x, y))
        self.initial_speed = speed
        self.speed = speed
        self.max_speed = 20
        self.speed_ramp_duration = 60_000
        self.spawn_time = pygame.time.get_ticks()
        self.velocity = pygame.Vector2(random.choice([-1, 1]), random.uniform(-1, 1)).normalize() * speed
        self.serve_direction = random.choice([-1, 1])
        self.waiting_to_serve = False

    def serve(self):
        if self.waiting_to_serve:
            self.velocity = pygame.Vector2(self.serve_direction, random.choice([-0.5, -0.25, 0.25, 0.5])).normalize() * self.speed
            self.spawn_time = pygame.time.get_ticks()
            self.waiting_to_serve = False

    def reset(self, x, y, serve_direction):
        self.rect.center = (x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.serve_direction = serve_direction
        self.waiting_to_serve = True

    def check_collision(self, paddles, bump_sound=None):
        for paddle in paddles:
            if self.rect.colliderect(paddle.rect):
                # Find relative hit position
                hit_y = self.rect.centery - paddle.rect.top
                zone_height = paddle.rect.height / 8
                zone_index = min(7, max(0, int(hit_y // zone_height)))

                # Define reflection angles in radians (-60, -45, -30, -15, 15, 30, 45, 60)
                angles_rad = [-1.047198, -0.785398, -0.523598, -0.261799, 0.261799, 0.523598, 0.785398, 1.047198]
                radians = angles_rad[zone_index]

                # Determine the direction (left or right)
                direction = 1 if self.velocity.x < 0 else -1
                if direction == 1:
                    self.rect.left = paddle.rect.right
                else:
                    self.rect.right = paddle.rect.left

                # Convert to a vector
                self.velocity = pygame.Vector2(
                    direction * math.cos(radians),
                    math.sin(radians)
                )

                transfer_factor = 0.5
                self.velocity.y += paddle.velocity_y * transfer_factor

                # Clamp velocity to prevent super steep bounces
                if abs(self.velocity.y) > 0.98:
                    self.velocity.y = 0.98 * math.copysign(1, self.velocity.y)

                self.velocity = self.velocity.normalize() * self.get_current_speed()

                if bump_sound:
                    bump_sound.play()
                break

    def get_current_speed(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.spawn_time

        if elapsed >= self.speed_ramp_duration:
            return self.max_speed

        t = elapsed / self.speed_ramp_duration
        return self.initial_speed + (self.max_speed - self.initial_speed) * t

    def update(self, screen_width, screen_height, paddles, bump_sound=None, wall_bump_sound=None):
        if self.waiting_to_serve:
            return

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.velocity.y *= -1
            if wall_bump_sound:
                wall_bump_sound.play()

        self.check_collision(paddles, bump_sound)
