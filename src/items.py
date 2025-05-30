import pygame


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
    )
]

def get_random_item():
    import random
    return random.choice(ITEMS)