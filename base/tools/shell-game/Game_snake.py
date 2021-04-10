from curses import wrapper
from random import randint
from threading import Thread
from curses.textpad import rectangle


import os
import time
import curses






class Screen:
    def __init__(self,Mode):
        self.Mode = Mode
    def Main(self,stdscr):
        
        
        
       
        Live = 10
        tab = "∎"
        size = os.get_terminal_size()
        x,y = (size[0]-1 ) // 2, (size[1]) // 2
        hi = [[x,y]]
        timerx = (0.2 if self.Mode < 1 else 0.1)
        timerx = 0.07 if self.Mode >= 2 else timerx
        timery = timerx + .04
        timer = timerx
        hicom = 0
        linum = 1
        is_exit = False
        Live_y,Live_x = randint(2,size[1]-3), randint(1,size[0]-2)
        
        global c
        # Colors 
        curses.start_color()
        curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_CYAN,curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        stdscr.clear()    
        
        def snck(*args):
            stdscr.addstr(*args, curses.color_pair(1))
        #curses.curs_set(0)
        def refresh():
            t = f"Live -> {Live}\n "
            stdscr.addstr(0,size[0]//2 - (len(t)//2),t, curses.color_pair(3))
            rectangle(stdscr,1,0,size[1]-2,size[0]-1)
            snck(y,x,tab)
            stdscr.addstr(Live_y,Live_x,["✣","✢","✤","✥","✦"][linum%5], curses.color_pair(2))
            
    
        refresh()
        global c
        c = stdscr.getch()
        def cc():
            global c
            while not is_exit:
                c = stdscr.getch()
        Thread(target=cc,daemon=True).start()
        d,r,l,u = 0,0,0,0
        hi_size = size
        while True:
                stop = False
                size = os.get_terminal_size()
                is_out = False
                if ((x ==0  or x == size[0]-1) or (y == 1 or y== size[1]-2)):
                    if self.Mode == 3:
                        is_out = True
                    else:
                        break
                if c == curses.KEY_DOWN or c == ord('k'): #Down
                    if d == 0:
                        if hicom == 2:
                            snck(hi[-1][1],hi[-1][0],"╮")
                        elif hicom == 3:
                            snck(hi[-1][1],hi[-1][0],"╭")
    
                    hicom = 1
                    y += 1
                    r,l,u = 0,0,0
                    d += 1
                    tab = "│"
                    timer = timery
                    if is_out:
                        y = 2
    
                elif c == curses.KEY_RIGHT or c == ord('l'): #>'
                    if r == 0:
                        if hicom == 1:
                            snck(hi[-1][1],hi[-1][0],"╰")
    
                        elif hicom == 4:
                            snck(hi[-1][1],hi[-1][0],"╭")
    
                    x += 1
                    d,l,u = 0,0,0
                    r += 1
                    hicom = 2
                    
                    timer = timerx
                    if is_out:
                        x = 2
                    tab = "─"

                elif c == curses.KEY_LEFT or c == ord('h'):
                    if l == 0:
                        if hicom == 4:
                            snck(hi[-1][1],hi[-1][0],"╮")
    
                        elif hicom == 1:
                            snck(hi[-1][1],hi[-1][0],"╯")
    
                            
                    x -= 1
                    d,r,u = 0,0,0
                    l += 1
                    hicom = 3
                    tab = "─"
                    timer = timerx
                    if is_out:
                        x = size[0] - 2

    
                elif c == curses.KEY_UP or c == ord('j'):
                    y -= 1
                    
                    tab = "│"
                    if u == 0:
                        if hicom == 2:
                            snck(hi[-1][1],hi[-1][0],"╯")
                        elif hicom == 3:
                            snck(hi[-1][1],hi[-1][0],"╰")
    
    
                    d,r,l = 0,0,0
                    u += 1
                    hicom = 4
                    timer = timery
                    if is_out:
                        y = size[1] - 3
                elif c == ord('c'):
                    stdscr.clear()
                elif c == ord('q'):
                    break
                else:
                    if hicom == 1: y += 1
                    elif hicom == 2: x += 1
                    elif hicom == 3: x -= 1
                    elif hicom == 4: y -= 1
                i = 0
                
                
                if x == Live_x and y == Live_y:
                    Live_x = randint(1,size[0]-2)
                    Live_y = randint(2,size[1]-3)
                    Live += 1
                refresh()
    
                if not stop:
                    
                    if len(hi) > Live:
                        hi = hi[1:]+[[x,y]]
                    else:
                        hi.append([x,y])
                    if  hi[0] not in hi[1:]:
                        stdscr.addstr(hi[0][1],hi[0][0]," ")

                        

                        

                linum += 1       

                stdscr.refresh()
                time.sleep(timer)
                is_size =    size

                
        is_exit = True
        stdscr.clear()
    def Game(self):
         return self.Main

