import pygame, random
from UIpygame import PyUI as pyui

pygame.init()
screenw = 1200
screenh = 1200
screen = pygame.display.set_mode((screenw, screenh), pygame.RESIZABLE)
ui = pyui.UI()
done = False
clock = pygame.time.Clock()

def col_to_int(col : pygame.Color):
    return 255*255*col[0] + 255*col[1] + col[2]
def pos_to_int(x, y):
    return x*screenh+y
def random_num(num, above, below, min_, max_):
    val = random.randint(num-above,num+below)
    return max(min(val, max_), min_)

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

        initial_pixel = Pixel(pygame.Color(130,130,130), 600, 600, Generator.spread_index)
        self.active_pixels.append(initial_pixel)
        self.add_pixel(initial_pixel)

    def tick(self):
        if len(self.active_pixels) > 0:
            self.complete_pass()
        elif not self.finished:
            self.finished = True
            temp = random.Random()
            pygame.image.save(self.surface, f"image_output_{temp.randint(100,999)}.png")

    def complete_pass(self):
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
        col = pixel.col
        count = 0
        while col_to_int(col) in self.used_colours:
            col = self.randomize_col(col)
            count += 1
            if count > Generator.search_limit:
                return 0
        return Pixel(col, pos[0], pos[1], Generator.spread_index)

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
    def randomize_col(self, col):
        return pygame.Color(
            random_num(col[0], 5, 5, 0, 255),
            random_num(col[1], 5, 5, 0, 255),
            random_num(col[2], 5, 5, 0, 255))


random.seed(1)
gen = Generator()

while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(pyui.Style.wallpapercol)
    ui.rendergui(screen)

    screen.blit(gen.surface,(0,0))
    gen.tick()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()