import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants
BALL_RADIUS = 10
PEG_RADIUS = 5
PEG_SPACING = 50
ROWS = 10
COLS = WIDTH // PEG_SPACING
GRAVITY = 0.5

# Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = 0

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > WIDTH:
            self.vx *= -1

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), BALL_RADIUS)

# Generate pegs
pegs = []
for row in range(ROWS):
    for col in range(COLS):
        x = col * PEG_SPACING + (PEG_SPACING // 2 if row % 2 == 0 else 0)
        y = row * PEG_SPACING + PEG_SPACING
        if x < WIDTH:
            pegs.append((x, y))

# Main loop
clock = pygame.time.Clock()
balls = []
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(Ball(event.pos[0], event.pos[1]))

    # Update and draw balls
    for ball in balls:
        ball.update()
        ball.draw()

        # Check collision with pegs
        for peg in pegs:
            dx = ball.x - peg[0]
            dy = ball.y - peg[1]
            distance = (dx**2 + dy**2)**0.5
            if distance < BALL_RADIUS + PEG_RADIUS:
                ball.vx *= -1
                ball.vy *= -1

    # Draw pegs
    for peg in pegs:
        pygame.draw.circle(screen, BLUE, peg, PEG_RADIUS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()