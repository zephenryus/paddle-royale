import random

import pygame


class ExplosionCircle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = random.randint(15, 30)
        self.growth_rate = random.uniform(1.5, 3.0)
        self.lifetime = 0
        self.max_lifetime = random.randint(20, 35)  # frames

    def update(self):
        self.lifetime += 1
        self.radius += self.growth_rate

        if self.radius > self.max_radius * 0.7:
            self.growth_rate *= 0.95

        return self.lifetime < self.max_lifetime and self.radius < self.max_radius * 1.2

    def get_color(self):
        progress = self.lifetime / self.max_lifetime

        if progress < 0.3:
            r = 255
            g = 255 - int(50 * (progress / 0.3))
        elif progress < 0.7:
            r = 255
            g = 205 - int(50 * ((progress - 0.3) / 0.4))
        else:
            r = 255 - int(100 * ((progress - 0.7) / 0.3))
            g = max(0, 155 - int(155 * ((progress - 0.7) / 0.3)))

        alpha = max(0, 255 - int(255 * (progress ** 2)))
        return r, g, 0, alpha

    def draw(self, surface):
        if self.radius > 1:
            color = self.get_color()

            temp_surface = pygame.Surface((int(self.radius * 2), int(self.radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, color,
                               (int(self.radius), int(self.radius)),
                               int(self.radius))
            surface.blit(temp_surface, (self.x - self.radius, self.y - self.radius))


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.circles = []
        self.active = True

        num_circles = random.randint(3, 5)
        for _ in range(num_circles):
            offset_x = random.gauss(0, 8)
            offset_y = random.gauss(0, 8)

            circle_x = x + offset_x
            circle_y = y + offset_y

            self.circles.append(ExplosionCircle(circle_x, circle_y))

    def update(self):
        self.circles = [circle for circle in self.circles if circle.update()]

        if not self.circles:
            self.active = False

        return self.active

    def draw(self, surface):
        for circle in self.circles:
            circle.draw(surface)
