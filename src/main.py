# Game Constants
import random
import sys

import pygame

from ItemBox import ItemBox
from ai_paddle import AIPaddle
from ball import Ball
from items import get_random_item, stun_paddle_effect, ITEMS
from paddle import Paddle
from scoreboard import Scoreboard
from serve_prompt import ServePrompt

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_item_icon(screen, item, x, y):
    icon = pygame.Surface((20, 20))
    icon.fill(item.color)
    screen.blit(icon, (x, y))


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
    left_paddle.set_controls(pygame.K_w, pygame.K_s, pygame.K_d)

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
        right_paddle.set_controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT)
    left_paddle.current_item = ITEMS[2]
    paddles = pygame.sprite.Group(left_paddle, right_paddle)
    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    ball_group = pygame.sprite.GroupSingle(ball)
    ball.waiting_to_serve = True
    missiles = pygame.sprite.Group()
    item_boxes = pygame.sprite.Group()
    item_spawn_timer = 0
    item_spawn_interval = random.randint(5, 20) * FPS

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
            item_spawn_timer += 1
            if item_spawn_timer >= item_spawn_interval:
                item_boxes.add(ItemBox(WINDOW_WIDTH, WINDOW_HEIGHT))
                item_spawn_interval = random.randint(5, 20) * FPS
                item_spawn_timer = 0

            for paddle in paddles:
                if isinstance(paddle, AIPaddle):
                    paddle.update(WINDOW_HEIGHT, ball)
                else:
                    paddle.update(WINDOW_HEIGHT, missiles)
            ball.update(WINDOW_WIDTH, WINDOW_HEIGHT, [left_paddle, right_paddle], paddle_bump_sound, wall_bump_sound)
            missiles.update(WINDOW_WIDTH, WINDOW_HEIGHT)
            item_boxes.update()

            # Check missile collisions with paddles
            for missile in missiles:
                if missile.rect.colliderect(left_paddle.rect):
                    stun_paddle_effect(left_paddle)
                    missile.kill()
                elif missile.rect.colliderect(right_paddle.rect):
                    stun_paddle_effect(right_paddle)
                    missile.kill()

            # Check missile collisions with ball
            for missile in missiles:
                if missile.rect.colliderect(ball.rect):
                    # Reverse ball direction
                    ball.velocity.x *= -1
                    ball.velocity.y *= -1
                    # Bounce missile
                    missile.bounce_off_ball()

            # Check for scoring
            if ball.rect.left <= 0:
                right_score += 1
                goal_sound.play()
                ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, serve_direction=-1)
                scoreboard.set_scores(left_score, right_score)
            elif ball.rect.right >= WINDOW_WIDTH:
                left_score += 1
                goal_sound.play()
                ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, serve_direction=1)
                scoreboard.set_scores(left_score, right_score)

        hit_box = pygame.sprite.spritecollideany(ball, item_boxes)
        if hit_box:
            item_boxes.remove(hit_box)

            if ball.last_hit_by == "left":
                if left_paddle.current_item is None:
                    left_paddle.current_item = get_random_item()
                    print(f"Left paddle got {left_paddle.current_item.name}")

            elif ball.last_hit_by == "right":
                if right_paddle.current_item is None:
                    right_paddle.current_item = get_random_item()
                    print(f"Right paddle got {right_paddle.current_item.name}")

        # Drawing
        screen.fill(BLACK)

        paddles.draw(screen)
        missiles.draw(screen)
        ball_group.draw(screen)
        left_paddle.draw_missile_aimer(screen)
        right_paddle.draw_missile_aimer(screen)
        item_boxes.draw(screen)
        if left_paddle.current_item:
            draw_item_icon(screen, left_paddle.current_item, 20, 20)
        if right_paddle.current_item:
            draw_item_icon(screen, right_paddle.current_item, WINDOW_WIDTH - 40, 20)
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
