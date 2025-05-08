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



def draw_chaos_line(screen, col, start, end, curve, step):
    direction = (end-start).normalized()

    prev = start.tuple()

    for i in range(0, int((end-start).length()), step):
        center = start+direction*i
        center.x = random.gauss(center.x, curve(i))
        center.y = random.gauss(center.y, curve(i))
        if i != 0:
            pygame.draw.aaline(screen, col, prev, center.tuple())
        prev = center.tuple()




divider = ui.makeslider(10,20,600,20,maxp=40000,startp=1000)
power = ui.makeslider(10,50,400,20,maxp=2,startp=1,increment=0.05)


while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(pyui.Style.wallpapercol)
    ui.rendergui(screen)

    # center = Vec(600,600)
    # radius = 800
    # random.seed(2)
    # for a in range(50):
    #     draw_chaos_line(screen, (a,0,255-a*2), center+Vec.make_from_angle(a/50*math.pi*2+2.5)*80, center+Vec.make_from_angle(a/50*math.pi*2)*radius, lambda x: math.sin((x**power.slider)/divider.slider)*5, 2)

    pygame.draw

    pygame.display.flip()
    clock.tick(60)
pygame.quit()