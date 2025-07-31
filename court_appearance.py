# court_appearance.py
from config import *
import pygame

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
