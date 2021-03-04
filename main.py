import pygame
from pygame import mixer
import random
import math

# Initialises Pygame in the project
pygame.init()
# Create a screen
screen = pygame.display.set_mode((800, 600))

# Score
scoreValue = 0
font = pygame.font.Font("freesansbold.ttf", 32)  # Set the properties of the font

# Select position of text
textX = 10
textY = 10


def showScore(x, y):
    score = font.render("Score : " + str(scoreValue), True, (255, 255, 255))  # Makes a rendered text object
    screen.blit(score, (x, y))  # Displays the text object on the screen


# Title and icon
pygame.display.set_caption("Space Geezers")
pygame.display.set_icon(pygame.image.load("arcadeMachIcon.png"))

# Background
background = pygame.image.load("space.png")

# Background music
mixer.music.load("backgroundMusic.wav")
mixer.music.play(-1)

# Player
playerImg = pygame.image.load("spaceShip64.png")
playerX = 368
playerY = 480
playerX_move = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_move = []
enemyY_move = []
enemyNum = 6

for i in range(enemyNum):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_move.append(4)
    enemyY_move.append(40)

# Bullet
# ready - You cant see the bullet on the screen
# fire - The bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_move = 0
bulletY_move = 10
bulletState = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 17, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game over
overFont = pygame.font.Font("freesansbold.ttf", 64)
def gameOverText():
    overText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (200, 250))


# Game loop
running = True
while running:
    # Change colour of screen. Uses RGB
    screen.fill((255, 115, 124))
    # Background image
    screen.blit(background, (0, 0))

    # Detects events in the game
    for event in pygame.event.get():
        # Checks for the exit button being pressed
        if event.type == pygame.QUIT:
            running = False
        # Detects any key press but not what specific key is pressed
        if event.type == pygame.KEYDOWN:
            # Checks to see if the key pressed was the left arrow key
            if event.key == pygame.K_LEFT:
                playerX_move = -4
            # Checks to see if the key pressed was the right arrow key
            if event.key == pygame.K_RIGHT:
                playerX_move = 4
            if event.key == pygame.K_SPACE:
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                # If statement stops the already existing bullet from skipping
                if bulletState == "ready":
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
        # Detects any releases of a key
        if event.type == pygame.KEYUP:
            # Checks if the key releases was the left or right arrow key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0

    # Updates the screen and realises movement
    playerX += playerX_move
    # Stops the player from going off the sides of the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800 (width of the screen) - 64 (the width of the player image)
        playerX = 736

    # Enemy movement
    for i in range(enemyNum):

        # Game over
        if enemyY[i] > 200:
            for j in range(enemyNum):
                enemyY[j] = 2000
            gameOverText()
            break

        # Moves all of the enemies
        enemyX[i] += enemyX_move[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyY[i] += enemyY_move[i]
            enemyX_move[i] = 4
        elif enemyX[i] >= 736:  # 800 (width of the screen) - 64 (the width of the player image)
            enemyX[i] = 736
            enemyY[i] += enemyY_move[i]
            enemyX_move[i] = -4

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:  # If collision is True
            bulletY = 480
            bulletState = "ready"
            scoreValue += 1
            print(scoreValue)
            # Resets the enemy position after being shot
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Updates the enemies position on the screen by calling the function
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    # If the bullet has left the screen
    if bulletY <= -32:  # I use -32 so the bullet leaves the screen before resetting.
        bulletY = 480  # Position of the player
        bulletState = "ready"
    # If a bullet is currently being fired
    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_move

    showScore(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
