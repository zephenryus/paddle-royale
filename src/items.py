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

ITEMS = [
    Item(
        id="big_paddle",
        name="Big Paddle",
        description="Increase size, lower speed.",
        color=(100, 255, 100),
        strategy=big_paddle_strategy
    )
]

def get_random_item():
    import random
    return random.choice(ITEMS)