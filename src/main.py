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
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Paddle Royale")
    clock = pygame.time.Clock()

    left_paddle = Paddle(30, (WINDOW_HEIGHT - 100) // 2)
    right_paddle = Paddle(WINDOW_WIDTH - 40, (WINDOW_HEIGHT - 100) // 2, speed=10)
    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    left_score = 0
    right_score = 0

    font = pygame.font.SysFont(None, 64)
    paddle_bump_sound = pygame.mixer.Sound("sounds/paddle_bump.wav")
    goal_sound = pygame.mixer.Sound("sounds/goal.wav")

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
        ball.update(WINDOW_WIDTH, WINDOW_HEIGHT, [left_paddle.rect, right_paddle.rect], paddle_bump_sound)

        # Check for scoring
        if ball.rect.left <= 0:
            right_score += 1
            goal_sound.play()
            ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        elif ball.rect.right >= WINDOW_WIDTH:
            left_score += 1
            goal_sound.play()
            ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Drawing
        screen.fill(BLACK)

        # TODO: Draw paddles, ball, score, etc.
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        # Draw score
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WINDOW_WIDTH // 4 - left_text.get_width() // 2, 20))
        screen.blit(right_text, (3 * WINDOW_WIDTH // 4 - right_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
