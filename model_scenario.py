#!/usr/bin/python3

#import sys
import pygame as pg
# from render import Color
import algorithms
import render
import parsing



FRAMETIME = 33


MAP = "olivier"
SCENARIO = 1


yard, graph, units, trains = parsing.parse_map(f"maps/{MAP}/main.map")
scenario = parsing.parse_scenario(f"maps/{MAP}/{SCENARIO}.scenario")


X, Y = len(yard[0]), len(yard)

display = pg.display.set_mode((X * render.BLOCK_SIZE, Y * render.BLOCK_SIZE), pg.RESIZABLE)

sc = render.init_main_surface(X, Y)

pg.display.set_caption(f"marshalling yard model {MAP}")

pg.display.update()

#print(*yard, sep='\n')

j = 0
GAME = True
while GAME:
    #Not-rail infrastructure
    render.field(yard, sc)
    
    #Hints
    bpos = render.mouse_hint(sc)
    render.block_highlight(sc, bpos)

    for t in trains[1:]:
        #print(t)
        t.process()
    
    #Rails ans units
    graph.render(sc)
    
    # Final scene render

    render.push(display, sc)
    pg.display.update()
    pg.time.delay(FRAMETIME)

    # Hotkeys
    j += 1
    for i in pg.event.get():
        
        # if (i.type not in (pg.MOUSEMOTION, pg.WINDOWMOVED)):
        #     print(i)

        if i.type == pg.QUIT or i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE:
            GAME = False
        
        if (i.type == pg.MOUSEBUTTONDOWN and i.button == 3):
            render.block_hint(display, graph, i.pos)

        # Map zooming and moving
        if i.type == pg.MOUSEWHEEL:
            MULT = 1
            if pg.key.get_pressed()[pg.K_LCTRL]: MULT = 10
            sc = render.zoom(i.y * MULT)
        if (i.type == pg.MOUSEMOTION and i.buttons == (0, 1, 0)):
            render.change_offset(i.rel)
        
        # API input



    # Exit confitions
    pressed_keys = pg.key.get_pressed()
    if pressed_keys[pg.K_LCTRL] and (pressed_keys[pg.K_c] or pressed_keys[pg.K_d] or pressed_keys[pg.K_w]):
        GAME = False
        pg.time.delay(100)

