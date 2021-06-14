#!/usr/bin/python3

#import sys
import pygame as pg
# from render import Color
import algorithms
import render
import parsing



FRAMETIME = 100


MAP = "olivier"
SCENARIO = 1


yard, graph, units, trains = parsing.parse_map(f"maps/{MAP}/main.map")
scenario = parsing.parse_scenario(f"maps/{MAP}/{SCENARIO}.scenario")
print(scenario)

X, Y = len(yard[0]), len(yard)

display = pg.display.set_mode((X * render.BLOCK_SIZE, Y * render.BLOCK_SIZE), pg.RESIZABLE)

sc = render.init_main_surface(X, Y)

pg.display.set_caption(f"[AUTO] marshalling yard model {MAP}")

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
        
    # Scenario processing

    for t in scenario.get_waiting_tasks():
        print(t.cmd, t.params)
        if (t.cmd == "MV" or t.cmd == "MVH" or t.cmd == "SMVH"):
            if len(t.params) == 4:
                who, *pos = map(int, t.params)
                path = algorithms.FindPath(trains[who], graph, tuple(pos), safe=(t.cmd[0] == 'S')).gen_path()
                #print(path)
                if path is None:
                    continue
                trains[who].set_path(path)
                scenario.start_task(t.id, (lambda who: trains[who].path is None), who)
            else:
                raise Exception(f"Wrong syntax of task {t.id}: {t.cmd} {' '.join(t.params)}")
        if (t.cmd == "MVT" or t.cmd == "SMVT"):
            if len(t.params) == 4:
                who, *pos = map(int, t.params)
                path = algorithms.FindPath(trains[who], graph, tuple(pos), side="tail", safe=(t.cmd[0] == 'S')).gen_path()
                #print(path)
                if path is None:
                    continue
                trains[who].set_path(path)
                scenario.start_task(t.id, (lambda who: trains[who].path is None), who)
            else:
                raise Exception(f"Wrong syntax of task {t.id}: {t.cmd} {' '.join(t.params)}")
        if (t.cmd == "C"):
            if (len(t.params) == 2):
                who, unit_id = map(int, t.params)
                success = trains[who].couple(graph, units[unit_id])
                if not success:
                    continue
                scenario.start_task(t.id, (lambda: True))
            else:
                raise Exception(f"Wrong syntax of task {t.id}: {t.cmd} {' '.join(t.params)}")
        if (t.cmd == "UC"):
            if (len(t.params) == 2):
                who, amount = map(int, t.params)
                trains[who].uncouple(amount)
                scenario.start_task(t.id, (lambda: True))
            else:
                raise Exception(f"Wrong syntax of task {t.id}: {t.cmd} {' '.join(t.params)}")
        if (t.cmd == "L"):
            if (len(t.params) == 3):
                who, count = map(int, t.params[:2])
                good_name = t.params[2]
                units[who].load(count, good_name)
                scenario.start_task(t.id, (lambda: True))
            else:
                raise Exception(f"Wrong syntax of task {t.id}: {t.cmd} {' '.join(t.params)}")            
        if (t.cmd == "UL"):
            if (len(t.params) == 2):
                who, count = map(int, t.params)
                units[who].unload(count)
                scenario.start_task(t.id, (lambda: True))
            else:
                raise Exception(f"Wrong syntax of task {t.id}: {t.cmd} {' '.join(t.params)}")


    scenario.process()

    # Exit confitions
    pressed_keys = pg.key.get_pressed()
    if pressed_keys[pg.K_LCTRL] and (pressed_keys[pg.K_c] or pressed_keys[pg.K_d] or pressed_keys[pg.K_w]):
        GAME = False
        pg.time.delay(100)

