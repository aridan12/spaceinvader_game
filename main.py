import pygame
from pygame import mixer
import random
import math

# Initialize the pygame
pygame.init()

# create the screen | 800 = width (X), 600 = height (Y)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders")  # Add title to the game
icon = pygame.image.load('favicon.png')  # Add Favicon to the game
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('background.jpg')  # Add Favicon to the game

# Background Sound
mixer.music.load('background_music.mp3')
mixer.music.play(-1)  # -1 will play it on loop


# Player
playerImg = pygame.image.load('player.png')
playerImgSize = 64  # player image size is 64 x 64 pixels
playerX = 0.4625 * screen_width  # playerX currently is 370
playerY = 0.8 * screen_height  # playX currently is 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

enemyImgSize = 64  # enemy image size is 64 x 64 pixels

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, screen_width - enemyImgSize))
    enemyY.append(random.randint((screen_height / 12), (screen_height / 4)))  # 50, 150
    enemyX_change.append(0.8)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletImgSize = 32  # enemy image size is 32 x 32 pixels
bulletX = 0
bulletY = 0.8 * screen_height  # 480 the top corner (Y) of our player
bulletX_change = 0
bulletY_change = 1.2
bullet_state = "ready"  # Bullet doesn't show in the screen

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text

game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    enemy(2000, 2000, i)
    screen.blit(over_text, (200, 250))



def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# bullet_state = "fire"  # Bullet is currently moving


def player(x, y):
    screen.blit(playerImg, (x, y))  # .blit() - drawing an image of the player in the screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # .blit() - drawing an image of the enemy in the screen


def fire_bullet(x, y):
    global bullet_state  # global allows us to use the bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # The bullet will appear in the center of the spaceship


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))  # Change the background-color of the game - RGB colors (from 0-255)
    # Adding background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # once the user press X and close the screen, exit.

        #  If key-stroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:  # KEYDOWN is pressing on the key #KEYUP is releasing the press
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8  # if the size of the screen is bigger/smaller than speed should change
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Getting the X coordinates of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #  Creating boundaries for the player
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_width - playerImgSize:  # (Currently 800 screen width - 64 pixels player image size = 736)
        playerX = screen_width - playerImgSize

    # Creating enemy movement

    for i in range(num_of_enemies):

        # Game Over

        if enemyY[i] > 440:
            screen.blit(background, (0, 0))
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screen_width - enemyImgSize:  # (800 screen width - 64 pixels player image size = 736)
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]

        # Collision

        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)  # True / False
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 0.8 * screen_height  # 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, screen_width - enemyImgSize)
            enemyY[i] = random.randint((screen_height / 12), (screen_height / 4))

        enemy(enemyX[i], enemyY[i], i)  # Calling enemy function

    # Bullet movement
    if bulletY <= 0:  # allowing us to shoot multiple bullets
        bulletY = 0.8 * screen_height  # 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # Calling player function so it will be shown on our screen as long as the game is active
    show_score(textX, textY)
    pygame.display.update()
