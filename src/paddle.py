import random

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


        self.is_stunned = False
        self.stun_timer = 0
        self.original_color = (255, 255, 255)
        self.stun_shake_offset = 0

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

        if self.is_stunned:
            self.stun_timer -= 1
            self.update_stun_visuals()

    def activate_item(self, missiles_group=None, launch_missile_sound=None):
        print(f"Activate item called. Current item: {self.current_item.id if self.current_item else None}")
        print(f"Missile ready: {self.missile_ready}, Missile aimer: {self.missile_aimer is not None}")
        print(f"Missiles group provided: {missiles_group is not None}")

        # Check if we're in missile aiming mode
        if self.missile_aimer and self.missile_ready:
            print("Firing missile!")
            try:
                # Fire the missile
                print("About to import Missile...")
                from missile import Missile
                print("Missile imported successfully")

                print(
                    f"Creating missile at ({self.rect.centerx}, {self.rect.centery}) with angle {self.missile_aimer.angle}")

                # Spawn missile further from paddle to avoid immediate collision
                spawn_distance = 40
                import math
                spawn_x = self.rect.centerx + math.cos(self.missile_aimer.angle) * spawn_distance
                spawn_y = self.rect.centery + math.sin(self.missile_aimer.angle) * spawn_distance

                missile = Missile(spawn_x, spawn_y, self.missile_aimer.angle)
                # Set immunity so missile can't immediately hit the paddle that fired it
                missile.immune_paddle = self
                missile.immunity_timer = 30  # 30 frames of immunity (~0.5 seconds at 60fps)
                print("Missile created successfully")

                if missiles_group is not None:
                    print("Adding missile to group...")
                    missiles_group.add(missile)
                    print(f"Missile added. Group now has {len(missiles_group)} missiles")
                else:
                    print("ERROR: No missiles group provided!")

                # Clean up missile state
                self.missile_aimer = None
                self.missile_ready = False
                if launch_missile_sound:
                    launch_missile_sound.play()
                print("Missile firing complete")
                return  # Exit early, don't process regular items

            except Exception as e:
                print(f"ERROR creating/firing missile: {e}")
                import traceback
                traceback.print_exc()
                return

        # Handle regular items
        if self.current_item:
            if self.current_item.id == "missile":
                print("Starting aiming mode")
                # Start aiming - don't clear current_item yet
                self.current_item.use(self)
            else:
                # Regular item usage
                self.current_item.use(self)
                self.current_item = None

    def draw(self, surface):
        if self.is_stunned and hasattr(self, 'stun_shake_offset'):
            shake_rect = self.rect.copy()
            shake_rect.x += self.stun_shake_offset
            surface.blit(self.image, shake_rect)
        else:
            surface.blit(self.image, self.rect)

    def update(self, screen_height, missiles_group=None, launch_missile_sound=None):
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
        if self.activate_item_key and keys[self.activate_item_key]:
            if not self.activate_key_pressed and (self.current_item or self.missile_aimer):
                self.activate_item(missiles_group, launch_missile_sound)
                self.activate_key_pressed = True
                # Clear current_item only after missile is fired
                if not self.missile_aimer:
                    self.current_item = None
        elif not keys[self.activate_item_key]:
            self.activate_key_pressed = False  # Reset when key is released

        self.velocity_y = self.rect.y - self.prev_y

    def draw_missile_aimer(self, surface):
        """Draw the missile aimer if active"""
        if self.missile_aimer:
            self.missile_aimer.draw(surface)

    def update_stun_visuals(self):
        if not self.is_stunned:
            return

        if self.stun_timer > 60:
            color = (128, 128, 128)
            self.stun_shake_offset = 0
        elif self.stun_timer > 30:
            color = (96, 96, 96)
            self.stun_shake_offset = random.randint(-1, 1)
        else:
            if (self.stun_timer // 5) % 2:
                color = (200, 50, 50)
            else:
                color = (128, 128, 128)

            self.stun_shake_offset = random.randint(-3, 3)

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(color)