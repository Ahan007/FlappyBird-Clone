import pygame
import random

# Initialize Pygame and the mixer for sound
pygame.init()
pygame.mixer.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 100, HEIGHT // 2
PIPE_WIDTH = 70
PIPE_SPEED = 5
PIPE_GAP = 150
GRAVITY = 0.5
JUMP_STRENGTH = -8

# Create Game Window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load Images (ensure these files are in your project folder)
bg_img = pygame.image.load("background.png")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (50, 35))

pipe_img = pygame.image.load("pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, 400))

ground_img = pygame.image.load("ground.png")
ground_img = pygame.transform.scale(ground_img, (WIDTH, 50))

# Load Sound Files (ensure these .wav files are in your project folder)
swoosh_sound = pygame.mixer.Sound("swoosh.wav")  # Updated jump sound
hit_sound = pygame.mixer.Sound("hit.wav")
point_sound = pygame.mixer.Sound("point.wav")

# Initialize Game Variables
def reset_game():
    global bird_y, bird_velocity, pipe_x, pipe_height, score, running
    bird_y = BIRD_Y
    bird_velocity = 0
    pipe_x = WIDTH
    pipe_height = random.randint(150, 350)
    score = 0
    running = True

reset_game()
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Main Game Loop
while True:
    win.blit(bg_img, (0, 0))  # Draw Background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            # Bird jump when SPACE is pressed
            if event.key == pygame.K_SPACE and running:
                bird_velocity = JUMP_STRENGTH
                swoosh_sound.play()
            # Restart game when R is pressed
            if event.key == pygame.K_r and not running:
                reset_game()

    if running:
        # Update Bird
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Update Pipe Position
        pipe_x -= PIPE_SPEED
        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_height = random.randint(150, 350)
            score += 1
            point_sound.play()

        # Draw Pipes (Top and Bottom)
        win.blit(pipe_img, (pipe_x, pipe_height - 400))  # Top Pipe
        win.blit(pipe_img, (pipe_x, pipe_height + PIPE_GAP))  # Bottom Pipe

        # Draw Bird
        win.blit(bird_img, (BIRD_X, bird_y))

        # Draw Ground at the bottom
        win.blit(ground_img, (0, HEIGHT - 50))

        # Collision Detection
        if (bird_y <= 0 or bird_y >= HEIGHT - 50) or \
           (BIRD_X + 50 > pipe_x and BIRD_X < pipe_x + PIPE_WIDTH and (bird_y < pipe_height or bird_y + 35 > pipe_height + PIPE_GAP)):
            hit_sound.play()
            running = False  # End game on collision

    else:
        # Display Game Over message and restart option
        over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        win.blit(over_text, (WIDTH // 6, HEIGHT // 2))

    # Display Score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)  # Set FPS to 30




