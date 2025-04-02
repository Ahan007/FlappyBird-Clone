# FlappyBird-Clone
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 100, HEIGHT // 2
PIPE_WIDTH = 70
PIPE_SPEED = 5
PIPE_GAP = 150
GRAVITY = 0.5
JUMP_STRENGTH = -8

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

bg_img = pygame.image.load("background-night.png")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

bird_frames = [
    pygame.image.load("bluebird-downflap.png"),
    pygame.image.load("bluebird-midflap.png"),
    pygame.image.load("bluebird-upflap.png")
]
bird_frames = [pygame.transform.scale(img, (50, 35)) for img in bird_frames]

pipe_img = pygame.image.load("pipe-green.png")
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, 400))

ground_img = pygame.image.load("base.png")
ground_img = pygame.transform.scale(ground_img, (WIDTH, 50))

gameover_img = pygame.image.load("gameover.png")


def reset_game():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, running, bird_frame_index
    bird_y = BIRD_Y
    bird_velocity = 0
    pipe_x = WIDTH
    pipe_height = random.randint(150, 350)
    score = 0
    running = True
    bird_frame_index = 0

reset_game()
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

while True:
    win.blit(bg_img, (0, 0))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and running:
                bird_velocity = JUMP_STRENGTH
            if not running and event.key == pygame.K_r:
                reset_game()

    if running:
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        bird_frame_index = (bird_frame_index + 1) % 3
        bird_img = bird_frames[bird_frame_index]

        pipe_x -= PIPE_SPEED
        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_height = random.randint(150, 350)
            score += 1

        win.blit(pipe_img, (pipe_x, pipe_height - 400))  
        win.blit(pipe_img, (pipe_x, pipe_height + PIPE_GAP))  

        win.blit(bird_img, (BIRD_X, bird_y))

        win.blit(ground_img, (0, HEIGHT - 50))

        if (bird_y <= 0 or bird_y >= HEIGHT - 50) or \
           (BIRD_X + 50 > pipe_x and BIRD_X < pipe_x + PIPE_WIDTH and 
            (bird_y < pipe_height or bird_y + 35 > pipe_height + PIPE_GAP)):
            running = False  

    else:
        win.blit(gameover_img, ((WIDTH - gameover_img.get_width()) // 2, HEIGHT // 3))
        restart_text = font.render("Press R to Restart", True, (255, 0, 0))
        win.blit(restart_text, (WIDTH // 4, HEIGHT // 2))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)
