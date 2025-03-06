import pygame
import math

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Universe Planck Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 100, 255)

# Entity properties
ball_radius = 15
pitcher_pos = (100, 300)  # Base pitcher position
catcher_pos = (700, 300)  # Base catcher position
t = 0
speed = 0.003

# Planck slider
slider_x, slider_y = 20, 20
slider_width, slider_height = 300, 20
min_planck = 1e-35
max_planck = 0.01
planck_value = min_planck
log_planck = math.log10(min_planck)

# Font
font = pygame.font.Font(None, 36)

# Gradient background
background = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    color = (220 - y // 3, 220 - y // 3, 255 - y // 4)
    pygame.draw.line(background, color, (0, y), (WIDTH, y))

# Textured entities
def create_texture(radius, color):
    texture = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        alpha = int(255 * (1 - r / radius))
        pygame.draw.circle(texture, (*color, alpha), (radius, radius), r)
    pygame.draw.circle(texture, DARK_RED if color == RED else (0, 50, 100), (radius, radius), radius // 2)
    return texture

ball_texture = create_texture(ball_radius, RED)
ghost_ball_texture = create_texture(ball_radius // 2, RED)
pitcher_texture = create_texture(20, BLUE)
catcher_texture = create_texture(20, BLUE)

# Main loop
running = True
dragging = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if slider_x <= mx <= slider_x + slider_width and slider_y <= my <= slider_y + slider_height:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            mx, _ = event.pos
            mx = max(slider_x, min(mx, slider_x + slider_width))
            log_planck = math.log10(min_planck) + (math.log10(max_planck) - math.log10(min_planck)) * (mx - slider_x) / slider_width
            planck_value = 10 ** log_planck

    screen.blit(background, (0, 0))

    # Draw slider
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height), border_radius=5)
    slider_pos = slider_x + (log_planck - math.log10(min_planck)) * slider_width / (math.log10(max_planck) - math.log10(min_planck))
    pygame.draw.rect(screen, BLACK, (slider_pos - 5, slider_y, 10, slider_height), border_radius=5)
    text = font.render(f"Planck Length: {planck_value:.2e} m", True, BLACK)
    screen.blit(text, (slider_x, slider_y + 30))

    # Calculate number of paths
    path_factor = math.log10(planck_value / min_planck) / math.log10(max_planck / min_planck)
    num_paths = min(int(path_factor * 10), 10)

    # Draw pitcher and catcher with multiplicity
    for i in range(num_paths + 1):
        offset = i * planck_value * 5000
        y_offset = math.sin(t * math.pi + i) * offset if i % 2 == 0 else (4 * t * (1 - t)) * offset
        alpha = 255 if i == 0 else 150 // i
        pitcher_surface = pitcher_texture.copy()
        catcher_surface = catcher_texture.copy()
        pitcher_surface.set_alpha(alpha)
        catcher_surface.set_alpha(alpha)
        screen.blit(pitcher_surface, (int(pitcher_pos[0] - 20), int(pitcher_pos[1] + y_offset - 20)))
        screen.blit(catcher_surface, (int(catcher_pos[0] - 20), int(catcher_pos[1] - y_offset - 20)))

    # Draw ball
    x = pitcher_pos[0] + (catcher_pos[0] - pitcher_pos[0]) * t
    y = pitcher_pos[1]
    screen.blit(ball_texture, (int(x - ball_radius), int(y - ball_radius)))
    for i in range(1, num_paths + 1):
        offset = i * planck_value * 5000
        y_offset = math.sin(t * math.pi + i) * offset if i % 2 == 0 else (4 * t * (1 - t)) * offset
        alpha = 150 // i
        ghost_surface = ghost_ball_texture.copy()
        ghost_surface.set_alpha(alpha)
        screen.blit(ghost_surface, (int(x - ball_radius // 2), int(y + y_offset - ball_radius // 2)))
        screen.blit(ghost_surface, (int(x - ball_radius // 2), int(y - y_offset - ball_radius // 2)))

    t += speed
    if t > 1:
        t = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()