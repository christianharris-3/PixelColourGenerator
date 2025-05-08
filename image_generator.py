import pygame, random
from Vector2 import Vec
from UIpygame import PyUI as pyui

pygame.init()
screenw = 1000
screenh = 1000
screen = pygame.display.set_mode((screenw+420, screenh), pygame.RESIZABLE)
ui = pyui.UI()
done = False
clock = pygame.time.Clock()

def col_to_int(col):
    # col = [c//2 for c in col]
    return 255*255*col[0] + 255*col[1] + col[2]
def pos_to_int(x, y):
    return x*screenh+y
def random_num(num, above, below, min_, max_):
    val = random.randint(num-above,num+below)
    return max(min(val, max_), min_)

def check_in_face(pos,w,h):
    x, y = pos[0]/w,1-pos[1]/h
    x+=0.1

    # eye
    if (x <= 0.64) and (y >= -x/2+0.95) and (2*y <= 0.8+x):
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
    def __init__(self, col, x, y, children, tag=0):
        self.col = col
        self.x = x
        self.y = y
        self.children = children
        self.tag = tag
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
        self.added_face = False
        self.surface = pygame.Surface((screenw, screenh))

        start_pixels = [#self.random_pixel()
            # Pixel(pygame.Color(0, 0, 0), 660, 320, Generator.spread_index, True),
            Pixel(pygame.Color(255, 255, 255), 530, 320, Generator.spread_index, False),
            # Pixel(pygame.Color(255, 255, 255), 690, 320, Generator.spread_index, False),
            # Pixel(pygame.Color(0, 130, 250), 100, 500, Generator.spread_index),
            # Pixel(pygame.Color(250, 0, 0), 500, 500, Generator.spread_index)
            ]
        for pixel in start_pixels:
            self.active_pixels.append(pixel)
            self.add_pixel(pixel)

    def add_face(self):
        if not self.added_face:
            self.added_face = True
            start_pixels = []
            for y in range(screenh):
                x = screenw
                while not check_in_face((x,y), screenw, screenh):
                    x-=1
                if x>0:
                    start_pixels.append(Pixel(pygame.Color(255, 255, 255), x + 1, y, Generator.spread_index, False))
                    start_pixels.append(Pixel(pygame.Color(0, 0, 0), x, y, Generator.spread_index, True))
            for x in range(screenw):
                y = screenh
                while not check_in_face((x,y), screenw, screenh) and y>0:
                    y-=1
                if y>0 and y != screenh:
                    start_pixels.append(Pixel(pygame.Color(255, 255, 255), x, y + 1, Generator.spread_index, False))
                    start_pixels.append(Pixel(pygame.Color(0, 0, 0), x, y, Generator.spread_index, True))

            for pixel in start_pixels:
                if pos_to_int(pixel.x, pixel.y) not in self.used_positions:
                    self.active_pixels.append(pixel)
                    self.add_pixel(pixel)

    def tick(self):
        if len(self.active_pixels) > 0:
            self.complete_pass()
        elif not self.finished:
            self.add_face()
            if len(self.active_pixels) == 0:
                self.finished = True
                temp = random.Random()
                pygame.image.save(self.surface, f"images/image_output_{temp.randint(10000,99999)}.png")

    def complete_pass(self):
        # if random.randint(0,40) == 22:
        #     self.add_face()

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
        if (not check_in_face(pos, screenw, screenh))^(pixel.tag == False):
            return 0

        # all_cols = self.get_all_cols(pixel.col,self.pos_to_random_val(pos,pixel))
        # if len(all_cols) == 0:
        #     return 0
        # col = random.choice(all_cols)


        col = pixel.col
        count = 0
        val = self.pos_to_random_val(pos,pixel)
        while col_to_int(col) in self.used_colours:
            col = self.randomize_col(col, val)
            count += 1
            if count > Generator.search_limit:
                return 0
        return Pixel(col, pos[0], pos[1], Generator.spread_index, pixel.tag)

    def random_pixel(self):
        pos = (random.randint(0,screenw), random.randint(0,screenh))
        while pos_to_int(*pos) in self.used_positions:
            pos = (random.randint(0, screenw), random.randint(0, screenh))
        return Pixel(pygame.Color([random.randint(0,255) for a in range(3)]),
                     pos[0], pos[1], Generator.spread_index)

    def add_pixel(self, pixel):
        self.used_colours.add(col_to_int(pixel.col))
        self.used_positions.add(pos_to_int(pixel.x, pixel.y))
        # if (Vec(pixel.x,pixel.y)-(Vec(screenw,screenh)/2)).length()<screenw/2:
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
    def get_all_cols(self, col, val):
        offset = 5
        return [pygame.Color(r,g,b)
                for r in range(max(col[0]-val-offset,0), min(col[0]-val+offset,256))
                for g in range(max(col[1]-val-offset,0), min(col[1]-val+offset,256))
                for b in range(max(col[2]-val-offset,0), min(col[2]-val+offset,256))
                if col_to_int((r,g,b)) not in self.used_colours]


    def pos_to_random_val(self, pos, pixel):
        if pixel.tag:
            return -1
            offset = Vec(pos[0], pos[1]) - Vec(300, 300)
        else:
            return 1
            offset = Vec(pos[0], pos[1]) - Vec(800, 500)
        return sum(Vec.make_from_angle(offset.angle() + 3.1 + offset.length() / 100, 1.5).tuple(True))

# random.seed(3)
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