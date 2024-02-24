import pygame
import sys
import random
import os
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
screen = pygame.display.set_mode((600, 400))
screen.fill((0, 0, 0))

snake_segments = [(300, 200), (290, 200), (280, 200)]
SNAKE_SPEED = 10
SNAKE_DIRECTION = 'right'
FOOD_POSITION = [random.randint(0, 59)*SNAKE_SPEED, random.randint(0, 39)*SNAKE_SPEED]
score = 0

font = pygame.font.Font(None, 36)

# Sound generation function
def generate_square_wave(frequency=440, volume=0.1, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    period = int(sample_rate / frequency)
    amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    waveform = array('h', [int(amplitude if time < period / 2 else -amplitude) for time in range(period)] * int(duration * frequency))
    sound = pygame.mixer.Sound(waveform)
    sound.set_volume(volume)
    return sound

# Predefined sounds
eat_food_sound = generate_square_wave(660, 0.1, 0.1)
game_over_sound = generate_square_wave(220, 0.1, 0.5)

def draw_snake():
    for segment in snake_segments:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(segment[0], segment[1], SNAKE_SPEED, SNAKE_SPEED))

def draw_food():
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(FOOD_POSITION[0], FOOD_POSITION[1], SNAKE_SPEED, SNAKE_SPEED))

def move_snake():
    global SNAKE_DIRECTION
    global FOOD_POSITION
    global score
    if SNAKE_DIRECTION == 'right':
        new_head = (snake_segments[0][0] + SNAKE_SPEED, snake_segments[0][1])
    elif SNAKE_DIRECTION == 'left':
        new_head = (snake_segments[0][0] - SNAKE_SPEED, snake_segments[0][1])
    elif SNAKE_DIRECTION == 'up':
        new_head = (snake_segments[0][0], snake_segments[0][1] - SNAKE_SPEED)
    elif SNAKE_DIRECTION == 'down':
        new_head = (snake_segments[0][0], snake_segments[0][1] + SNAKE_SPEED)

    snake_segments.insert(0, new_head)
    if new_head == tuple(FOOD_POSITION):
        FOOD_POSITION[0] = random.randint(0, 59)*SNAKE_SPEED
        FOOD_POSITION[1] = random.randint(0, 39)*SNAKE_SPEED
        eat_food_sound.play()  # Play a sound when the snake eats food
        score += 1
    else:
        snake_segments.pop()

def check_collisions():
    if snake_segments[0] in snake_segments[1:] or \
       snake_segments[0][0] < 0 or snake_segments[0][0] > 590 or \
       snake_segments[0][1] < 0 or snake_segments[0][1] > 390:
        game_over_sound.play()  # Play a sound when the snake collides with itself or the screen boundaries
        return True
    return False

def handle_input():
    global SNAKE_DIRECTION
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and SNAKE_DIRECTION != 'left':
                SNAKE_DIRECTION = 'right'
            elif event.key == pygame.K_LEFT and SNAKE_DIRECTION != 'right':
                SNAKE_DIRECTION = 'left'
            elif event.key == pygame.K_UP and SNAKE_DIRECTION != 'down':
                SNAKE_DIRECTION = 'up'
            elif event.key == pygame.K_DOWN and SNAKE_DIRECTION != 'up':
                SNAKE_DIRECTION = 'down'

clock = pygame.time.Clock()

while True:
    handle_input()
    move_snake()
    if check_collisions():
        text = font.render("Game Over! Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (200, 200))
        pygame.display.update()
        pygame.time.wait(3000)
        break
    screen.fill((0, 0, 0))
    draw_snake()
    draw_food()
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (0, 0))
    pygame.display.update()
    clock.tick(15)
