import pygame

WIDTH = 800
HEIGHT = 600
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)


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

        # 2. update physics (every frame, but only once the game has started)
        if started:
            bird_velocity = bird_velocity + GRAVITY
            if bird_velocity > MAX_FALL_SPEED:
                bird_velocity = MAX_FALL_SPEED

            bird_y = bird_y + bird_velocity

            if bird_y < 0:
                bird_y = 0
                bird_velocity = 0

        # 3. draw
        screen.fill(SKY_BLUE)
        pygame.draw.circle(screen, YELLOW, (bird_x, bird_y), 20)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
