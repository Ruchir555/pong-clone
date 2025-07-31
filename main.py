# main.py
import pygame
import sys
from player import Player
from ball import Ball
from score import Score
# from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BALL_SPEED_X, BALL_SPEED_Y, CPU_SPEED, PLAYER_SPEED
from config import *
from court_appearance import *

# # Constants
# SCREEN_WIDTH = 640
# SCREEN_HEIGHT = 480
# FPS = 60


def main():
    pygame.init()

    # Load sounds
    hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
    player_win_point_sound = pygame.mixer.Sound("assets/sounds/player_win_point.wav")
    player_lose_point_sound = pygame.mixer.Sound("assets/sounds/player_lose_point.wav")
    game_win_sound = pygame.mixer.Sound("assets/sounds/game_win_1.wav")   #game_win, game_win_1


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Tennis")
    clock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/Jackfruit_song.mp3")   #tetris_theme.mid, Jackfruit_song.mp3
    pygame.mixer.music.set_volume(0.3)  # Optional: set background volume
    pygame.mixer.music.play(-1)         # Loop forever

    # Create player paddle
    paddle = Player(x=SCREEN_WIDTH//2 - 40, y=SCREEN_HEIGHT - 40, width=80, height=10, speed=PLAYER_SPEED)

    # Top CPU paddle
    cpu = Player(x=SCREEN_WIDTH // 2 - 40, y=40, width=80, height=10, speed=CPU_SPEED)

    # Create Ball
    ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
    ball_held = True  # Waiting for serve

    # Create score:
    # score = Score()
    score = Score(win_sound=player_win_point_sound, lose_sound=player_lose_point_sound, game_win_sound=game_win_sound)



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if ball_held and event.key == pygame.K_SPACE:
                    ball_held = False  # Launch the ball!
                    # Flat or lob depending on modifier key:
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        ball.z = 0
                        ball.z_speed = 10  # Lob
                    else:
                        ball.z = 0
                        ball.z_speed = 3   # Flat serve

        keys = pygame.key.get_pressed()
        paddle.move(keys)

        # BALL MOVEMENT LOGIC:
        if ball_held:
            ball.x = paddle.rect.centerx
            ball.y = paddle.rect.top - ball.radius
        else:
            ball.move()


         # Basic CPU AI: move toward the ball's x-position
        if not ball_held:
            if ball.x < cpu.rect.centerx:
                cpu.rect.x -= cpu.speed
            elif ball.x > cpu.rect.centerx:
                cpu.rect.x += cpu.speed

        # Keep CPU on screen
        cpu.rect.x = max(0, min(cpu.rect.x, SCREEN_WIDTH - cpu.rect.width))

        # CPU misses → point to player
        if ball.y + ball.radius < 0:
            print("Player scores!")
            player_win_point_sound.play()
            score.point_to_player()
            ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
            ball_held = True

        # Player misses → point to CPU
        elif ball.y - ball.radius > SCREEN_HEIGHT:
            print("CPU scores!")
            player_lose_point_sound.play()
            score.point_to_cpu()
            ball = Ball(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, radius=8, speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y)
            ball_held = True
        else:
            # Then: check collisions
            ball.check_collision(paddle.rect, hit_sound)
            ball.check_collision(cpu.rect, hit_sound)

        # Draw the court
        # screen.fill((0, 128, 0))  # Court background
        # draw_net(screen)          # Center net
        # draw_court(screen)
        draw_realistic_tennis_court(screen)


        paddle.draw(screen)
        cpu.draw(screen)
        ball.draw(screen)
        score.draw(screen)
        if ball_held:
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


