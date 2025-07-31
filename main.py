# main.py
import pygame
import sys
import time
from player import Player
from ball import Ball
from score import Score
from config import *
from court_appearance import *

def main():
    pygame.init()

    # Load sounds
    hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
    player_win_point_sound = pygame.mixer.Sound("assets/sounds/player_win_point.wav")
    player_lose_point_sound = pygame.mixer.Sound("assets/sounds/player_lose_point.wav")
    game_win_sound = pygame.mixer.Sound("assets/sounds/game_win_1.wav")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Tennis")
    clock = pygame.time.Clock()
    pygame.mixer.init()
    songs_dict = {
        "jack": "Jackfruit_song.mp3",
        "tetris": "tetris_theme.mid"
    }
    selected_song = songs_dict["tetris"]
    pygame.mixer.music.load(f"assets/sounds/{selected_song}")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    paddle = Player(x=SCREEN_WIDTH//2 - 40, y=SCREEN_HEIGHT - 40, width=80, height=10, speed=PLAYER_SPEED)
    cpu = Player(x=SCREEN_WIDTH // 2 - 40, y=40, width=80, height=10, speed=CPU_SPEED)

    ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
    ball_held = True

    server = "player"  # Initial server
    cpu_serve_delay_timer = 0
    cpu_serve_ready = False

    score = Score(win_sound=player_win_point_sound, lose_sound=player_lose_point_sound, game_win_sound=game_win_sound)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if ball_held and server == "player" and event.key == pygame.K_SPACE:
                    ball_held = False
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        ball.z = 0
                        ball.z_speed = 10
                    else:
                        ball.z = 0
                        ball.z_speed = 3

        keys = pygame.key.get_pressed()
        paddle.move(keys)

        if score.just_changed_server and score.last_game_winner:
            server = "cpu" if server == "player" else "player"
            score.just_changed_server = False

        # Ensure CPU serve setup occurs any time it's CPU's turn to serve
        if ball_held and server == "cpu" and not cpu_serve_ready:
            cpu_serve_delay_timer = time.time()
            cpu_serve_ready = True

        if ball_held:
            if server == "player":
                ball.x = paddle.rect.centerx
                ball.y = paddle.rect.top - ball.radius
            else:
                ball.x = cpu.rect.centerx
                ball.y = cpu.rect.bottom + ball.radius
                if cpu_serve_ready and time.time() - cpu_serve_delay_timer > 0.5:
                    ball_held = False
                    ball.z = 0
                    ball.z_speed = 4
                    ball.speed_y = BALL_SPEED_Y
                    ball.speed_x = BALL_SPEED_X
                    cpu_serve_ready = False
        else:
            ball.move()

        if not ball_held:
            if ball.x < cpu.rect.centerx:
                cpu.rect.x -= cpu.speed
            elif ball.x > cpu.rect.centerx:
                cpu.rect.x += cpu.speed

        cpu.rect.x = max(0, min(cpu.rect.x, SCREEN_WIDTH - cpu.rect.width))

        if ball.y + ball.radius < 0:
            player_win_point_sound.play()
            player_won_game = score.point_to_player()
            ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
            ball_held = True

        elif ball.y - ball.radius > SCREEN_HEIGHT:
            player_lose_point_sound.play()
            cpu_won_game = score.point_to_cpu()
            ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
            ball_held = True
        else:
            ball.check_collision(paddle.rect, hit_sound)
            ball.check_collision(cpu.rect, hit_sound)

        draw_realistic_tennis_court(screen)
        paddle.draw(screen)
        cpu.draw(screen)
        ball.draw(screen)
        score.draw(screen)

        if ball_held and server == "player":
            font = pygame.font.SysFont("Courier", 24)
            label = font.render("Press SPACE to Serve", True, (255, 255, 255))
            label2 = font.render("SHIFT + SPACE to Lob Serve", True, (255, 255, 255))
            screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2))
            screen.blit(label2, (SCREEN_WIDTH // 2 - label2.get_width() // 2, SCREEN_HEIGHT // 2 + label2.get_width() // 5))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
