# score.py

import pygame
from config import SCREEN_WIDTH

POINTS = ["0", "15", "30", "40"]

class Score:
    def __init__(self):
        self.player_points = 0
        self.cpu_points = 0
        self.player_games = 0
        self.cpu_games = 0
        self.font = pygame.font.SysFont("Courier", 28)

    def point_to_player(self):
        self.player_points += 1
        self._apply_tennis_logic()

    def point_to_cpu(self):
        self.cpu_points += 1
        self._apply_tennis_logic()

    def _apply_tennis_logic(self):
        # Deuce logic
        if self.player_points >= 3 and self.cpu_points >= 3:
            if self.player_points == self.cpu_points + 2:
                self.player_games += 1
                self.reset_points()
            elif self.cpu_points == self.player_points + 2:
                self.cpu_games += 1
                self.reset_points()
        else:
            # Normal win logic
            if self.player_points >= 4 and self.player_points - self.cpu_points >= 2:
                self.player_games += 1
                self.reset_points()
            elif self.cpu_points >= 4 and self.cpu_points - self.player_points >= 2:
                self.cpu_games += 1
                self.reset_points()

    def reset_points(self):
        self.player_points = 0
        self.cpu_points = 0

    def draw(self, screen):
        # Points display
        if self.player_points >= 3 and self.cpu_points >= 3:
            if self.player_points == self.cpu_points:
                point_display = "Deuce"
            elif self.player_points > self.cpu_points:
                point_display = "Adv Player"
            else:
                point_display = "Adv CPU"
        else:
            player_score = POINTS[min(self.player_points, 3)]
            cpu_score = POINTS[min(self.cpu_points, 3)]
            point_display = f"Player: {player_score}   CPU: {cpu_score}"

        label = self.font.render(point_display, True, (255, 255, 255))
        games = f"Games - Player: {self.player_games}  CPU: {self.cpu_games}"
        games_label = self.font.render(games, True, (255, 255, 255))

        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 20))
        screen.blit(games_label, (SCREEN_WIDTH // 2 - games_label.get_width() // 2, 60))
