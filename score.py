# score.py

import pygame
from config import SCREEN_WIDTH


POINTS = ["0", "15", "30", "40", "Adv", "Win"]

class Score:
    def __init__(self):
        self.player = 0
        self.cpu = 0
        self.font = pygame.font.SysFont("Courier", 32)

    def point_to_player(self):
        self.player += 1
        self._apply_tennis_logic()

    def point_to_cpu(self):
        self.cpu += 1
        self._apply_tennis_logic()

    def _apply_tennis_logic(self):
        # Simplified tennis scoring logic
        if self.player >= 4 and self.player - self.cpu >= 2:
            self.player = 0
            self.cpu = 0
            print(">> Player wins the game!")

        elif self.cpu >= 4 and self.cpu - self.player >= 2:
            self.player = 0
            self.cpu = 0
            print(">> CPU wins the game!")

    def draw(self, screen):
        player_score = POINTS[min(self.player, 5)]
        cpu_score = POINTS[min(self.cpu, 5)]
        text = f"Player: {player_score}   CPU: {cpu_score}"
        label = self.font.render(text, True, (255, 255, 255))
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 20))
