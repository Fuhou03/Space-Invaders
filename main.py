import pygame
import random
import math
from pygame import mixer

# Screen and Background
pygame.init()
screen = pygame.display.set_mode((800, 600))  # width and height
background = pygame.image.load('background.jpg')

pygame.display.set_caption("Space Invaders")  # Screen Title
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)  # Sets the small icon next to window title

mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 loops it


# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 490
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien2.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)



# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletY = 480
bulletX = 0
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"  # Ready - can't see on screen.  Fire - currently moving

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)  # Font and size
textX = 10
textY = 10

def show_score(x, y):
    score = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))  # Render not blit
    screen.blit(score, (x, y))

# Game Over
gameover_font = pygame.font.Font("freesansbold.ttf", 60)  # Font and size

def game_over():
    gameover_text = gameover_font.render("GAME OVER", True, (255, 255, 255))  # Render not blit
    screen.blit(gameover_text, (200, 250))


# Put player and enemy onto screen
def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means to draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_Collision(eX, eY, bX, bY):  # If bullet and enemy collide
    distance = math.sqrt((math.pow(eX - bX, 2)) + (math.pow(eY - bY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))  # background colour
    screen.blit(background, (0, 0))  # put background on screen

    for event in pygame.event.get():  # gets all the events happening e.g a keypress
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # if left arrow is pressed
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:  # right arrow pressed
                playerX_change = 0.3

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":  # So you can only shoot once the bullet hits top
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX  # Gets current x coord of spaceship
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # keystroke released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # Stops moving

    playerX += playerX_change  # Moves the player

    # Stops player when it reaches edge of window
    if playerX <= 0:
        playerX = 0
    elif playerX >= (800 - 64):  # spaceship is 64 pixels
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000    # Gets rid of them (off screen)
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # Enemy moves in opposite direction after it hits the edge
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]  # Moves down after hitting edge
        elif enemyX[i] >= (800 - 64):
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:  # When we hit an enemy
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()  # Don't add -1 so that it only plays once

            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)  # Spawn enemy in random spot after it's hit
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:  # Allows you to shoot multiple bullets
        bulletY = 480  # Resets y coord
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # So the window updates during gameplay
