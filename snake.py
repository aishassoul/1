#импортируем нужные библиотеки
import pygame, random, sys, time

pygame.init()  #запускаем pygame

#размеры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 620, 400
BLOCK_SIZE = 20   #размер одного квадратика (сегмента змейки и еды)
SPEED = 10        #начальная скорость игры

#цвета (RGB)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

#создаём окно игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")  #заголовок окна

#создаём шрифт для текста
font = pygame.font.Font(None, 30)

#функция для вывода текста на экран
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)  #создаём текстовую поверхность
    screen.blit(text_surface, (x, y))              #рисуем текст на экране по координатам (x, y)

#функция для генерации случайной еды (чтобы не появлялась на змейке)
def generate_food(snake_body):
    while True:  #бесконечный цикл пока не найдём место
        #выбираем случайную клетку по сетке
        x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        #проверяем — не совпадает ли с телом змейки
        if (x, y) not in snake_body:
            return x, y  #возвращаем координаты еды

#рисуем змейку (каждый сегмент зелёным)
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

#рисуем еду (красный квадрат)
def draw_food(food_position):
    pygame.draw.rect(screen, RED, (food_position[0], food_position[1], BLOCK_SIZE, BLOCK_SIZE))

#основная функция игры
def game():
    #стартовая змейка (из 3 квадратиков)
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "RIGHT"  #направление движения
    food = generate_food(snake)  #создаём первую еду
    score = 0  #счёт
    level = 1  #уровень
    speed = SPEED  #текущая скорость

    clock = pygame.time.Clock()  #создаём таймер
    running = True               #флаг, чтобы игра шла

    while running:
        screen.fill(BLACK)  #очищаем экран (чёрный фон)

        #обрабатываем все события (клавиши и выход)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #если нажали на крестик
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  #если нажали клавишу
                #движение вверх (если не идём вниз)
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                #движение вниз (если не идём вверх)
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                #движение влево (если не идём вправо)
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                #движение вправо (если не идём влево)
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        #координаты головы змейки (первая часть списка)
        head_x, head_y = snake[0]

        #меняем координаты головы в зависимости от направления
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        #проверка на удар о стену если выходим за границы экрана
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            running = False  #заканчиваем игру

        #проверка на удар о себя (если голова совпадает с любой частью тела)
        if (head_x, head_y) in snake:
            running = False  #заканчиваем игру

        #добавляем новую голову змейки в начало
        snake.insert(0, (head_x, head_y))

        #проверяем, съела ли змейка еду
        if (head_x, head_y) == food:
            score += 1  #добавляем очко
            food = generate_food(snake)  #создаём новую еду
            #каждые 3 очка новый уровень и ускорение
            if score % 3 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()  #удаляем хвост (если не съела)

        #рисуем змейку
        draw_snake(snake)
        #рисуем еду
        draw_food(food)

        #рисуем текст (счёт и уровень)
        draw_text(f"Счет: {score}", 10, 10)
        draw_text(f"Уровень: {level}", 500, 10)

        #обновляем экран
        pygame.display.update()
        #ограничиваем скорость (чтобы игра не шла слишком быстро)
        clock.tick(speed)

    #если проиграли, показываем сообщение
    screen.fill(BLACK)
    draw_text("Вы проиграли!", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 10, RED)
    pygame.display.update()
    time.sleep(2)  #ждём 2 секунды
    pygame.quit()
    sys.exit()

#запускаем игру
game()
