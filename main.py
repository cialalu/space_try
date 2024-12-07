import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Wordle")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load assets
background = pygame.image.load("background.jpg")
ship_img = pygame.image.load("ship.png")
laser_img = pygame.image.load("laser.png")
enemy_imgs = [
    pygame.image.load(f"enemy{i}_1.png") for i in range(1, 4)
]
explosion_imgs = {
    "blue": pygame.image.load("explosionblue.png"),
    "green": pygame.image.load("explosiongreen.png"),
    "purple": pygame.image.load("explosionpurple.png")
}

# Scaling assets
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
ship_img = pygame.transform.scale(ship_img, (50, 50))
laser_img = pygame.transform.scale(laser_img, (5, 20))
enemy_imgs = [pygame.transform.scale(img, (50, 50)) for img in enemy_imgs]
explosion_imgs = {key: pygame.transform.scale(img, (50, 50)) for key, img in explosion_imgs.items()}

# Clock
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.Font(None, 36)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 60)
        self.speed = 5
        self.lasers = pygame.sprite.Group()
        self.shield = False
        self.triple_shot = False
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        if self.triple_shot:
            offsets = [-15, 0, 15]
            for offset in offsets:
                laser = Laser(self.rect.centerx + offset, self.rect.top)
                self.lasers.add(laser)
        else:
            laser = Laser(self.rect.centerx, self.rect.top)
            self.lasers.add(laser)

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type_):
        super().__init__()
        self.type = type_
        self.image = pygame.Surface((30, 30))  # Create a temporary surface
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

        # Load shield image for the "shield" power-up
        if self.type == "shield":
            self.image = pygame.image.load("shield.png")  # Load shield.png image
            self.image = pygame.transform.scale(self.image, (30, 30))  # Scale to fit
        elif self.type == "triple_shot":
            self.image = pygame.image.load("triple_shot.png")  # Load shield.png image
            self.image = pygame.transform.scale(self.image, (30, 30))  # Scale to fit
        elif self.type == "speed_boost":
            self.image = pygame.image.load("speed_boost.png")  # Load shield.png image
            self.image = pygame.transform.scale(self.image, (30, 30))  # Scale to fit
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Groups
player = Player()
all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Enemy spawn timer
enemy_spawn_time = 1000  # Spawn an enemy every second
last_enemy_spawn = pygame.time.get_ticks()

# Power-up timer
powerup_spawn_time = 5000  # Spawn a power-up every 5 seconds
last_powerup_spawn = pygame.time.get_ticks()

# Level system
level = 1
enemies_to_clear = 15
cleared_enemies = 0
score = 0

def show_level_menu(level):
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        title_text = font.render(f"Level {level} Cleared!", True, WHITE)
        option_text1 = font.render("Press N to proceed to the next level", True, WHITE)
        option_text2 = font.render("Press R to restart", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(option_text1, (WIDTH // 2 - option_text1.get_width() // 2, HEIGHT // 2))
        screen.blit(option_text2, (WIDTH // 2 - option_text2.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    menu_running = False
                    return "next"
                if event.key == pygame.K_r:
                    menu_running = False
                    return "restart"

def show_start_screen():
    start_screen_running = True
    while start_screen_running:
        screen.fill(BLACK)
        title_text = font.render("Welcome to Space Wordle!", True, WHITE)
        instruction_text1 = font.render("Use LEFT and RIGHT arrows to move.", True, WHITE)
        instruction_text2 = font.render("Press SPACE to shoot.", True, WHITE)
        start_text = font.render("Press S to Start", True, GREEN)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(instruction_text1, (WIDTH // 2 - instruction_text1.get_width() // 2, HEIGHT // 2))
        screen.blit(instruction_text2, (WIDTH // 2 - instruction_text2.get_width() // 2, HEIGHT // 2 + 40))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start_screen_running = False

# Show start screen
show_start_screen()

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Spawn enemies
    if pygame.time.get_ticks() - last_enemy_spawn > enemy_spawn_time:
        x = random.randint(0, WIDTH - 50)
        y = random.randint(-100, -40)
        enemy = Enemy(x, y, random.choice(enemy_imgs))
        all_sprites.add(enemy)
        enemies.add(enemy)
        last_enemy_spawn = pygame.time.get_ticks()

    # Spawn power-ups
    if pygame.time.get_ticks() - last_powerup_spawn > powerup_spawn_time:
        x = random.randint(0, WIDTH - 30)
        y = random.randint(-100, -40)
        type_ = random.choice(["shield", "triple_shot", "speed_boost"])
        powerup = PowerUp(x, y, type_)
        all_sprites.add(powerup)
        powerups.add(powerup)
        last_powerup_spawn = pygame.time.get_ticks()

    # Updates
    all_sprites.update()
    player.lasers.update()

    # Collision: Laser hits enemy
    for laser in player.lasers:
        hits = pygame.sprite.spritecollide(laser, enemies, True)
        for hit in hits:
            laser.kill()
            cleared_enemies += 1
            score += 10

    # Collision: Player collects power-up
    powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
    for powerup in powerup_hits:
        if powerup.type == "shield":
            player.shield = True
        elif powerup.type == "triple_shot":
            player.triple_shot = True
        elif powerup.type == "speed_boost":
            player.speed += 2

    # Collision: Player collides with enemy
    enemy_hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in enemy_hits:
        if player.shield:
            player.shield = False
        else:
            player.lives -= 1
            if player.lives <= 0:
                running = False

    # Level progression
    if cleared_enemies >= enemies_to_clear:
        level += 1
        cleared_enemies = 0
        enemies_to_clear += 10
        choice = show_level_menu(level - 1)
        if choice == "restart":
            level = 1
            cleared_enemies = 0
            enemies_to_clear = 15
            score = 0
            player.lives = 3
            player.speed = 5
            player.shield = False
            player.triple_shot = False
            all_sprites.empty()
            all_sprites.add(player)
            enemies.empty()
            powerups.empty()
        if level > 3:
            print("You Win!")
            running = False

    # Draw
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    player.lasers.draw(screen)

    # Display HUD
    hud_text = font.render(f"Level: {level}  Score: {score}  Lives: {player.lives}", True, WHITE)
    screen.blit(hud_text, (10, 10))
    powerup_status = f"Shield: {'ON' if player.shield else 'OFF'} | Triple Shot: {'ON' if player.triple_shot else 'OFF'} | Speed: {player.speed}"
    powerup_text = font.render(powerup_status, True, WHITE)
    screen.blit(powerup_text, (10, 50))

    # Flip display
    pygame.display.flip()

pygame.quit()
sys.exit()

