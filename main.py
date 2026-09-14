import json
import random

import pygame

SAVE_FILE = "highscore.json"

WIDTH = 800
HEIGHT = 600
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GREEN = (0, 180, 0)
WHITE = (255, 255, 255)
BROWN = (200, 150, 80)

GROUND_HEIGHT = 50

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
    font = pygame.font.Font(None, 36)
    flap_sound = pygame.mixer.Sound("assets/flap.wav")
    hit_sound = pygame.mixer.Sound("assets/hit.wav")
    bird_image = pygame.image.load("assets/bird.png").convert_alpha()

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
    pipes = [{"top": top_pipe, "bottom": bottom_pipe, "scored": False}]
    spawn_timer = 0
    game_over = False
    score = 0

    try:
        with open(SAVE_FILE, "r") as f:
            save_data = json.load(f)
            best_score = save_data["best_score"]
    except FileNotFoundError:
        best_score = 0

    running = True
    while running:
        # 1. handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        bird_y = HEIGHT // 2
                        game_over = False
                        score = 0
                        spawn_timer = 0
                        pipes = [{
                            "top": pygame.Rect(PIPE_X, 0, PIPE_WIDTH, top_pipe_height),
                            "bottom": pygame.Rect(PIPE_X, GAP_Y + PIPE_GAP, PIPE_WIDTH, bottom_pipe_height),
                            "scored": False,
                        }]

                    bird_velocity = FLAP_STRENGTH
                    flap_sound.play()
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

            for pipe in pipes:
                pipe["top"].x -= PIPE_SPEED
                pipe["bottom"].x -= PIPE_SPEED

            spawn_timer += 1

            if spawn_timer >= PIPE_SPAWN_INTERVAL:
                spawn_timer = 0
                new_gap_y = random.randint(GAP_MARGIN, HEIGHT - PIPE_GAP - GAP_MARGIN)
                new_top_height = new_gap_y
                new_bottom_height = HEIGHT - (new_gap_y + PIPE_GAP)

                new_top = pygame.Rect(WIDTH, 0, PIPE_WIDTH, new_top_height)
                new_bottom = pygame.Rect(WIDTH, new_gap_y + PIPE_GAP, PIPE_WIDTH, new_bottom_height)
                pipes.append({"top": new_top, "bottom": new_bottom, "scored": False})

            kept_pipes = []
            for pipe in pipes:
                if pipe["top"].x > -PIPE_WIDTH:
                    kept_pipes.append(pipe)
            pipes = kept_pipes

            for pipe in pipes:
                if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
                    game_over = True
                    hit_sound.play()

            for pipe in pipes:
                if not pipe["scored"] and pipe["top"].x + PIPE_WIDTH < bird_x:
                    pipe["scored"] = True
                    score += 1

            if score > best_score:
                best_score = score
                with open(SAVE_FILE, "w") as f:
                    json.dump({"best_score": best_score}, f)

            if bird_y + BIRD_RADIUS >= HEIGHT - GROUND_HEIGHT:
                game_over = True
                hit_sound.play()

        # 3. draw
        screen.fill(SKY_BLUE)
        bird_draw_rect = bird_image.get_rect(center=(bird_x, bird_y))
        screen.blit(bird_image, bird_draw_rect)
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe["top"])
            pygame.draw.rect(screen, GREEN, pipe["bottom"])
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        score_text = font.render(f"Score: {score}   Best: {best_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if not started:
            start_text = font.render("Press SPACE to start", True, WHITE)
            screen.blit(start_text, (200, 250))

        if game_over:
            game_over_text = font.render(f"Game Over! Score: {score}", True, WHITE)
            screen.blit(game_over_text, (200, 250))
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(restart_text, (200, 300))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
