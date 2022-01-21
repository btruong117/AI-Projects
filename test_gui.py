import py_compile
import pygame as pg
import sys
from pygame.locals import*

init_x = 50
init_y = 50
OFFWHITE, BLACK, SAGE, LIME= (226, 220, 205), (0, 0 , 0), (157, 193, 131), (199, 234, 70)

pg.init()
FPS = 60
Frames = pg.time.Clock()

DISPLAYSURFACE = pg.display.set_mode((1280, 640))
DISPLAYSURFACE.fill(OFFWHITE)

pg.display.set_caption("Test")

x = init_x
y = init_y

for i in range(8):
    x = init_x
    for j in range(8):
    
        if i % 2 != 0:
            if j % 2 != 0:
                pg.draw.rect(DISPLAYSURFACE, LIME, (x, y, 50, 50))
            if j % 2 == 0:
                pg.draw.rect(DISPLAYSURFACE, SAGE, (x, y, 50, 50))
        else:
            if j % 2 != 0:
                pg.draw.rect(DISPLAYSURFACE, SAGE, (x, y, 50, 50))
            if j % 2 == 0:
                pg.draw.rect(DISPLAYSURFACE, LIME, (x, y, 50, 50))
        x += 50
    y += 50

while True:
    pg.display.update()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    Frames.tick(FPS)
