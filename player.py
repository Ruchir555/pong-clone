# player.py

import pygame

class Player:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep the paddle on screen
        self.rect.x = max(0, min(self.rect.x, 640 - self.rect.width))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
