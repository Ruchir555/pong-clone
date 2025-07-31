# main.py
import pygame
import sys
import time
from player import Player
from ball import Ball
from score import Score
from config import *
from court_appearance import *

def show_difficulty_menu(screen):
    font = pygame.font.SysFont("Courier", 28)
    title = font.render("Select Difficulty", True, (255, 255, 255))
    options = ["Easy", "Medium", "Hard"]
    selected = 0

    while True:
        screen.fill((0, 0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            label = font.render(option, True, color)
            screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 200 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower()

def show_pause_menu(screen):
    font = pygame.font.SysFont("Courier", 32)
    options = ["Back to Game", "Exit to Menu"]
    selected = 0

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    while True:
        screen.blit(overlay, (0, 0))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            label = font.render(option, True, color)
            screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 200 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]

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

    while True:
        # Select difficulty
        difficulty = show_difficulty_menu(screen)
        if difficulty == "easy":
            cpu_speed = CPU_SPEED_EASY
            ball_speed_x = BALL_SPEED_X_EASY
            ball_speed_y = BALL_SPEED_Y_EASY
        elif difficulty == "hard":
            cpu_speed = CPU_SPEED_HARD
            ball_speed_x = BALL_SPEED_X_HARD
            ball_speed_y = BALL_SPEED_Y_HARD
        else:  # medium
            cpu_speed = CPU_SPEED
            ball_speed_x = BALL_SPEED_X
            ball_speed_y = BALL_SPEED_Y

        paddle = Player(x=SCREEN_WIDTH//2 - 40, y=SCREEN_HEIGHT - 40, width=80, height=10, speed=PLAYER_SPEED)
        cpu = Player(x=SCREEN_WIDTH // 2 - 40, y=40, width=80, height=10, speed=cpu_speed)
        ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=ball_speed_x, speed_y=ball_speed_y)
        score = Score(win_sound=player_win_point_sound, lose_sound=player_lose_point_sound, game_win_sound=game_win_sound)

        ball_held = True
        server = "player"  # Initial server
        cpu_serve_delay_timer = 0
        cpu_serve_ready = False
        in_game = True

        while in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        choice = show_pause_menu(screen)
                        if choice == "Exit to Menu":
                            in_game = False
                            break
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
                        ball.speed_y = ball_speed_y
                        ball.speed_x = ball_speed_x
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
                score.point_to_player()
                ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=ball_speed_x, speed_y=ball_speed_y)
                ball_held = True

            elif ball.y - ball.radius > SCREEN_HEIGHT:
                player_lose_point_sound.play()
                score.point_to_cpu()
                ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=ball_speed_x, speed_y=ball_speed_y)
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

if __name__ == "__main__":
    main()
