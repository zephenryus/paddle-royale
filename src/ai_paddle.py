from paddle import Paddle


class AIPaddle(Paddle):
    def __init__(self, x, y, width=10, height=100, speed=5, reaction_delay=0):
        super().__init__(x, y, width, height, speed)
        self.reaction_delay = reaction_delay
        self.frame_counter = 0
        self.last_seen_ball_y = y

    def update(self, window_height, ball=None):
        self.tick_effects()

        if ball and self.speed > 0:
            self.frame_counter += 1
            if self.frame_counter >= self.reaction_delay:
                self.last_seen_ball_y = ball.rect.centery
                self.frame_counter = 0

            if self.rect.centery < self.last_seen_ball_y:
                self.rect.y += min(self.speed, self.last_seen_ball_y - self.rect.centery)
            elif self.rect.centery > self.last_seen_ball_y:
                self.rect.y -= min(self.speed, self.rect.centery - self.last_seen_ball_y)

        self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))

        self.velocity_y = self.rect.y - self.prev_y
        self.prev_y = self.rect.y
