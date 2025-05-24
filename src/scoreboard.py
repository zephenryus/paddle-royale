import pygame.font


class Scoreboard:
    def __init__(self, font: pygame.font.Font, color=(255, 255, 255), y=20):
        self.font = font
        self.color = color
        self.y = y
        self.left_score = 0
        self.right_score = 0

    def set_scores(self, left, right):
        self.left_score = left
        self.right_score = right

    def draw(self, surface, screen_width):
        left_text = self.font.render(str(self.left_score), True, self.color)
        right_text = self.font.render(str(self.right_score), True, self.color)

        surface.blit(left_text, (screen_width // 4 - left_text.get_width() // 2, self.y))
        surface.blit(right_text, (3 * screen_width // 4 - right_text.get_width() // 2, self.y))