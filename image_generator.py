import pygame, random
from Vector2 import Vec
from UIpygame import PyUI as pyui

pygame.init()
screenw = 600
screenh = 600
screen = pygame.display.set_mode((screenw+420, screenh), pygame.RESIZABLE)
ui = pyui.UI()
done = False
clock = pygame.time.Clock()

def col_to_int(color):
    col = [c//2 for c in color]
    return 255*255*col[0] + 255*col[1] + col[2]
def pos_to_int(x, y):
    return x*screenh+y
def random_num(num, above, below, min_, max_):
    val = random.randint(num-above,num+below)
    return max(min(val, max_), min_)

def check_in_face(pos,w,h):
    x, y = pos[0]/w,1-pos[1]/h

    # eye
    if (x <= 0.64) and (y >= -x/2+0.975) and (2*y <= 0.8+x):
        return False

    # head circle
    if ((x+0.5)**2+(y-0.6)**2 <= 1.175**2) and (y >= 0.3125-x/8):
        return True
    # neck
    if (y >= 3*x-1.25) and (y <= 0.3125-x/8):
        return True
    # nose
    if (y <= -4*x+3.35) and (y > -x/8+0.5625):
        return True

    return False

# def draw_chaos_line(start, end, )

class Pixel:
    def __init__(self, col, x, y, children):
        self.col = col
        self.x = x
        self.y = y
        self.children = children
    def __str__(self):
        return f"<PIXEL x:{self.x} y:{self.y} col:{self.col}>"
    def __repr__(self):
        return self.__str__()

class Generator:
    spread_index = 2
    search_limit = 100
    def __init__(self):
        self.used_colours = set()
        self.used_positions = set()
        self.active_pixels = []
        self.finished = False
        self.surface = pygame.Surface((screenw, screenh))

        start_pixels = [self.random_pixel()
            # Pixel(pygame.Color(255, 0, 130), 100, 100, Generator.spread_index),
            # Pixel(pygame.Color(130, 250, 0), 500, 100, Generator.spread_index),
            # Pixel(pygame.Color(0, 130, 250), 100, 500, Generator.spread_index),
            # Pixel(pygame.Color(250, 0, 0), 500, 500, Generator.spread_index)
            ]

        for pixel in start_pixels:
            self.active_pixels.append(pixel)
            self.add_pixel(pixel)

    def tick(self):
        if len(self.active_pixels) > 0:
            self.complete_pass()
        elif not self.finished:
            self.finished = True
            temp = random.Random()
            pygame.image.save(self.surface, f"image_output_{temp.randint(100,999)}.png")

    def complete_pass(self):

        if random.randint(0,40) == 22:
            self.active_pixels.append(self.random_pixel())

        del_list = []
        new_pixels = []
        for pixel in self.active_pixels:
            if pixel.children>0:
                new = self.generate_pixel(pixel)
                if new != 0:
                    self.add_pixel(new)
                    new_pixels.append(new)
                pixel.children -= 1
            if pixel.children == 0:
                del_list.append(pixel)
        for pixel in del_list:
            self.active_pixels.remove(pixel)
        for pixel in new_pixels:
            self.active_pixels.append(pixel)


    def generate_pixel(self, pixel):
        pos = (pixel.x, pixel.y)
        count = 0
        while pos_to_int(*pos) in self.used_positions:
            pos = self.randomize_pos(pixel.x, pixel.y)
            count+=1
            if count > 20:
                return 0
        if not check_in_face(pos, screenw, screenh):
            return 0
        col = pixel.col
        count = 0
        while col_to_int(col) in self.used_colours:
            col = self.randomize_col(col, self.pos_to_random_val(pos,pixel))
            count += 1
            if count > Generator.search_limit:
                return 0
        return Pixel(col, pos[0], pos[1], Generator.spread_index)

    def random_pixel(self):
        pos = (random.randint(0,screenw), random.randint(0,screenh))
        while pos_to_int(*pos) in self.used_positions:
            pos = (random.randint(0, screenw), random.randint(0, screenh))
        return Pixel(pygame.Color([random.randint(0,255) for a in range(3)]),
                     pos[0], pos[1], Generator.spread_index)

    def add_pixel(self, pixel):
        self.used_colours.add(col_to_int(pixel.col))
        self.used_positions.add(pos_to_int(pixel.x, pixel.y))
        self.surface.set_at((pixel.x, pixel.y), pixel.col)

    def validate_pixel(self, pixel):
        if pos_to_int(pixel.x, pixel.y) in self.used_positions:
            return False
        if col_to_int(pixel.col) in self.used_colours:
            return False
        return True

    def randomize_pos(self, x, y):
        return random_num(x, 1, 1, 0, screenw), random_num(y, 1, 1, 0, screenh)
    def randomize_col(self, col, val):
        offset = 5
        return pygame.Color(
            random_num(col[0]-val, offset, offset, 0, 255),
            random_num(col[1], offset, offset, 0, 255),
            random_num(col[2]+val, offset, offset, 0, 255))

    def pos_to_random_val(self, pos, pixel):
        offset = Vec(pos[0],pos[1])-Vec(600,600)
        return sum(Vec.make_from_angle(offset.angle()+offset.length()/300,1.5).tuple(True))

random.seed(1)
gen = Generator()

while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(pyui.Style.wallpapercol)
    ui.rendergui(screen)

    screen.blit(gen.surface,(0,0))
    screen.blit(pygame.transform.scale(gen.surface,(400,400)),(screenw+10,10))
    screen.blit(pygame.transform.scale(gen.surface, (100, 100)), (screenw + 160, 420))
    screen.blit(pygame.transform.scale(gen.surface, (40, 40)), (screenw + 190, 530))
    gen.tick()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()