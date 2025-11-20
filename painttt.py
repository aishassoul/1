import pygame
import random

white = (255, 255, 255)
eraser = (0, 0, 0)
green = (34, 139, 34)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

pygame.display.set_caption("Paint")

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 15
    mode = white
    last_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

            # выбор цвета
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mode = red
                elif event.key == pygame.K_g:
                    mode = green
                elif event.key == pygame.K_b:
                    mode = blue
                elif event.key == pygame.K_y:
                    mode = yellow
                elif event.key == pygame.K_e:
                    mode = eraser
                elif event.key == pygame.K_x:
                    mode = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

                # готовые фигуры
                elif event.key == pygame.K_w:  # прямоугольник
                    drawRectangle(screen, pygame.mouse.get_pos(), 200, 100, mode)
                elif event.key == pygame.K_c:  # круг
                    drawCircle(screen, pygame.mouse.get_pos(), mode)
                elif event.key == pygame.K_s:  # квадрат
                    drawSquare(screen, pygame.mouse.get_pos(), 120, mode)
                elif event.key == pygame.K_t:  # прямоугольный треугольник
                    drawRightTriangle(screen, pygame.mouse.get_pos(), 120, mode)
                elif event.key == pygame.K_q:  # равносторонний треугольник
                    drawEquilateralTriangle(screen, pygame.mouse.get_pos(), 120, mode)
                elif event.key == pygame.K_h:  # ромб
                    drawRhombus(screen, pygame.mouse.get_pos(), 80, mode)

            # рисование линий мышью
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                last_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION and event.buttons[0] and last_pos:
                drawLineBetween(screen, last_pos, pygame.mouse.get_pos(), radius, mode)
                last_pos = pygame.mouse.get_pos()

        pygame.display.flip()
        clock.tick(60)

# линии (как кисть)
def drawLineBetween(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    steps = max(abs(dx), abs(dy))

    for i in range(steps):
        t = i / steps
        x = int(start[0] * (1 - t) + end[0] * t)
        y = int(start[1] * (1 - t) + end[1] * t)
        pygame.draw.circle(screen, color, (x, y), width)

# прямоугольник
def drawRectangle(screen, pos, w, h, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x, y, w, h), 3)

# круг
def drawCircle(screen, pos, color):
    x, y = pos
    pygame.draw.circle(screen, color, (x, y), 100, 3)

# квадрат
def drawSquare(screen, pos, size, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x, y, size, size), 3)

# прямоугольный треугольник
def drawRightTriangle(screen, pos, size, color):
    x, y = pos
    p1 = (x, y)
    p2 = (x + size, y)
    p3 = (x, y + size)
    pygame.draw.polygon(screen, color, [p1, p2, p3], 3)

# равносторонний треугольник
def drawEquilateralTriangle(screen, pos, size, color):
    x, y = pos
    h = int(size * 0.866)  # высота треугольника
    p1 = (x, y)
    p2 = (x + size, y)
    p3 = (x + size // 2, y - h)
    pygame.draw.polygon(screen, color, [p1, p2, p3], 3)

# ромб
def drawRhombus(screen, pos, size, color):
    x, y = pos
    top = (x, y - size)
    right = (x + size, y)
    bottom = (x, y + size)
    left = (x - size, y)
    pygame.draw.polygon(screen, color, [top, right, bottom, left], 3)

main()
