import pygame
from pygame.locals import *
import sys
from datetime import datetime

pygame.font.init()
pygame.init()

color_background = (0, 0, 0)
color_text = (255, 255, 255)

x = 320
y = 240
screen = pygame.display.set_mode((x, y))
font = pygame.font.Font("/home/pi/rpidualili9341/ui/swiss911.ttf", 110)

screen.fill((color_background))

time = None

tx = None
ty = None

def pprint(text, color):
    global tx, ty, screen, font
    image = font.render(text, False, color)
    if tx is None or ty is None:
        width, height = image.get_size()
        tx = int(x/2-width/2)
        ty = int(y/2-height/2)
    screen.blit(image, (tx, ty))

while 1:
    now = datetime.now()
    newtime = str(now.hour).zfill(2) + \
              ":" + str(now.minute).zfill(2) + \
              ":" + str(now.second).zfill(2)
    if time is None:
        time = newtime
    if time is None or time != newtime:
        pprint(time, color_background)
        time = newtime
        pprint(time, color_text)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            break

pygame.quit()
