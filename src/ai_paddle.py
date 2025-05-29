from paddle import Paddle


class AIPaddle(Paddle):
    def update(self, window_height, ball=None):
        if ball:
            target_y = ball.rect.centery
            if self.rect.centery < target_y:
                self.rect.y += min(self.speed, target_y - self.rect.centery)
            elif self.rect.centery > target_y:
                self.rect.y -= min(self.speed, self.rect.centery - target_y)

        self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))
