import pygame as pg
import glyphs as gph
from dictionary import Color


BLOCK_SIZE = 30 # % 3
HALF_BLOCK_SIZE = 15
X = None
Y = None
OFFSET_X = 0
OFFSET_Y = 0

pg.font.init()
roboto_font = pg.font.SysFont("roboto", 24)
hint_font = pg.font.SysFont("roboto", 12)

# Colors

def init_main_surface(XX, YY):
    global X, Y
    X = XX
    Y = YY
    return get_main_surface()

def get_main_surface():
    sc = pg.Surface((X * BLOCK_SIZE, Y * BLOCK_SIZE))
    return sc

def set_block_size(sz):
    if (sz == 0):
        return
    global BLOCK_SIZE, HALF_BLOCK_SIZE
    BLOCK_SIZE = sz
    HALF_BLOCK_SIZE = sz // 2

def find_block_center(block_x, block_y):
    return block_x * BLOCK_SIZE + HALF_BLOCK_SIZE, block_y * BLOCK_SIZE + HALF_BLOCK_SIZE


def draw_line(sc, point_A, point_B, color=Color.WHITE, width=2):
    pg.draw.line(sc, color.value, point_A, point_B, width)


def draw_rectangle(sc, point_LU, size, color=Color.WHITE, width=1):
    pg.draw.rect(sc, color.value, (*point_LU, *size), width)


def draw_block(sc, block_x, block_y, type="E"):
    bx, by = find_block_center(block_x, block_y)
    d = gph.TERMS[type]
    if (type[0] == "E"):
        return
    if (type[0] == "P"):
        zx, zy, zsx, zsy = None, None, None, None
        px, py, psx, psy = None, None, None, None
        if (type[1] == "H"):
            zx, zy = bx - HALF_BLOCK_SIZE, by - HALF_BLOCK_SIZE // 3 + 1
            zsx, zsy = BLOCK_SIZE, 2 * HALF_BLOCK_SIZE // 3
            if (type[2] == "N"):
                    px, py = bx - HALF_BLOCK_SIZE, by - HALF_BLOCK_SIZE + 2
                    psx, psy = BLOCK_SIZE, HALF_BLOCK_SIZE - 1
            if (type[2] == "S"):
                    px, py = bx - HALF_BLOCK_SIZE, by + 1
                    psx, psy = BLOCK_SIZE, HALF_BLOCK_SIZE - 1
            if (type[2] == "W"):
                    px, py = bx - HALF_BLOCK_SIZE + 2, by - HALF_BLOCK_SIZE
                    psx, psy = HALF_BLOCK_SIZE - 1, BLOCK_SIZE                
            if (type[2] == "E"):
                    px, py = bx + 1, by - HALF_BLOCK_SIZE
                    psx, psy = HALF_BLOCK_SIZE - 1, BLOCK_SIZE

        #Platform
        draw_rectangle(sc,
               (px, py),
               (psx, psy),
               color=Color.GREY,
               width = 0)

        #Placeholder
        draw_rectangle(sc, 
                  (zx, zy), 
                  (zsx, zsy),
                  color=Color.BLACK)
            

    if (type[0] == "B"):
        if (d[0][1] == '-'):
            draw_line(sc,
                     (bx - HALF_BLOCK_SIZE, by - HALF_BLOCK_SIZE),
                     (bx + HALF_BLOCK_SIZE, by - HALF_BLOCK_SIZE),
                     color=Color.RED)
        if (d[2][1] == '-'):
            draw_line(sc,
                     (bx - HALF_BLOCK_SIZE, by + HALF_BLOCK_SIZE),
                     (bx + HALF_BLOCK_SIZE, by + HALF_BLOCK_SIZE),
                     color=Color.RED)
        if (d[1][0] == '|'):
            draw_line(sc,
                     (bx - HALF_BLOCK_SIZE, by - HALF_BLOCK_SIZE),
                     (bx - HALF_BLOCK_SIZE, by + HALF_BLOCK_SIZE),
                     color=Color.RED)
        if (d[1][2] == '|'):
            draw_line(sc,
                     (bx + HALF_BLOCK_SIZE, by - HALF_BLOCK_SIZE),
                     (bx + HALF_BLOCK_SIZE, by + HALF_BLOCK_SIZE),
                     color=Color.RED)




def field(ffield, sc):
    sc.fill(Color.BACKGROUND.value)

    X = len(ffield[0])
    Y = len(ffield)

    for i in range(Y):
        for j in range(X):
            draw_block(sc, j, i, ffield[i][j])


def unit(sc, uunit):
    color = uunit.color
    coupled = uunit.coupled
    pcx, pcy = find_block_center(*uunit.edge.pos[:2])
    rail_id = uunit.edge.pos[2]
    tsx, tsy = BLOCK_SIZE // 3 * 2, HALF_BLOCK_SIZE // 3 * 2
    img = pg.Surface((tsx, tsy))
    img.fill(color.value)
    if coupled: draw_rectangle(img, (0, 0), (tsx, tsy), color=Color.BLACK, width=BLOCK_SIZE // 10)
    img.set_colorkey((0, 0, 0, 255))
    slux, sluy = pcx, pcy

    if rail_id == 1:
        slux -= BLOCK_SIZE // 3                      #10      
        sluy -= HALF_BLOCK_SIZE // 3                 #5       
    elif rail_id == 2:
        slux -= HALF_BLOCK_SIZE // 3                 #5
        sluy -= BLOCK_SIZE // 3                      #10  
        img = pg.transform.rotate(img, -90)
    elif rail_id == 3:
        slux -= BLOCK_SIZE // 10                     #3  
        sluy -= HALF_BLOCK_SIZE + BLOCK_SIZE // 10   #18    
        img = pg.transform.rotate(img, -45)
    elif rail_id == 4:
        slux -= BLOCK_SIZE // 10                     #3           
        sluy -= BLOCK_SIZE // 10                     #3         
        img = pg.transform.rotate(img, 45)
    elif rail_id == 5:
        slux -= HALF_BLOCK_SIZE + BLOCK_SIZE // 10   #18                   
        sluy -= BLOCK_SIZE // 10                     #3   
        img = pg.transform.rotate(img, -45)
    elif rail_id == 6:
        slux -= HALF_BLOCK_SIZE + BLOCK_SIZE // 10   #18          
        sluy -= HALF_BLOCK_SIZE + BLOCK_SIZE // 10   #18     
        img = pg.transform.rotate(img, 45)
    else:
        raise Exception(f"wrong position of unit {uunit}")
    sluy += 1
    sc.blit(img, (slux, sluy))


def edge(sc, e):
    x, y = e.pos[:2]
    bx, by = find_block_center(x, y)
    width = max(1, (-(-BLOCK_SIZE // 15)))
    rail_id = e.pos[2]
    if rail_id == 1:
        draw_line(sc, (bx - HALF_BLOCK_SIZE, by), (bx + HALF_BLOCK_SIZE, by), color=e.color)
    if rail_id == 2:
        draw_line(sc, (bx, by - HALF_BLOCK_SIZE), (bx, by + HALF_BLOCK_SIZE), color=e.color)
    if rail_id == 3:
        draw_line(sc, (bx + HALF_BLOCK_SIZE, by), (bx, by - HALF_BLOCK_SIZE), color=e.color)
    if rail_id == 4:
        draw_line(sc, (bx + HALF_BLOCK_SIZE, by), (bx, by + HALF_BLOCK_SIZE), color=e.color)
    if rail_id == 5:
        draw_line(sc, (bx - HALF_BLOCK_SIZE, by), (bx, by + HALF_BLOCK_SIZE), color=e.color)
    if rail_id == 6:
        draw_line(sc, (bx - HALF_BLOCK_SIZE, by), (bx, by - HALF_BLOCK_SIZE), color=e.color)



def mouse_hint(sc=None):
    pos = pg.mouse.get_pos()
    pos = (((pos[0] - OFFSET_X) // BLOCK_SIZE), ((pos[1]- OFFSET_Y) // BLOCK_SIZE))
    hint = roboto_font.render(f"{pos}", False, (0, 180, 0))
    if (sc is not None): sc.blit(hint, (0, 0))
    return pos

def block_highlight(sc, block_pos):
    bc = find_block_center(*block_pos)
    bc = (bc[0] - BLOCK_SIZE // 2, bc[1] - BLOCK_SIZE // 2)
    draw_rectangle(sc, bc, (BLOCK_SIZE, BLOCK_SIZE), color=Color.RED)

def change_offset(rel):
    global OFFSET_X, OFFSET_Y
    OFFSET_X += rel[0]
    OFFSET_Y += rel[1]

def zoom(delta):
    global OFFSET_X, OFFSET_Y
    mpos = pg.mouse.get_pos()
    set_block_size(BLOCK_SIZE + delta)
    bcx, bcy = mouse_hint()
    change_offset((-bcx * delta, -bcy * delta))
    return get_main_surface()


def push(display, sc):
    display.fill(Color.BLACK.value)
    display.blit(sc, (OFFSET_X, OFFSET_Y))


class Console():
    display = None
    x, y = (0, 0)
    def __init__(self, display, x = 500, y = 50):
        self.display = display
        self.x, self.y = x, y

    def render(self, message = ""):
        cx, cy = pg.display.get_surface().get_size()
        blitx = cx // 2 - self.x // 2
        blity = cy // 2 - self.y // 2
        
        sc = pg.Surface((self.x, self.y))
        sc.fill((1, 1, 1))
        
        hint = roboto_font.render(message, False, (250, 250, 250))
        sc.blit(hint, (10, 10))

        draw_rectangle(sc, (0, 0), (self.x, self.y), Color.GREY, width=5)
        self.display.blit(sc, (blitx, blity))
    def process(self):
        message = ""
        while True:
            self.render(message)
            pg.time.delay(20)
            pg.display.update()
    
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    GAME = False
                if i.type == pg.MOUSEWHEEL:
                    MULT = 1
                    if pg.key.get_pressed()[pg.K_LCTRL]: MULT = 10
                    sc = render.zoom(i.y * MULT)
                if (i.type == pg.MOUSEMOTION and i.buttons == (0, 1, 0)):
                    render.change_offset(i.rel)
                if (i.type == pg.KEYDOWN and i.key in (13, 1073741912)):
                    return message
                if (i.type == pg.KEYDOWN):
                    if (i.key == 8):
                        message = message[:-1]
                    else:
                        message += i.unicode


def console(display):
    c = Console(display)
    return c.process()

class BlockHint:
    display = None
    graph = None
    x, y = (500, 50)
    def __init__(self, display, graph, size=(500, 50)):
        self.x, self.y = size
        self.display = display
        self.graph = graph
        pg.time.delay(50)
        for i in pg.event.get():
            pass


    def process(self):
        self.render()
        while True:
            for i in pg.event.get():
                if i.type == pg.KEYDOWN or i.type == pg.MOUSEBUTTONDOWN:
                    return

    def render(self):
        bx, by = mouse_hint()

        print("rendering")

        sc = pg.Surface((self.x, self.y))
        draw_rectangle(sc, (0, 0), (self.x, self.y), color=Color.BLACK, width = 5)
        sc.fill((180, 180, 180))

        unit = None
        for z in range(6):
            e = self.graph.get((bx, by, z + 1))
            if not e or not e.unit: continue
            unit = e.unit
        text_hint = hint_font.render(str(unit), False, (20, 20, 20))
        sc.blit(text_hint, (10, 10))
        self.display.blit(sc, pg.mouse.get_pos())
        pg.display.update()



def block_hint(display, graph, mouse_pos):
    b = BlockHint(display, graph)
    b.process()
    
