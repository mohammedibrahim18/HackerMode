import curses.panel
from time import sleep
from threading import Thread
from curses.textpad import rectangle

import os
import curses


# Import -> Games
from Game_snake import Screen


class Run_Games:
    def __init__(self, Games):
        Games["Exit"] = self.Exit
        self.Games = Games
        
    def box_panel(self, height, width, x, y, text,color) -> curses.panel:
        #win = curses.newwin(height, width, y - (), x - (width))
        win = curses.newwin(height, width, x,y)
        win.erase()
        win.box()
        win.addstr(1,width // 2 - (len(text) // 2), text,curses.color_pair(color if text != "Exit" else 2))
        win.addstr(2,1,"─"*(width - 2))
        win.addstr(2,width-1,"┤")
        win.addstr(2,0,"├")
        Panel = curses.panel.new_panel(win)
        return Panel
    
    def Screen(self, stdscr) -> int:
        size = os.get_terminal_size()
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        history = {"size": os.get_terminal_size()}
        title = "Games"
        index_Page = 0
        Key = ""
        Data = {}
        # Colors
        curses.start_color()
        curses.init_pair(1,curses.COLOR_BLUE,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
        Games = self.Games
        while (size := os.get_terminal_size()):
    
            size = [size[0] - 2, size[1] - 2]
            if size != history["size"]:
                stdscr.clear()
            # panels
            for x in range(len(Games)):
                exec(f"""Data["pa{x}"] = self.box_panel(5,10 ,3+ x+(x - 1),4 + x+(x - 1 ),"{list(Games.keys())[x]}",1) """)
            
            # Commands
            if Key == curses.KEY_UP:
                if index_Page >0:
                    index_Page -= 1
                Data[f"pa{index_Page}"].top()
            elif Key == curses.KEY_DOWN:
                if index_Page <len(Games) - 1:
                    index_Page += 1
                Data[f"pa{index_Page}"].top()
            elif Key == ord('c'):
                stdscr.clear()
            elif Key == 10:
                return index_Page
            
            
            # Screen
            stdscr.addstr(1,3,list(Games.keys())[index_Page] + "        ")
            rectangle(stdscr, 0, 0, size[1], size[0])
            stdscr.addstr(1,size[0] // 2 - (len(title) // 2), title)
            curses.panel.update_panels()
            stdscr.refresh()
            
            # data
            Key = stdscr.getch()
            history["size"] = size
        stdscr.clear()
    def Exit(self):
         print("\033[0;31m[\033[0;33m FINISH \033[0;31m] \033[0;34m-> \033[0;32mGame\033[0m")
         exit()
         
def Run():

    while True:
        Data = {
    # (Name-Games := NameFile) : Method-Games
    "Simple" : Screen(0).Game(),
    "Average" : Screen(1).Game(),
    "Hard" : Screen(2).Game(),
    "No loss" : Screen(3).Game()
    }
        Players = Run_Games(Data)
        index = curses.wrapper(Players.Screen)
        Games = list(Players.Games.values())
        Name = list(Players.Games.keys())
        if index == len(Games) - 1:
            Games[index]()
        print(f"\033[0;31m[\033[0;33m Game \033[0;31m] \033[0;34m-> \033[0;32m{Name[index]}\033[0m")
        try:
            curses.wrapper(Games[index])
        except Exception as e:
            print (e)
            exit()
#            break


try:
    Run()
except KeyboardInterrupt:
    pass
except Exception as e:
    print(e)
        
