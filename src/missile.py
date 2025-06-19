import math
import pygame


class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed=8):
        super().__init__()
        self.image = pygame.Surface((8, 3))
        self.image.fill((255, 100, 100))  # Red missile

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.velocity = pygame.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        self.bounces_remaining = 3

    def update(self, screen_width, screen_height):
        # Move the missile
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Bounce off top/bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.velocity.y *= -1
            self.bounces_remaining -= 1

        # Bounce off left/right walls
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.velocity.x *= -1
            self.bounces_remaining -= 1

        # Remove missile if no bounces left
        if self.bounces_remaining <= 0:
            self.kill()

    def bounce_off_ball(self):
        """Reverse missile direction when hitting ball"""
        self.velocity.x *= -1
        self.velocity.y *= -1
        self.bounces_remaining -= 1

        if self.bounces_remaining <= 0:
            self.kill()


class MissileAimer:
    def __init__(self, paddle_rect, is_left_paddle=True):
        self.paddle_rect = paddle_rect
        self.is_left_paddle = is_left_paddle
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise
        self.speed = 0.05  # Radians per frame

        # Set initial angle and limits based on paddle side
        if is_left_paddle:
            # Left paddle aims right: -90 to 90 degrees
            self.angle = -math.pi / 2  # Start at -90 degrees
            self.min_angle = -math.pi / 2
            self.max_angle = math.pi / 2
        else:
            # Right paddle aims left: 90 to -90 degrees (or 90 to 270)
            self.angle = math.pi / 2  # Start at 90 degrees
            self.min_angle = math.pi / 2
            self.max_angle = 3 * math.pi / 2

    def update(self):
        self.angle += self.direction * self.speed

        # Reverse direction at limits
        if self.angle >= self.max_angle:
            self.angle = self.max_angle
            self.direction = -1
        elif self.angle <= self.min_angle:
            self.angle = self.min_angle
            self.direction = 1

    def get_aim_position(self):
        """Get the position of the aiming dot"""
        radius = 30
        center_x = self.paddle_rect.centerx
        center_y = self.paddle_rect.centery

        x = center_x + math.cos(self.angle) * radius
        y = center_y + math.sin(self.angle) * radius

        return (x, y)

    def draw(self, surface):
        """Draw the aiming dot"""
        pos = self.get_aim_position()
        pygame.draw.circle(surface, (255, 255, 0), (int(pos[0]), int(pos[1])), 5)