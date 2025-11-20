#импортируем нужные библиотеки
import pygame, sys
from pygame.locals import *
import random, time

#инициализируем pygame видео звук шрифты
pygame.init()

#задаём FPS (скорость кадров)
FPS = 60
FramePerSec = pygame.time.Clock()

#создаём основные цвета rgb
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 400      #ширина окна
SCREEN_HEIGHT = 600     #высота окна
SPEED = 5               #скорость врага
SCORE = 0               #счётчик очков
COINS = 0               #счётчик монет

# разные "веса" монет (сколько монета даёт очков)  #update
COIN_WEIGHTS = [1, 2, 3, 5]                         #update
coin_value = random.choice(COIN_WEIGHTS)           #update

# после скольких монет увеличивать скорость врага   #update
COINS_FOR_SPEEDUP = 5                               #update
next_speed_up = COINS_FOR_SPEEDUP                  #update

#шрифты для текста
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#загружаем фон картинка дороги
background = pygame.image.load("AnimatedStreet.png")

#создаём монету и уменьшаем её размер
coin_img = pygame.image.load("Coin.png")
coin_img = pygame.transform.scale(coin_img, (36, 36))  #меняем размер картинки
coin_rect = coin_img.get_rect()                        #получаем границы монеты
coin_rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  #случайная позиция сверху
coin_speed = 4                                         #скорость падения монеты

#создаём окно 400,600
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)                                #заливаем белым
pygame.display.set_caption("Game")                     #название окна


#класс Enemy
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")     #картинка enemy
        self.rect = self.image.get_rect()               #его прямоугольная область
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)  #старт сверху

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)                      #движение вниз
        if (self.rect.bottom > 600):                    #если выехал за экран
            SCORE += 1                                  #добавляем 1 очко
            self.rect.top = 0                           #переносим наверх
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  #новая позиция


#класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")    #картинка игрока
        self.rect = self.image.get_rect()               #его прямоугольная область
        self.rect.center = (160, 520)                   #стартовая позиция
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()         #проверяем какие клавиши нажаты
        
        #движение влево
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        #движение вправо
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

#создаём объекты игрока и врага
P1 = Player()
E1 = Enemy()

#создаём группы для удобной отрисовки
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#создаём событие, которое каждую секунду увеличивает скорость врага
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#основной игровой цикл
while True:
    #обрабатываем все события нажатия клавиш и тд
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5                #увеличиваем скорость со временем
        if event.type == QUIT:
            pygame.quit()                 #выходим из игры
            sys.exit()

    #рисуем фон
    DISPLAYSURF.blit(background, (0,0))

    #выводим счёт врагов (вверху слева)
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    #движение монеты вниз
    coin_rect.y += coin_speed
    #если монета упала за экран вернуть наверх
    if coin_rect.top > SCREEN_HEIGHT:
        coin_rect.bottom = 0
        coin_rect.centerx = random.randint(40, SCREEN_WIDTH - 40)
        coin_value = random.choice(COIN_WEIGHTS)        # новая случайная ценность монеты  # <<< NEW

    #рисуем монету
    DISPLAYSURF.blit(coin_img, coin_rect)

    #рисуем значение монеты над монетой                                #update
    value_text = font_small.render(str(coin_value), True, BLACK)       #update
    DISPLAYSURF.blit(value_text, (coin_rect.centerx - 8, coin_rect.top - 15)) #update

    #показываем количество собранных монет вверху справа
    coins_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 110, 10))

    #двигаем и рисуем игрока и врага
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        
    #проверяем столкновение игрока с монетой
    if P1.rect.colliderect(coin_rect): #перекасаются ли
        COINS += coin_value                                # прибавляем "вес" монеты    #update
        coin_rect.bottom = 0                               #возвращаем монету наверх
        coin_rect.centerx = random.randint(40, SCREEN_WIDTH - 40)
        coin_value = random.choice(COIN_WEIGHTS)           # новая ценность монеты     #update

        # проверяем, не пора ли ускорить врага по монетам                           #update
        if COINS >= next_speed_up:                         #update
            SPEED += 1                                    #update
            next_speed_up += COINS_FOR_SPEEDUP        #update

    #проверяем столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.wav').play()         #звук столкновения
          time.sleep(1)
          DISPLAYSURF.fill(RED)                          #экран красный
          DISPLAYSURF.blit(game_over, (30,250))          #надпись Game Over
          pygame.display.update()
          for entity in all_sprites:
                entity.kill()                            #убираем спрайты
          time.sleep(2)
          pygame.quit()                                  #закрываем игру
          sys.exit()        
        
    pygame.display.update()                              #обновляем экран
    FramePerSec.tick(FPS)                                #ограничиваем FPS
