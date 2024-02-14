import pygame
import random
import math
import sys

# init pygame
pygame.init()

# global variables for window
WIDTH = 600
HEIGHT = 400
TITLE = "Pong Game"

# global variables for colour
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# set height and width of screen and window title
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# set the game clock loop and FPS
CLOCK = pygame.time.Clock()
FPS = 60


class Paddle:
    # set initial position of dimensions, speed, and colour
    def __init__(self, posx, posy, width, height, speed, colour):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.colour = colour

        # create rect object and assign
        self.paddleRect = pygame.Rect(posx, posy, width, height)
        # draw object to game window
        self.user_paddle = pygame.draw.rect(SCREEN, self.colour, self.paddleRect)

    # Used to display the paddle object on screen
    def display(self):
        self.user_paddle = pygame.draw.rect(SCREEN, self.colour, self.paddleRect)

    # used to define the paddle movement and update the position of the object
    # paddle will only move in y direct, defined by y_movement
    # if y_movement == -1 then paddle is moving updated
    # if y_movement == 0 then paddle is stationary
    # if y_movement == 1 then paddle is moving downward
    def update(self, y_movement):
        self.posy = self.posy + self.speed * y_movement

        # restrict the movements of the paddle to the game window
        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        # self.paddleRect = (self.posx, self.posy, self.width, self.height)
        # Use move_ip to update the position of the existing rectangle
        self.paddleRect.move_ip(0, self.speed * y_movement)

        # Set the updated rectangle back to self.paddleRect
        self.paddleRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def get_location(self):
        return self.posy

    # render player score to screen
    def displayScore(self, text, score, x, y, colours):
        font20 = pygame.font.Font('freesansbold.ttf', 20)
        text = font20.render(text + f'{score}', True, colours)
        textRect = text.get_rect()
        textRect.center = (x, y)
        SCREEN.blit(text, textRect)

    def getRect(self):
        return self.paddleRect


# ball class
class Ball:
    # initialise starting variables
    def __init__(self, posx, posy, radius, speed, colour):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.colour = colour
        self.x_movement = 1
        self.y_movement = -1
        # define circle rect object
        self.ball = pygame.draw.circle(SCREEN, self.colour, (self.posx, self.posy), self.radius)

    # display ball in game window function
    def display(self):
        self.ball = pygame.draw.circle(SCREEN, self.colour, (self.posx, self.posy), self.radius)

    # function to update position of ball in game window
    def update(self):
        self.posx += self.speed * self.x_movement
        self.posy += self.speed * self.y_movement

        # keep ball within game window if it hits the top of the game window
        # adds ceiling and floor to game window
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.y_movement *= -1

        # keeps ball within game window if it hits the left or right wall
        if self.posx <= 0 or self.posx >= WIDTH:
            self.x_movement *= -1

            if self.posx <= 0:
                # print('Paddle Two Scored')
                return 1
            if self.posx >= WIDTH:
                # print('Paddle One Scored')
                return - 1

    def get_location(self):
        return self.posx, self.posy

    # used to reflect the balls direction when it makes contact with the paddles
    def hit(self):
        self.x_movement *= -1

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.reset_direction = random.randrange(0, 2)
        self.x_movement = [-1, 1][self.reset_direction]

    # define function to return circle rect object
    def getRect(self):
        return self.ball


# game manager function
def main():
    running = True
    SCREEN.fill((0, 0, 0))

    # define paddles
    # passing starting posx, posy, width, height, speed and colour
    paddle_one = Paddle(20, 200, 7, 70, 10, GREEN)
    paddle_two = Paddle(WIDTH - 30, 200, 7, 70, 10, GREEN)

    # put paddle objects in list to be used later
    # for collision detection of paddles and ball
    paddles_lst = [paddle_one, paddle_two]

    # define ball
    # passing in starting posx, posy, radius, speed and colour
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE)

    # varible used to track score, starts at 0
    paddle_one_score = 0
    paddle_two_score = 0

    while running:

        # check to see if user wants to close game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Update paddle_one based on keys
        if keys[pygame.K_w]:
            paddle_one_y_movement = -1
        elif keys[pygame.K_s]:
            paddle_one_y_movement = 1
        else:
            paddle_one_y_movement = 0

        # Update paddle_two based on keys
        if keys[pygame.K_UP]:
            paddle_two_y_movement = -1
        elif keys[pygame.K_DOWN]:
            paddle_two_y_movement = 1
        else:
            paddle_two_y_movement = 0

        for paddle in paddles_lst:
            if pygame.Rect.colliderect(ball.getRect(), paddle.getRect()):
                ball.hit()

        # update objects with new y position
        paddle_one.update(paddle_one_y_movement)
        paddle_two.update(paddle_two_y_movement)
        # update ball object to new position and assign to point
        # variable used to determin if a point has been scored and by what player
        point = ball.update()

        # if point = -1 then ball has touched RHS wall
        # if point = 1 then ball has touched LHS wall
        if point == -1:
            paddle_one_score += 1
        if point == 1:
            paddle_two_score += 1

        # reset ball position to middle of screen when a point has been scored
        if point:
            ball.reset()

        # get location of game window object
        # used to track state of game
        paddle_one_y_position = paddle_one.get_location()
        paddle_two_y_position = paddle_two.get_location()
        ball_x_and_y_position = ball.get_location()

        # print(f'Paddle One: {paddle_one_y_position} | Paddle Two: {paddle_two_y_position} | Ball: {
        # ball_x_and_y_position}')\

        def game_state():
            current_state = (
                paddle_one_y_position,
                paddle_two_y_position,
                ball_x_and_y_position,
                paddle_one_score,
                paddle_two_score)
            print(current_state)
            return current_state

        SCREEN.fill((0, 0, 0))  # Clear the screen

        paddle_one.display()
        paddle_two.display()
        ball.display()

        paddle_one.displayScore("Player One: ", paddle_one_score, 100, 20, WHITE)
        paddle_two.displayScore("Player Two: ", paddle_two_score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        CLOCK.tick(FPS)
        game_state()


if __name__ == "__main__":
    main()
    pygame.quit()
