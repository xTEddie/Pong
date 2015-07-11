import pygame
import time
import math

## Colors
WHITE = (255,255,255)
BLACK= (0,0,0)
RED = (255,0,0)
GREEN = (0,100,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

## variables
NAME = "Pong"
DISPLAY_WIDTH = 800 ## DEFAULT = 800
DISPLAY_HEIGHT = 600 ## DEFAULT = 600
PADDLE_WIDTH = 80 ## DEFAULT = 60
PADDLE_HEIGHT = 10
PADDLE_OFFSET = 50
BALL_SIZE = 10
FPS = 30

pygame.init()

## fonts
SMALL_FONT = pygame.font.SysFont("comicsansms", 25, True) 
MEDIUM_FONT = pygame.font.SysFont("comicsansms", 50, True) 
LARGE_FONT = pygame.font.SysFont("comicsansms", 80, True)

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(NAME) 
clock = pygame.time.Clock()

def getTextSurface(text, color, size):
    ## Draw text on a new Surface
    if size == "small":
        textSurface = SMALL_FONT.render(text, True, color) 
    elif size == "medium":
        textSurface = MEDIUM_FONT.render(text, True, color)
    elif size == "large":
        textSurface = LARGE_FONT.render(text, True, color)
    return textSurface, textSurface.get_rect()

def blitText(msg, color, x_displace=0, y_displace=0, size="small"):
    ## Draw surface on another surface
    textSurf, textRect = getTextSurface(msg, color, size)
    textRect.center = (DISPLAY_WIDTH/2) + x_displace, (DISPLAY_HEIGHT/2) + y_displace
    gameDisplay.blit(textSurf, textRect) 

def drawArena():
    gameDisplay.fill(BLACK)

def drawPaddle(paddle, color):
    pygame.draw.rect(gameDisplay, color, paddle)

def movePaddle(paddle, paddleX):
    ## Make sure paddle does not go off screen
    if paddleX < 0:
        paddle.x = 0
    elif paddleX + PADDLE_WIDTH > DISPLAY_WIDTH:
        paddle.x = DISPLAY_WIDTH - PADDLE_WIDTH 
    else:    
        paddle.x = paddleX
    return paddle
    
def drawBall(ball):
    pygame.draw.rect(gameDisplay, YELLOW, ball)

def updateScore(score):
    text = SMALL_FONT.render(str(score), True, WHITE)
    gameDisplay.blit(text, [DISPLAY_WIDTH/2 - text.get_size()[0]/2,0])

def moveBall(ball, ballX, ballY):
    ball.x = ballX
    ball.y = ballY
    return ball

def checkHitBall(ball, paddlePlayer, paddleComp):
    global paddleHit
    if ball.y + BALL_SIZE > paddlePlayer.y and ball.y + BALL_SIZE < paddlePlayer.y + PADDLE_HEIGHT:
        if ball.x + BALL_SIZE > paddlePlayer.x and ball.x + BALL_SIZE < paddlePlayer.x + PADDLE_WIDTH or ball.x > paddlePlayer.x and ball.x < paddlePlayer.x + PADDLE_WIDTH:
            paddleHit = "Player"
            return True
    elif ball.y < paddleComp.y + PADDLE_HEIGHT and ball.y > paddleComp.y:
        if ball.x + BALL_SIZE > paddleComp.x and ball.x + BALL_SIZE < paddleComp.x + PADDLE_WIDTH or ball.x > paddleComp.x and ball.x < paddleComp.x + PADDLE_WIDTH:
            paddleHit = "Comp"
            return True
    else:
        return False

def checkEdgeCollision(ball):
    if ball.x < 0:
        return True
    elif ball.x + BALL_SIZE > DISPLAY_WIDTH:
        return True
    else:
        return False
    
def getPaddleAngle(ball, paddle):
    portion = ball.x + BALL_SIZE/2 - paddle.x
    ratio = portion/PADDLE_WIDTH
    angle = 90
    
    if ratio >= 0 and ratio < 0.125:
        angle = 0
    elif ratio >= 0.125 and ratio < 0.25:
        angle = 22.5
    elif ratio >= 0.25 and ratio < 0.375:
        angle = 45
    elif ratio >= 0.375 and ratio < 0.5:
        angle = 67.5
    elif ratio > 0.5 and ratio <= 0.625:
        angle = 112.5 
    elif ratio > 0.625 and ratio <= 0.75:
        angle = 135
    elif ratio > 0.75 and ratio <= 0.875:
        angle = 157.5
    elif ratio > 0.875 and ratio <= 1:
        angle = 180
    return angle

def compPlay(ball, paddlePlayer, paddleComp):
    ## If ball moves towards computer's paddle
    if ballYDirection == 1:
        if ball.x + BALL_SIZE < paddleComp.x + PADDLE_WIDTH/2:
            paddleComp.x -= 10
        elif ball.x + BALL_SIZE > paddleComp.x + PADDLE_WIDTH/2:
            paddleComp.x += 10
    elif ballYDirection == -1:
        if paddleComp.x < DISPLAY_WIDTH/2:
            paddleComp.x += 10
        elif paddleComp.x > DISPLAY_WIDTH/2:
            paddleComp.x -= 10
    return movePaddle(paddleComp, paddleComp.x)

def pauseGame():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        blitText("Pause", WHITE, y_displace=-100,size="large")
        blitText("Press C to continue or Q to quit", WHITE, 25)
        pygame.display.update()
        clock.tick(5) ## Change FPS

def startScreen():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ## If quit button is pressed
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    runGame()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(BLACK)
        blitText("PONG", WHITE, y_displace=-100, size="large")
        blitText("by Edward Tran", WHITE, y_displace=0, x_displace=200, size="medium")
        blitText("Press C to play, P to pause or Q to quit", WHITE, y_displace=180)
        pygame.display.update()
        clock.tick(15) ## Change FPS
    
def runGame():
    gameExit = False
    gameOver = False
    playerWin = False

    ## Initialize variables and starting positions
    score = 0
    ballX = DISPLAY_WIDTH/2 - BALL_SIZE/2
    ballY = DISPLAY_HEIGHT/2 - BALL_SIZE/2
    ballXDispl = 0
    ballYDispl = BALL_SIZE
    global ballYDirection ## Track Y direction, 1 == Up, -1 == Down
    ballYDirection = -1
    ball = pygame.Rect(ballX, ballY , BALL_SIZE, BALL_SIZE)
    paddleX = DISPLAY_WIDTH/2 - PADDLE_WIDTH/2
    paddleY = DISPLAY_HEIGHT - PADDLE_OFFSET - PADDLE_HEIGHT
    paddleDisp = 0
    paddleComp = pygame.Rect(paddleX, PADDLE_OFFSET, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddlePlayer = pygame.Rect(paddleX, paddleY, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    ## Draw objects
    drawArena()
    pygame.draw.rect(gameDisplay, RED, paddleComp)
    pygame.draw.rect(gameDisplay, BLUE, paddlePlayer)

    while not gameExit:

        # Game Over loop
        while gameOver == True:
            gameDisplay.fill(BLACK)
            blitText("Game Over", RED, y_displace=-50, size="large")
            blitText("Press C to play again or Q to quit", WHITE, y_displace=50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: ## If quit button is pressed
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        runGame()

        # Player Win loop
        while playerWin == True:
            gameDisplay.fill(BLACK)
            blitText("You Win!", YELLOW, y_displace=-50, size="large")
            blitText("Press C to play again or Q to quit", WHITE, y_displace=50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: ## If quit button is pressed
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        playerWin = False
                    elif event.key == pygame.K_c:
                        runGame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddleDisp = -10                   
                elif event.key == pygame.K_RIGHT:
                    paddleDisp = 10
                elif event.key == pygame.K_p:
                    pauseGame()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    paddleDisp = 0
                elif event.key == pygame.K_RIGHT:
                    paddleDisp = 0
                    
        ## Move ball to the opposite direction if paddle hits ball
        if checkHitBall(ball, paddlePlayer, paddleComp):
            # Get angle in degree
            if paddleHit == "Player":
                angle = getPaddleAngle(ball, paddlePlayer)
                #score += 1
            else:
                angle = getPaddleAngle(ball, paddleComp)

            if angle == 0:
                ballXDirection = 0

            ballYDirection = - ballYDirection    
            ballYDispl = - ballYDispl
            ballXDispl = ballYDispl*math.cos(math.radians(angle))

            if paddleHit == "Comp":
                ballXDispl = - ballXDispl

        ## Move ball to the opposite direction if ball hits wall
        if checkEdgeCollision(ball):
            # Bounce ball back from the wall if ball its wall    
            ballXDispl = - ballYDispl*math.cos(math.radians(angle))

            if paddleHit == "Comp":
                ballXDispl = - ballXDispl

        ballY += ballYDispl
        ballX += ballXDispl
        ball = moveBall(ball, ballX, ballY)
        paddleX += paddleDisp
        
        paddlePlayer = movePaddle(paddlePlayer, paddleX)
        paddleComp = compPlay(ball, paddlePlayer, paddleComp)

        ## Game over if ball goes off screen
        if ball.y + BALL_SIZE > DISPLAY_HEIGHT: 
            gameOver = True
        elif ball.y < 0:
            playerWin = True

        drawArena()
        drawBall(ball)
        drawPaddle(paddleComp, RED)
        drawPaddle(paddlePlayer, BLUE)
        #updateScore(score)
        
        pygame.display.update()
        clock.tick(FPS)
        
    pygame.quit() ## Requires to prevent program from freezing
    quit()

startScreen()
