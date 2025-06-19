import pygame

from missile import MissileAimer


class Item:
    def __init__(self, id, name, description, color, strategy):
        self.id = id
        self.name = name
        self.description = description
        self.color = color
        self.strategy = strategy

    def use(self, paddle):
        self.strategy(paddle)


def big_paddle_strategy(paddle):
    paddle.rect.height = int(paddle.rect.height * 1.5)
    paddle.image = pygame.Surface((paddle.rect.width, paddle.rect.height))
    paddle.image.fill((255, 255, 255))
    paddle.speed = max(2, int(paddle.speed * 0.8))

    paddle.rect = paddle.image.get_rect(center=paddle.rect.center)

    def revert(p):
        p.rect.height = p.original_height
        p.image = pygame.Surface((p.rect.width, p.rect.height))
        p.image.fill((255, 255, 255))
        p.speed = p.original_speed
        p.rect = p.image.get_rect(center=p.rect.center)

    paddle.active_effects.append((5 * 60, revert))


def small_paddle_strategy(paddle):
    paddle.rect.height = int(paddle.rect.height * 0.5)
    paddle.image = pygame.Surface((paddle.rect.width, paddle.rect.height))
    paddle.image.fill((255, 255, 255))
    paddle.speed = int(paddle.speed * 2.0)

    paddle.rect = paddle.image.get_rect(center=paddle.rect.center)

    def revert(p):
        p.rect.height = p.original_height
        p.image = pygame.Surface((p.rect.width, p.rect.height))
        p.image.fill((255, 255, 255))
        p.speed = p.original_speed
        p.rect = p.image.get_rect(center=p.rect.center)

    paddle.active_effects.append((5 * 60, revert))


def missile_strategy(paddle):
    # Determine if this is the left paddle (check x position)
    is_left_paddle = paddle.rect.centerx < 400  # Assuming 800px wide screen
    # Create aimer and attach to paddle
    paddle.missile_aimer = MissileAimer(paddle.rect, is_left_paddle)
    paddle.missile_ready = True


def stun_paddle_effect(paddle):
    """Stun effect for when hit by missile"""
    original_speed = paddle.speed
    paddle.speed = 0

    def remove_stun(p):
        p.speed = original_speed

    paddle.active_effects.append((3 * 60, remove_stun))  # 3 seconds at 60fps


ITEMS = [
    Item(
        id="big_paddle",
        name="Big Paddle",
        description="Increase size, lower speed.",
        color=(100, 255, 100),
        strategy=big_paddle_strategy
    ),
    Item(
        id="small_paddle",
        name="Small Paddle",
        description="Shrinks paddle, but increases speed.",
        color=(100, 100, 255),
        strategy=small_paddle_strategy
    ),
    Item(
        id="missile",
        name="Missile",
        description="Launch a bouncing missile to stun opponent.",
        color=(255, 100, 100),
        strategy=missile_strategy
    )
]


def get_random_item():
    import random
    return random.choice(ITEMS)