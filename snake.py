import pygame
import random
import sys
import time
import psycopg2

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="snake",
        user="aishassoul",
        password=""
    )
    return conn

def create_results_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id SERIAL PRIMARY KEY,
            player_name VARCHAR(50),
            score INT,
            level INT,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

def save_result_to_db(player_name, score, level):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO results (player_name, score, level) VALUES (%s, %s, %s)",
        (player_name, score, level)
    )

    conn.commit()
    cur.close()
    conn.close()

pygame.init()

SCREEN_WIDTH = 620
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20
START_SPEED = 10

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
font = pygame.font.Font(None, 30)

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def generate_food(snake_body):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake_body:
            return x, y

def draw_snake(snake_body):
    for x, y in snake_body:
        pygame.draw.rect(screen, GREEN, (x, y, BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

def game(player_name):
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"

    food = generate_food(snake)
    food_value = random.randint(1, 3)
    food_spawn_time = pygame.time.get_ticks()

    score = 0
    level = 1
    speed = START_SPEED

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        head_x, head_y = snake[0]

        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        

        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            running = False

        if (head_x, head_y) in snake:
            running = False

        snake.insert(0, (head_x, head_y))

        now = pygame.time.get_ticks()
        if now - food_spawn_time > 3000:
            food = generate_food(snake)
            food_value = random.randint(1, 3)
            food_spawn_time = pygame.time.get_ticks()

        if (head_x, head_y) == food:
            score += food_value
            food = generate_food(snake)
            food_value = random.randint(1, 3)
            food_spawn_time = pygame.time.get_ticks()

            if score % 3 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

        draw_snake(snake)
        draw_food(food)
        draw_text(str(food_value), food[0] + 3, food[1] - 18, WHITE)

        draw_text(f"счёт: {score}", 10, 10)
        draw_text(f"уровень: {level}", 500, 10)

        pygame.display.update()
        clock.tick(speed)

    screen.fill(BLACK)
    draw_text("вы проиграли", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 10, RED)
    pygame.display.update()
    time.sleep(2)

    save_result_to_db(player_name, score, level)

if __name__ == "__main__":
    create_results_table()
    name = input("enter your name: ").strip()
    
    game(name)
    pygame.quit()
    sys.exit()
