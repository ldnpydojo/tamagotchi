import select
import sys
import os
import contextlib   
import time
import tty
import termios

import fin.color
C = fin.color.C

import tam


WIDTH = 25
HEIGHT = 15

ACTIONS = {}

HELP = []
for a in ["quit", "feed", "drink", "play", "sleep", "wake"]:
    ACTIONS[a[0]] = a
    HELP.append("(%s)%s" % (C.blue(a[0]), a[1:]))
HELP = " ".join(HELP)


@contextlib.contextmanager
def raw_term():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def draw_at(data, x, y):
    print('\x1b[%s;%sH%s' % (y, x, data))

def draw_tamagotchi(tam):
    WIDTH = int(25 - (10 * (tam.attributes["hunger"]/100.0)))
    print( "\x1b[1;1H")

    # for teh lolz
    os.system("clear")
    
    face_col = C.blue
    if tam.attributes["thirst"] > 50:
        face_col = C.yellow

    draw_at(face_col("+" + "-" * (WIDTH-2) + "+"), 1,1)
    for i in range(HEIGHT-1):
        draw_at(face_col("\x1b[0G+" + " " * (WIDTH-2) + "+"), 1, i)
    draw_at(face_col("\x1b[0G+" + "-" * (WIDTH-2) + "+"), 1, i+2)
    
    #EYES
    col = C.yellow
    if tam.sleeping:
        col = C.red
    draw_at(col("x" if tam.sleeping else "o"), 5, 3)
    draw_at(col("x" if tam.sleeping else "o"), WIDTH-6, 3)

    #NOSE
    draw_at(C.blue("\\"), (WIDTH-1)/2, 7)
    draw_at(C.blue("-"), (WIDTH-1)/2, 8)

    #MOUTH
    if tam.attributes["unhappiness"] < 50:
        draw_at(C.blue("\_____/"), (WIDTH-6)/2, 12)
    else:
        draw_at(C.blue("/------\\"), (WIDTH-6)/2, 12)

    for i, (attr, value) in enumerate(tam.attributes.viewitems()):
        draw_at("%s: %s" % (attr, value), WIDTH+2, 3 + (i*2))

    draw_at(HELP, 1, HEIGHT+1)
    draw_at(str(time.time()), 1, HEIGHT + 2)    



def main():
    tamagotchi = tam.Tamagochi()
    now = time.time()
    with raw_term():
        
        while True:
            new_now = time.time()
            tamagotchi.update(new_now - now)
            now = new_now
            to_read, to_write, _ = select.select([sys.stdin], [], [], 0.1)
            if len(to_read):
                inp =  sys.stdin.read(1)
                print inp
                if inp == "q":
                    return
                if inp in ACTIONS:
                    getattr(tamagotchi, ACTIONS[inp])()
                
                
            draw_tamagotchi(tamagotchi)
            
                
    #tama = tamagotchi.Tamagotchi()

    while True:
        time.sleep(10)


if __name__ == "__main__":
  sys.exit(main())