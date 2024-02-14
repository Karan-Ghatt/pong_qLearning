import pygame
import random
import math
import sys
import numpy as np

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
    def __init__(self, posx, posy, width, height, speed, colour):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.colour = colour

        self.paddleRect = pygame.Rect(posx, posy, width, height)
        self.user_paddle = pygame.draw.rect(SCREEN, self.colour, self.paddleRect)

    def display(self):
        self.user_paddle = pygame.draw.rect(SCREEN, self.colour, self.paddleRect)

    def update(self, y_movement):
        self.posy = self.posy + self.speed * y_movement

        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        self.paddleRect.move_ip(0, self.speed * y_movement)
        self.paddleRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def get_location(self):
        return self.posy

    def displayScore(self, text, score, x, y, colours):
        font20 = pygame.font.Font('freesansbold.ttf', 20)
        text = font20.render(text + f'{score}', True, colours)
        textRect = text.get_rect()
        textRect.center = (x, y)
        SCREEN.blit(text, textRect)

    def getRect(self):
        return self.paddleRect


class Ball:
    def __init__(self, posx, posy, radius, speed, colour):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.colour = colour
        self.x_movement = 1
        self.y_movement = -1
        self.ball = pygame.draw.circle(SCREEN, self.colour, (self.posx, self.posy), self.radius)

    def display(self):
        self.ball = pygame.draw.circle(SCREEN, self.colour, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.x_movement
        self.posy += self.speed * self.y_movement

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.y_movement *= -1

        if self.posx <= 0 or self.posx >= WIDTH:
            self.x_movement *= -1

            if self.posx <= 0:
                return 1
            if self.posx >= WIDTH:
                return -1

    def get_location(self):
        return [self.posx, self.posy]

    def hit(self):
        self.x_movement *= -1

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.reset_direction = random.randrange(0, 2)
        self.x_movement = [-1, 1][self.reset_direction]

    def getRect(self):
        return self.ball


class QLearning:
    def __init__(self):
        self.num_bins_paddle = 10
        self.num_bins_ball_x = 20
        self.num_bins_ball_y = 10
        self.num_actions = 3
        self.q_table_paddle_one = np.zeros((self.num_bins_paddle, self.num_bins_ball_x,
                                            self.num_bins_ball_y, self.num_actions))
        self.q_table_paddle_two = np.zeros((self.num_bins_paddle, self.num_bins_ball_x,
                                            self.num_bins_ball_y, self.num_actions))

    def discretize_state(self, paddle_position, ball_position):
        paddle_bin = min(int(np.digitize(paddle_position, np.linspace(0, HEIGHT, self.num_bins_paddle))) - 1, self.num_bins_paddle - 1)
        ball_x_bin = min(int(np.digitize(ball_position[0], np.linspace(0, WIDTH, self.num_bins_ball_x))) - 1, self.num_bins_ball_x - 1)
        ball_y_bin = min(int(np.digitize(ball_position[1], np.linspace(0, HEIGHT, self.num_bins_ball_y))) - 1, self.num_bins_ball_y - 1)
        return paddle_bin, ball_x_bin, ball_y_bin

    def game_state(self, paddle_one_y_pos, paddle_two_y_pos, ball_x_y, paddle_one_score, paddle_two_score):
        paddle_one_state = self.discretize_state(paddle_one_y_pos, ball_x_y)
        paddle_two_state = self.discretize_state(paddle_two_y_pos, ball_x_y)
        current_state = [paddle_one_state, paddle_two_state, paddle_one_score, paddle_two_score]
        return current_state

    def makeQtables(self):
        self.q_table_paddle_one = np.zeros((self.num_bins_paddle, self.num_bins_ball_x,
                                            self.num_bins_ball_y, self.num_actions))

        self.q_table_paddle_two = np.zeros((self.num_bins_paddle, self.num_bins_ball_x,
                                            self.num_bins_ball_y, self.num_actions))

    def get_action(self, state, epsilon):
        if np.random.rand() < epsilon:
            return np.random.randint(self.num_actions)
        else:
            return np.argmax(self.q_table_paddle_one[state[0]])

    def update_q_table(self, state, action, reward, new_state, alpha, gamma):
        current_value = self.q_table_paddle_one[state[0] + (action,)]
        future_max_value = np.max(self.q_table_paddle_one[new_state[0]])
        new_value = (1 - alpha) * current_value + alpha * (reward + gamma * future_max_value)
        self.q_table_paddle_one[state[0] + (action,)] = new_value


def main():
    running = True
    SCREEN.fill((0, 0, 0))

    q_learning = QLearning()

    paddle_one = Paddle(20, 200, 7, 70, 10, GREEN)
    paddle_two = Paddle(WIDTH - 30, 200, 7, 70, 10, GREEN)

    paddles_lst = [paddle_one, paddle_two]

    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE)

    paddle_one_score = 0
    paddle_two_score = 0

    epsilon = 0.1
    alpha = 0.1
    gamma = 0.9

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            paddle_one_y_movement = -1
        elif keys[pygame.K_s]:
            paddle_one_y_movement = 1
        else:
            paddle_one_y_movement = 0

        if keys[pygame.K_UP]:
            paddle_two_y_movement = -1
        elif keys[pygame.K_DOWN]:
            paddle_two_y_movement = 1
        else:
            paddle_two_y_movement = 0

        for paddle in paddles_lst:
            if pygame.Rect.colliderect(ball.getRect(), paddle.getRect()):
                ball.hit()

        paddle_one.update(paddle_one_y_movement)
        paddle_two.update(paddle_two_y_movement)
        point = ball.update()

        if point == -1:
            paddle_one_score += 1
        if point == 1:
            paddle_two_score += 1

        if point:
            ball.reset()

        paddle_one_y_position = paddle_one.get_location()
        paddle_two_y_position = paddle_two.get_location()
        ball_x_and_y_position = ball.get_location()

        state = q_learning.game_state(paddle_one_y_position, paddle_two_y_position, ball_x_and_y_position,
                                      paddle_one_score, paddle_two_score)

        action_paddle_one = q_learning.get_action(state, epsilon)
        action_paddle_two = q_learning.get_action(state, epsilon)

        paddles_actions = [action_paddle_one, action_paddle_two]

        for i, paddle in enumerate(paddles_lst):
            paddle.update(paddles_actions[i] - 1)

        next_state = q_learning.game_state(paddle_one.get_location(), paddle_two.get_location(),
                                           ball.get_location(), paddle_one_score, paddle_two_score)

        reward = max(paddle_one_score, paddle_two_score)

        q_learning.update_q_table(state, action_paddle_one, reward, next_state, alpha, gamma)

        SCREEN.fill((0, 0, 0))
        paddle_one.display()
        paddle_two.display()
        ball.display()
        paddle_one.displayScore("Player One: ", paddle_one_score, 100, 20, WHITE)
        paddle_two.displayScore("Player Two: ", paddle_two_score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
