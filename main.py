import pygame
import random
from pygame import mixer

# Initialize the Pygame
pygame.init()

# Creating a scree of (width, height)/ (x,y)
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (800,600))

# Title and Icon
pygame.display.set_caption("Space Invadors")

icon = pygame.image.load("assets/ufo.png")
pygame.display.set_icon(icon)

# Adding Image (Player in this case)
playerImage = pygame.image.load("assets/player.png")
playerImage = pygame.transform.scale(playerImage, (64,64)) # Scaling image to 64x64
playerX = 370
playerY = 480
playerX_change = 0

# Adding Enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = 0.05
enemyY_change =[]

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load("assets/enemy.png"))
    enemyImage[i] = pygame.transform.scale(enemyImage[i], (64,64)) # Scaling image to 64x64
    enemyX.append(random.randint(0, 740))
    enemyY.append(random.randint(0, 150))
    enemyY_change.append(50)

# Bullet
bulletImage = pygame.image.load("assets/bulletImg.png")
bulletX = 0
bulletY = 480
bulletY_change = 0.5
bulletState = "ready" # There will be two states "ready" --> static position behind ship | "fire" --> moving


# Score
scoreValue = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def showScore(x,y):
    score = font.render(f"Score: {scoreValue}", True, (255,255,255))
    screen.blit(score, (x,y))

def gameOverText():
    overText = over_font.render(f"Game Over", True, (255,0,0))
    screen.blit(overText, (200,100))

def player(x,y):
    screen.blit(playerImage, (x, y))
    # The blit function is used to draw anything on screen at position x and y
def enemy(image, x,y):
    if x and y:
        screen.blit(image, (x,y))

def fireBullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImage, (x+15, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = ((enemyX-bulletX)**2 + (enemyY-bulletY)**2)**0.5
    if distance < 27:
        return True
    else:
        return False



gameOverPlayed = False
# Game Loop
running = True
while running:
    # Adding color in the screen (r,g,b)
    screen.fill((0,0,0))

    # Background Image
    screen.blit(background, (0,0))
    
    # Checking all the events on screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # This event is pressing the cross button of the opened tab
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.1
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.1
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    fireSound = mixer.Sound("assets/laser.mp3")
                    fireSound.play()
                    fireBullet(playerX,playerY)
                    bulletX = playerX
            
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] >400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            
            gameOverText()
            if not gameOverPlayed:
                gameOverSound = mixer.Sound("assets/gameOver.mp3")
                gameOverSound.play()
                gameOverPlayed = True
            break


        enemyX[i] += enemyX_change
        if enemyX[i] > 760:
            enemyX_change = -0.05   
            enemyY[i] += 50
        elif enemyX[i] < 0:
            enemyX_change = 0.05
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Adding killing sound
            explosionSound = mixer.Sound("assets/kill.mp3")
            explosionSound.play()
            bulletY = playerY
            # bulletX = playerX
            bulletState = "ready"
            scoreValue += 1
            enemyX[i] = random.randint(0,740)
            enemyY[i] = random.randint(0,150)
    
        # Adding enemy image to the sccreen
        enemy(enemyImage[i], enemyX[i], enemyY[i])
                
    # Bullet Movement
    if bulletY < 0:
        bulletX = playerX
        bulletY = playerY
        bulletState = "ready"
    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Checking for player position so it doesn't go outside the screen
    playerX += playerX_change
    if playerX > 736:
        playerX = 736
    elif playerX < 0:
        playerX = 0


    
    # Adding image to Screen(see the player function)
    player(playerX, playerY) 
    showScore(textX, textY)
    pygame.display.update()