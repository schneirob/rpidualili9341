import pygame
from pygame.locals import *
import sys
from datetime import datetime

pygame.font.init()
pygame.init()
pygame.mouse.set_visible(False)

color_background = (0, 0, 0)
color_text = (255, 255, 255)

x = 320
y = 240
screen = pygame.display.set_mode((x, y))
fontname = "/home/pi/rpidualili9341/ui/swiss911.ttf"
# fontname = "swiss911.ttf"
font = pygame.font.Font(fontname, 110)
fontsmall = pygame.font.Font(fontname, 20)

screen.fill((color_background))

time = None

tx = None
ty = None

clock = pygame.time.Clock()

start = datetime.now()
framecount = 0

def pprint(text, color):
    global tx, ty, screen, font, now, start, framecount

    framecount += 1
    fps = framecount / (now-start).total_seconds()
    image = fontsmall.render("%.2f fps" % fps, False, color)
    screen.blit(image, (0, 0))

    image = font.render(text, False, color)
    if tx is None or ty is None:
        width, height = image.get_size()
        tx = int(x/2-width/2)
        ty = int(y/2-height/2)
    screen.blit(image, (tx, ty))

    image = fontsmall.render("%.0f" % now.microsecond, False, color)
    screen.blit(image, (0, ty + 120))


ok = True
while ok:
    clock.tick(1000)
    now = datetime.now()
    time = str(now.hour).zfill(2) + \
           ":" + str(now.minute).zfill(2) + \
           ":" + str(now.second).zfill(2)

    screen.fill((color_background))
    pprint(time, color_text)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            ok = False

pygame.quit()
