# Game Constants
import sys

import pygame

from ai_paddle import AIPaddle
from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard
from serve_prompt import ServePrompt

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
    font = pygame.font.SysFont(None, 64)
    small_font = pygame.font.SysFont(None, 36)

    show_splash = True
    selected_option = 0
    menu_options = ["1 Player", "2 Players"]
    is_single_player = True
    ai_difficulty = 1

    while show_splash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 2
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    is_single_player = (selected_option == 0)

                    if is_single_player:
                        difficulty_options = ["Easy", "Medium", "Hard"]
                        selected_difficulty = 1  # Default to medium
                        selecting_difficulty = True

                        while selecting_difficulty:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_UP:
                                        selected_difficulty = (selected_difficulty - 1) % len(difficulty_options)
                                    elif event.key == pygame.K_DOWN:
                                        selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
                                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                                        ai_difficulty = selected_difficulty
                                        selecting_difficulty = False

                            screen.fill(BLACK)
                            title_text = font.render("Select Difficulty", True, WHITE)
                            screen.blit(title_text,
                                        title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)))

                            for i, option in enumerate(difficulty_options):
                                prefix = "> " if i == selected_difficulty else "  "
                                option_text = small_font.render(f"{prefix}{option}", True, WHITE)
                                screen.blit(option_text, option_text.get_rect(
                                    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 40)))

                            pygame.display.flip()
                            clock.tick(FPS)

                        show_splash = False

        screen.fill(BLACK)
        title_text = font.render("PADDLE ROYALE!", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)))

        for i, option in enumerate(menu_options):
            prefix = "> " if i == selected_option else "  "
            option_text = small_font.render(f"{prefix}{option}", True, WHITE)
            screen.blit(option_text, option_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 40)))

        pygame.display.flip()
        clock.tick(FPS)

    left_paddle = Paddle(30, (WINDOW_HEIGHT - 100) // 2)
    left_paddle.set_controls(pygame.K_w, pygame.K_s)

    if is_single_player:
        difficulty_settings = [
            { "speed": 4, "lag_frames": 12 },
            { "speed": 5, "lag_frames": 6 },
            { "speed": 6, "lag_frames": 1 }
        ]
        ai_settings = difficulty_settings[ai_difficulty]
        right_paddle = AIPaddle(WINDOW_WIDTH - 40, (WINDOW_HEIGHT - 100) // 2, speed=ai_settings["speed"], reaction_delay=ai_settings["lag_frames"])
    else:
        right_paddle = Paddle(WINDOW_WIDTH - 40, (WINDOW_HEIGHT - 100) // 2, speed=10)
        right_paddle.set_controls(pygame.K_UP, pygame.K_DOWN)
    paddles = pygame.sprite.Group(left_paddle, right_paddle)
    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    ball_group = pygame.sprite.GroupSingle(ball)
    ball.waiting_to_serve = True

    paused = False
    scoreboard = Scoreboard(font)
    left_score = 0
    right_score = 0
    scoreboard.set_scores(left_score, right_score)
    serve_prompt = ServePrompt(font)

    paddle_bump_sound = pygame.mixer.Sound("sounds/paddle_bump.wav")
    wall_bump_sound = pygame.mixer.Sound("sounds/ball_bumps_wall.wav")
    goal_sound = pygame.mixer.Sound("sounds/goal.wav")

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif paused and event.key == pygame.K_q:
                    running = False
                elif ball.waiting_to_serve and event.key == pygame.K_SPACE:
                    ball.serve()

        if not paused:
            for paddle in paddles:
                if isinstance(paddle, AIPaddle):
                    paddle.update(WINDOW_HEIGHT, ball)
                else:
                    paddle.update(WINDOW_HEIGHT)
            ball.update(WINDOW_WIDTH, WINDOW_HEIGHT, [left_paddle, right_paddle], paddle_bump_sound, wall_bump_sound)

            # Check for scoring
            if ball.rect.left <= 0:
                right_score += 1
                goal_sound.play()
                last_scorer = "right"
                ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, serve_direction=-1)
                scoreboard.set_scores(left_score, right_score)
            elif ball.rect.right >= WINDOW_WIDTH:
                left_score += 1
                goal_sound.play()
                last_scorer = "left"
                ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, serve_direction=1)
                scoreboard.set_scores(left_score, right_score)

        # Drawing
        screen.fill(BLACK)

        paddles.draw(screen)
        ball_group.draw(screen)
        scoreboard.draw(screen, WINDOW_WIDTH)
        serve_prompt.visible = ball.waiting_to_serve
        serve_prompt.draw(screen, WINDOW_WIDTH, WINDOW_HEIGHT)

        if paused:
            pause_text = font.render("Paused", True, WHITE)
            prompt_text = small_font.render("Press ESC to resume | Q to quit", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)))
            screen.blit(prompt_text, prompt_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
