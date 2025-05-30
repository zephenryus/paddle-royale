import pygame


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=10, height=100, speed=5):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.current_item = None
        self.up_key = None
        self.down_key = None
        self.activate_item_key = None

        self.prev_y = y
        self.velocity_y = 0

    def set_controls(self, up_key, down_key, activate_item_key):
        self.up_key = up_key
        self.down_key = down_key
        self.activate_item_key = activate_item_key

    def activate_item(self):
        if not self.current_item:
            return

        item_id = self.current_item["id"]
        if item_id == "big_paddle":
            self.rect.height = int(self.rect.height * 1.5)
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill((255, 255, 255))
            self.speed = max(2, int(self.speed * 0.6))

        self.current_item = None

    def update(self, screen_height):
        self.prev_y = self.rect.y

        keys = pygame.key.get_pressed()
        if self.up_key and keys[self.up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.down_key and keys[self.down_key] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

        if self.activate_item_key and keys[self.activate_item_key] and self.current_item:
            self.activate_item()

        self.velocity_y = self.rect.y - self.prev_y
