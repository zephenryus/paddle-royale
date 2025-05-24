import pygame.font


class ServePrompt:
    def __init__(self, font: pygame.font.Font, text="Press SPACE to serve", color=(255, 255, 255)):
        self.font = font
        self.text = text
        self.color = color
        self.visible = False

    def draw(self, surface, screen_width, screen_height):
        if not self.visible:
            return

        rendered = self.font.render(self.text, True, self.color)
        surface.blit(rendered, (
            (screen_width - rendered.get_width()) // 2,
            (screen_height // 2) + 40
        ))