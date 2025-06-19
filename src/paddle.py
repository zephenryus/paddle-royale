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

        # Missile-related attributes
        self.missile_aimer = None
        self.missile_ready = False

        # Key state tracking for single presses
        self.activate_key_pressed = False

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

    def activate_item(self, missiles_group=None):
        print(f"Activate item called. Current item: {self.current_item.id if self.current_item else None}")
        print(f"Missile ready: {self.missile_ready}, Missile aimer: {self.missile_aimer is not None}")

        if self.current_item:
            if self.current_item.id == "missile":
                if self.missile_ready and self.missile_aimer:
                    print("Firing missile!")
                    # Fire the missile
                    from missile import Missile
                    missile = Missile(
                        self.rect.centerx,
                        self.rect.centery,
                        self.missile_aimer.angle
                    )
                    if missiles_group:
                        missiles_group.add(missile)

                    # Clean up
                    self.missile_aimer = None
                    self.missile_ready = False
                    self.current_item = None
                else:
                    print("Starting aiming mode")
                    # Start aiming
                    self.current_item.use(self)
            else:
                self.current_item.use(self)
                self.current_item = None

    def update(self, screen_height, missiles_group=None):
        self.prev_y = self.rect.y
        self.tick_effects()

        # Update missile aimer if active
        if self.missile_aimer:
            self.missile_aimer.paddle_rect = self.rect
            self.missile_aimer.update()

        keys = pygame.key.get_pressed()
        if self.up_key and keys[self.up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.down_key and keys[self.down_key] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

        # Handle activation key with single press detection
        if self.activate_item_key and keys[self.activate_item_key] and self.current_item:
            if not self.activate_key_pressed:  # Only trigger on first press
                self.activate_item(missiles_group)
                self.activate_key_pressed = True
        elif not keys[self.activate_item_key]:
            self.activate_key_pressed = False  # Reset when key is released

        self.velocity_y = self.rect.y - self.prev_y

    def draw_missile_aimer(self, surface):
        """Draw the missile aimer if active"""
        if self.missile_aimer:
            self.missile_aimer.draw(surface)