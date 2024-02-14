import pygame
import sys


# 1 - create basic window for game


# init pygame
pygame.init()

# global variables for window
WIDTH = 600
HEIGHT = 400
TITLE = "Pong Game"

# set height and width of screen and window title
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# set the game clock loop and FPS
clock = pygame.time.Clock()
FPS = 60

# initial starting position of rectangle
rec_start_x = 10
rec_start_y = 200

# Initial position of the ball
ball_x = WIDTH // 2
ball_y = HEIGHT // 2

# game loop
while True:
    # pygame checking for screen events and for input then deciding what todo
    for event in pygame.event.get():

        # check if user wants to close game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # get user input for moving rectangle
    keys = pygame.key.get_pressed()

    # update the rectangle position based on key press
    rec_start_y -= keys[pygame.K_UP] * 5
    rec_start_y += keys[pygame.K_DOWN] * 5

    # movement of ball
    ball_x = ball_x - 2

    # create bounds for rectangle
    rec_start_y = max(0, min(rec_start_y, HEIGHT - 60))

    ball_x = max(0, min(ball_x, WIDTH - 50))
    ball_y = max(0, min(ball_y, HEIGHT - 10))

    # draw stuff in the game window
    SCREEN.fill((0,0,225))

    # create rectangle object
    rectangle = pygame.Rect(rec_start_x, rec_start_y, 10, 50)

    # draw a rectangle in game window
    pygame.draw.rect(SCREEN, (250,0,0), rectangle, width=0)

    # create a circle object for the ball
    ball_radius = 10
    ball_rec = (ball_x, ball_y)
    pygame.draw.circle(SCREEN, (0, 255, 0), ball_rec, ball_radius)


    # update display
    pygame.display.flip()

    # set frame rate
    clock.tick(FPS)




