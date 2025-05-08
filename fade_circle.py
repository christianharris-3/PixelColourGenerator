import pygame, math, random
from UIpygame import PyUI as pyui
from Vector2 import Vec

pygame.init()
screenw = 1200
screenh = 1200
screen = pygame.display.set_mode((screenw, screenh), pygame.RESIZABLE)
ui = pyui.UI()
ui.styleload_green()
done = False
clock = pygame.time.Clock()


def draw_fade_circle()



while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(pyui.Style.wallpapercol)
    ui.rendergui(screen)


    pygame.display.flip()
    clock.tick(60)
pygame.quit()