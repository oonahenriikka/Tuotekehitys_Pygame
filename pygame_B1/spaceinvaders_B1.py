import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 900
PLAYER_SIZE = 100
ENEMY_SIZE = 30
BULLET_SIZE = 5
PLAYER_SPEED = 5
ENEMY_SPEED = {"easy": 2, "normal": 4, "hard": 6}
BULLET_SPEED = 7
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game states
MAIN_MENU = "main_menu"
PLAYING = "playing"
GAME_OVER = "game_over"
current_state = MAIN_MENU

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Player
imported_image = pygame.image.load(r"C:\Users\oonah\OneDrive\Tiedostot\Tieto- ja viestintätekniikka\Tuotekehitys_Pygame\pygame_B1\pmodel.png")
player_image = pygame.transform.scale(imported_image, (100, 100))
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
player_speed = PLAYER_SPEED

# Enemies
enemies = []

# Bullets
bullets = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Hide the cursor
pygame.mouse.set_visible(False)

mouse_x, mouse_y = pygame.mouse.get_pos()

# Main menu loop
while current_state == MAIN_MENU:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                current_state = PLAYING
                player_speed = ENEMY_SPEED["easy"]
            elif event.key == pygame.K_n:
                current_state = PLAYING
                player_speed = ENEMY_SPEED["normal"]
            elif event.key == pygame.K_h:
                current_state = PLAYING
                player_speed = ENEMY_SPEED["hard"]

    screen.fill(BLACK)

    # Draw menu text
    title_text = font.render("Space Invaders", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))
    easy_text = font.render("Press 'E' for Easy", True, WHITE)
    normal_text = font.render("Press 'N' for Normal", True, WHITE)
    hard_text = font.render("Press 'H' for Hard", True, WHITE)
    screen.blit(easy_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(normal_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
    screen.blit(hard_text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))

    pygame.display.flip()

    clock.tick(FPS)

# Reset game variables for a new game
player.x = WIDTH // 2 - PLAYER_SIZE // 2
player.y = HEIGHT - 2 * PLAYER_SIZE
enemies = []
bullets = []
score = 0
paused = False

# Playing loop
while current_state == PLAYING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shoot bullet
                bullet = pygame.Rect(player.centerx - BULLET_SIZE // 2, player.y, BULLET_SIZE, BULLET_SIZE)
                bullets.append(bullet)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # 'P' key is pressed
                # Toggle pause
                paused = not paused

    # Pause the game
    if paused:
        # Skip the rest of the game loop
        continue
    
    # Get mouse position
    mouse_x, _ = pygame.mouse.get_pos()
   

    player.x = mouse_x - PLAYER_SIZE // 2
    player.y = HEIGHT - PLAYER_SIZE  # Set a fixed y-position if needed, or use mouse_y for variable y-position

    if not enemies:
        enemies = [pygame.Rect(random.randint(0, WIDTH - ENEMY_SIZE), random.randint(0, HEIGHT // 2), ENEMY_SIZE, ENEMY_SIZE) for _ in range(5)]

    # Update enemies
    for enemy in enemies:
        enemy.y += player_speed
        if enemy.y > HEIGHT:
            enemy.y = 0
            enemy.x = random.randint(0, WIDTH - ENEMY_SIZE)

        # Check collision with bullets
        for bullet in bullets:
            if enemy.colliderect(bullet):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10

    # Update bullets
    for bullet in bullets:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

    # Check collision with player
    for enemy in enemies:
        if player.colliderect(enemy):
            current_state = GAME_OVER

    # Draw everything
    screen.fill(BLACK)
    player_image_rect = player_image.get_rect(center=(player.x + PLAYER_SIZE // 2, player.y + PLAYER_SIZE // 2))
    screen.blit(player_image, player_image_rect)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    # Draw the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    #Draw the pause
    pause_text = font.render("Press 'P' to Pause", True, WHITE)
    screen.blit(pause_text, (WIDTH - pause_text.get_width() - 10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Game over loop
while current_state == GAME_OVER:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)

    # Draw game over text
    game_over_text = font.render(f"Game Over - Your Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 50))
    restart_text = font.render("Press 'R' to Restart", True, WHITE)
    quit_text = font.render("Press 'Q' to Quit", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                # Quit the game
                pygame.quit()
                sys.exit()

    # Restart incomplete
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x, self.rect.y))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    clock.tick(FPS)