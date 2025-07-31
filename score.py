# score.py

import pygame
from config import SCREEN_WIDTH

POINTS = ["0", "15", "30", "40"]

class Score:
    def __init__(self, win_sound=None, lose_sound=None, game_win_sound=None):
        self.player_points = 0
        self.cpu_points = 0
        self.player_games = 0
        self.cpu_games = 0
        self.font = pygame.font.SysFont("Courier", 28)
        self.win_sound = win_sound
        self.lose_sound = lose_sound
        self.game_win_sound = game_win_sound
        self.last_game_winner = None  # Track who won the last game
        self.just_changed_server = False  # Flag to trigger CPU serve

    def point_to_player(self):
        if self.win_sound:
            self.win_sound.play()
        self.player_points += 1
        return self._apply_tennis_logic("player")

    def point_to_cpu(self):
        if self.lose_sound:
            self.lose_sound.play()
        self.cpu_points += 1
        return self._apply_tennis_logic("cpu")

    def _apply_tennis_logic(self, scorer):
        if self.player_points >= 3 and self.cpu_points >= 3:
            if self.player_points == self.cpu_points + 2:
                self.player_games += 1
                self.last_game_winner = "player"
                self.just_changed_server = True
                if self.game_win_sound:
                    self.game_win_sound.play()
                self.reset_points()
                return True
            elif self.cpu_points == self.player_points + 2:
                self.cpu_games += 1
                self.last_game_winner = "cpu"
                self.just_changed_server = True
                if self.game_win_sound:
                    self.game_win_sound.play()
                self.reset_points()
                return True
        else:
            if self.player_points >= 4 and self.player_points - self.cpu_points >= 2:
                self.player_games += 1
                self.last_game_winner = "player"
                self.just_changed_server = True
                if self.game_win_sound:
                    self.game_win_sound.play()
                self.reset_points()
                return True
            elif self.cpu_points >= 4 and self.cpu_points - self.player_points >= 2:
                self.cpu_games += 1
                self.last_game_winner = "cpu"
                self.just_changed_server = True
                if self.game_win_sound:
                    self.game_win_sound.play()
                self.reset_points()
                return True

        return False

    def reset_points(self):
        self.player_points = 0
        self.cpu_points = 0

    def draw(self, screen):
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

        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 10))
        screen.blit(games_label, (SCREEN_WIDTH // 2 - games_label.get_width() // 2, 40))
