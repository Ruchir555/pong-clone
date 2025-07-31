# court_appearance.py
from config import *
import pygame



def draw_net(screen):
    net_height = 4
    net_width = 15
    gap = 10
    y = SCREEN_HEIGHT // 2 - net_height // 2

    for x in range(0, SCREEN_WIDTH, net_width + gap):
        pygame.draw.rect(screen, (255, 255, 255), (x, y, net_width, net_height))

def draw_court(screen):
    court_green = (94, 156, 85)
    line_white = (255, 255, 255)
    screen.fill(court_green)

    margin_x = 20
    margin_y = 40
    court_width = SCREEN_WIDTH - 2 * margin_x
    court_height = SCREEN_HEIGHT - 2 * margin_y

    # Outer rectangle
    pygame.draw.rect(screen, line_white, (margin_x, margin_y, court_width, court_height), 3)

    # Horizontal service lines
    service_y1 = margin_y + court_height // 4
    service_y2 = margin_y + 3 * court_height // 4
    pygame.draw.line(screen, line_white, (margin_x, service_y1), (margin_x + court_width, service_y1), 2)
    pygame.draw.line(screen, line_white, (margin_x, service_y2), (margin_x + court_width, service_y2), 2)

    # Center service line
    center_x = margin_x + court_width // 2
    pygame.draw.line(screen, line_white, (center_x, service_y1), (center_x, service_y2), 2)

    # Net (dashed)
    net_y = margin_y + court_height // 2
    for x in range(margin_x, margin_x + court_width, 20):
        pygame.draw.line(screen, line_white, (x, net_y), (x + 10, net_y), 2)

    # Center marks on baselines
    pygame.draw.line(screen, line_white, (center_x, margin_y),
                     (center_x, margin_y + 5), 2)
    pygame.draw.line(screen, line_white, (center_x, margin_y + court_height),
                     (center_x, margin_y + court_height - 5), 2)


def draw_realistic_tennis_court(screen):
    # Colors
    red = (180, 0, 0)
    green = (0, 100, 0)
    white = (255, 255, 255)

    screen.fill(red)  # Outer area (red court)

    # Court dimensions
    margin = 40
    court_width = SCREEN_WIDTH - 2 * margin
    court_height = SCREEN_HEIGHT - 2 * margin

    court_rect = pygame.Rect(margin, margin, court_width, court_height)
    pygame.draw.rect(screen, green, court_rect)  # Inner court

    # Draw outer court border
    pygame.draw.rect(screen, white, court_rect, 3)

    # Baselines
    pygame.draw.line(screen, white, (margin, margin), (margin + court_width, margin), 2)
    pygame.draw.line(screen, white, (margin, margin + court_height), (margin + court_width, margin + court_height), 2)

    # Singles sidelines
    side_offset = court_width * 0.08  # 8% for singles boundary inside doubles
    pygame.draw.line(screen, white, (margin + side_offset, margin), (margin + side_offset, margin + court_height), 2)
    pygame.draw.line(screen, white, (margin + court_width - side_offset, margin), (margin + court_width - side_offset, margin + court_height), 2)

    # Service lines
    service_y1 = margin + court_height // 4
    service_y2 = margin + 3 * court_height // 4
    pygame.draw.line(screen, white, (margin + side_offset, service_y1), (margin + court_width - side_offset, service_y1), 2)
    pygame.draw.line(screen, white, (margin + side_offset, service_y2), (margin + court_width - side_offset, service_y2), 2)

    # Center service line
    center_x = margin + court_width // 2
    pygame.draw.line(screen, white, (center_x, service_y1), (center_x, service_y2), 2)

    # Net line
    net_y = margin + court_height // 2
    pygame.draw.line(screen, white, (margin, net_y), (margin + court_width, net_y), 3)

    # Center marks on baseline
    pygame.draw.line(screen, white, (center_x, margin - 5), (center_x, margin + 5), 2)
    pygame.draw.line(screen, white, (center_x, margin + court_height - 5), (center_x, margin + court_height + 5), 2)
