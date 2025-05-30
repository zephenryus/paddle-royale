import pygame


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, width=10, height=100, speed=5):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.current_item = None
        self.active_effects = []

        self.up_key = None
        self.down_key = None
        self.activate_item_key = None

        self.prev_y = y
        self.velocity_y = 0

        self.original_height = height
        self.original_speed = speed

    def set_controls(self, up_key, down_key, activate_item_key):
        self.up_key = up_key
        self.down_key = down_key
        self.activate_item_key = activate_item_key

    def tick_effects(self):
        still_active = []
        for duration, expire_func in self.active_effects:
            duration -= 1
            if duration <= 0:
                expire_func(self)
            else:
                still_active.append((duration, expire_func))
        self.active_effects = still_active

    def activate_item(self):
        if self.current_item:
           self.current_item.use(self)
           self.current_item = None

    def update(self, screen_height):
        self.prev_y = self.rect.y
        self.tick_effects()

        keys = pygame.key.get_pressed()
        if self.up_key and keys[self.up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.down_key and keys[self.down_key] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

        if self.activate_item_key and keys[self.activate_item_key] and self.current_item:
            self.activate_item()

        self.velocity_y = self.rect.y - self.prev_y
