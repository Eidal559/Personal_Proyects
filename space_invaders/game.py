import pygame
import random
import math
import os
import sys

# Initialize pygame
pygame.init()

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, 'assets')

def load_image(filename, scale=None):
    path = os.path.join(assets_dir, filename)
    try:
        image = pygame.image.load(path)
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Cannot load image: {path}")
        print(f"Pygame error: {e}")
        sys.exit()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = load_image('game_icon.png')
pygame.display.set_icon(icon)

# Player settings
playerImg = load_image('player_ship.png', (64, 64))  # Adjust size as needed
playerX = 370
playerY = 480
playerX_change = 0

# Enemy settings
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    img = load_image('enemy_ship.png', (64, 64))  # Adjust size as needed
    enemyImg.append(img)
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet settings
bulletImg = load_image('laser_bullet.png', (32, 32))  # Adjust size as needed
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # "ready" means you can't see the bullet, "fire" means it's moving

# Score settings
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Functions to display elements
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player_draw(x, y):
    screen.blit(playerImg, (x, y))

def enemy_draw(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27

# Main game loop
running = True
while running:
    # Screen background
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player boundary and movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy_draw(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player_draw(playerX, playerY)
    show_score(textX, textY)

    # Update the display
    pygame.display.update()
