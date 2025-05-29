import random

import pygame.sprite


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, field_width, field_height):
        super().__init__()

        self.original_image = pygame.Surface((35, 35), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 215, 0), self.original_image.get_rect())
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()

        center_margin = field_width * 0.25  # Targeting the center 50% of the playing field
        min_x = int(field_width // 2 - center_margin)
        max_x = int(field_width // 2 + center_margin)

        self.rect.x = random.randint(min_x, max_x)
        self.rect.y = random.randint(50, field_height - 70)

        self.angle = 0

        self.collected = False

    def update(self):
        self.angle = (self.angle + 1) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
