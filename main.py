import random

import pygame

WIDTH = 800
HEIGHT = 600
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GREEN = (0, 180, 0)

PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 5
PIPE_SPAWN_INTERVAL = 90  # frames between new pipes (60fps, so ~1.5 seconds)
BIRD_RADIUS = 20
GAP_MARGIN = 50  # smallest allowed pipe segment height, top or bottom


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird_x = WIDTH // 2
    bird_y = HEIGHT // 2
    bird_velocity = 0
    started = False

    GRAVITY = 0.5
    FLAP_STRENGTH = -10
    MAX_FALL_SPEED = 10

    # -- Step 4a: one static pipe pair, just to see the shape --
    PIPE_X = 600
    GAP_Y = 200  # top edge of the gap

    top_pipe_height = GAP_Y
    bottom_pipe_height = HEIGHT - (GAP_Y + PIPE_GAP)

    top_pipe = pygame.Rect(PIPE_X, 0, PIPE_WIDTH, top_pipe_height)
    bottom_pipe = pygame.Rect(PIPE_X, GAP_Y + PIPE_GAP, PIPE_WIDTH, bottom_pipe_height)
    pipes = [(top_pipe, bottom_pipe)]
    spawn_timer = 0
    game_over = False

    running = True
    while running:
        # 1. handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = FLAP_STRENGTH
                    started = True

        # 2. update physics (every frame, but only once the game has started, and not after a collision)
        if started and not game_over:
            bird_velocity = bird_velocity + GRAVITY
            if bird_velocity > MAX_FALL_SPEED:
                bird_velocity = MAX_FALL_SPEED

            bird_y = bird_y + bird_velocity

            if bird_y < 0:
                bird_y = 0
                bird_velocity = 0

            bird_rect = pygame.Rect(bird_x - BIRD_RADIUS, bird_y - BIRD_RADIUS, BIRD_RADIUS * 2, BIRD_RADIUS * 2)

            for top, bottom in pipes:
                top.x -= PIPE_SPEED
                bottom.x -= PIPE_SPEED

            spawn_timer += 1

            if spawn_timer >= PIPE_SPAWN_INTERVAL:
                spawn_timer = 0
                new_gap_y = random.randint(GAP_MARGIN, HEIGHT - PIPE_GAP - GAP_MARGIN)
                new_top_height = new_gap_y
                new_bottom_height = HEIGHT - (new_gap_y + PIPE_GAP)

                new_top = pygame.Rect(WIDTH, 0, PIPE_WIDTH, new_top_height)
                new_bottom = pygame.Rect(WIDTH, new_gap_y + PIPE_GAP, PIPE_WIDTH, new_bottom_height)
                pipes.append((new_top, new_bottom))

            kept_pipes = []
            for top, bottom in pipes:
                if top.x > -PIPE_WIDTH:
                    kept_pipes.append((top, bottom))
            pipes = kept_pipes

            for top, bottom in pipes:
                if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                    game_over = True

            if bird_y + BIRD_RADIUS >= HEIGHT:
                game_over = True

        # 3. draw
        screen.fill(SKY_BLUE)
        pygame.draw.circle(screen, YELLOW, (bird_x, bird_y), BIRD_RADIUS)
        for top, bottom in pipes:
            pygame.draw.rect(screen, GREEN, top)
            pygame.draw.rect(screen, GREEN, bottom)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
