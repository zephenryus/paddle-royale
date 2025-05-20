# Game Constants
import sys

import pygame

from ball import Ball
from paddle import Paddle

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main():
    # Initialize PyGame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Paddle Royale")
    clock = pygame.time.Clock()

    left_paddle = Paddle(30, (WINDOW_HEIGHT - 100) // 2)
    right_paddle = Paddle(WINDOW_WIDTH - 40, (WINDOW_HEIGHT - 100) // 2)
    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # TODO: Add game logic
        left_paddle.move(pygame.K_w, pygame.K_s, WINDOW_HEIGHT)
        right_paddle.move(pygame.K_UP, pygame.K_DOWN, WINDOW_HEIGHT)
        ball.update(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Drawing
        screen.fill(BLACK)

        # TODO: Draw paddles, ball, score, etc.
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
