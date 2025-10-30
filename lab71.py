import os, sys, time, math
from pathlib import Path
import pygame


BASE_DIR = Path(__file__).resolve().parent

def asset(name: str) -> str:
    p = BASE_DIR / name
    if not p.exists():
        raise FileNotFoundError(f"Не найден файл: {p}")
    return str(p)


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MICKEY MOUSE CLOCK (Esc to quit)")
clock = pygame.time.Clock()


clock_img = pygame.image.load(asset("clock.png")).convert_alpha()
clock_img = pygame.transform.smoothscale(clock_img, (WIDTH, HEIGHT))

right_arm = pygame.image.load(asset("rightarm.png")).convert_alpha()
left_arm  = pygame.image.load(asset("leftarm.png")).convert_alpha()


right_arm = pygame.transform.smoothscale(right_arm, (800, 600))     
left_arm  = pygame.transform.smoothscale(left_arm,  (41,  682))   


CENTER_MINUTE = (WIDTH // 2 - 30, HEIGHT // 2 - 15)   
CENTER_SECOND = (WIDTH // 2 + 20, HEIGHT // 2 - 18)   

def blit_rotate_center(surface, image, center_xy, angle_deg):
    """Повернуть image вокруг собственного центра и нарисовать так,
    чтобы геометрический центр лег в точку center_xy."""
    rotated = pygame.transform.rotate(image, angle_deg)
    rect = rotated.get_rect(center=center_xy)
    surface.blit(rotated, rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    
    t = time.localtime()
    minute = t.tm_min
    second = t.tm_sec

    
    minute_angle = -(minute * 6 + (second / 60) * 6)   
    second_angle = -(second * 6)                      

    
    screen.fill((0, 0, 0))
    screen.blit(clock_img, (0, 0))

    
    blit_rotate_center(screen, right_arm, CENTER_MINUTE, minute_angle)
    blit_rotate_center(screen, left_arm,  CENTER_SECOND, second_angle)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
