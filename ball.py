# ball.py

import pygame

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.z = 0              # height above the ground
        self.z_speed = 0        # vertical velocity
        self.gravity = 0.5      # how quickly the ball falls


    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Update height (z-axis)
        self.z += self.z_speed
        self.z_speed -= self.gravity  # gravity pulls it down

        # Bounce when it hits the ground (z=0)
        if self.z < 0:
            self.z = 0
            self.z_speed *= -0.6  # simulate bounce with energy loss

        # Bounce off left and right walls
        if self.x - self.radius <= 0 or self.x + self.radius >= 640:
            self.speed_x *= -1

        # # Bounce off top        # this is the standard pong variation, remove if you are playing against a CPU
        # if self.y - self.radius <= 0:
        #     self.speed_y *= -1


    def check_collision(self, paddle_rect, hit_sound=None):
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)

        if ball_rect.colliderect(paddle_rect):
            if hit_sound:
                hit_sound.play()
            # Only bounce if the ball is moving toward the paddle
            if self.speed_y > 0 and self.y < paddle_rect.centery:
                # Ball is moving down (player paddle)
                self.speed_y *= -1
                self.y = paddle_rect.top - self.radius

            elif self.speed_y < 0 and self.y > paddle_rect.centery:
                # Ball is moving up (CPU paddle)
                self.speed_y *= -1
                self.y = paddle_rect.bottom + self.radius


    def draw(self, screen):
        # Shadow (fixed y position on court)
        shadow_color = (0, 0, 0)
        pygame.draw.ellipse(screen, shadow_color,
            (int(self.x - self.radius), int(self.y + 8), self.radius * 2, 6))

        # Ball itself — shrink size based on height
        scale = max(0.5, 1 - self.z / 100)
        ball_radius = int(self.radius * scale)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), ball_radius)
