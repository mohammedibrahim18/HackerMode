import cmd,os,pathlib, threading, time
from N4Tools.terminal import terminal
from N4Tools.Design import Color
if __name__ == '__main__':
    from system import System
else:
    from base.system import System

Color = Color()
terminal = terminal()

# Normal:
# ┌───[ {pwd} ]#[ {ToolName} ]>>>
# │
# └─>>>$

# Smoth:
# ╭───[ {pwd} ]#[ {ToolName} ]>>>
# │
# ╰─>>>$
# ├

'''
PROMPT = lambda path,ToolName:Color.reader(f'\
[$LGREEN]┌───[$LBLUE][ [$LCYAN]{path}[$LBLUE] ][$LGREEN]#[$LBLUE][ [$LRED]{ToolName} [$LBLUE]][$LGREEN]>>>\n\
[$LGREEN]│\n\
[$LGREEN]└─>>>WL#$ W#')
'''

PROMPT = lambda path,ToolName:Color.reader(f'\
[$LGREEN]╭───[$LBLUE][ [$LCYAN]{path}[$LBLUE] ][$LGREEN]#[$LBLUE][ [$LRED]{ToolName} [$LBLUE]][$LGREEN]>>>\n\
[$LGREEN]│\n\
[$LGREEN]╰─>>>[$LWIHTE]$ [$WIHTE]')

class BaseShell(cmd.Cmd):
    prompt = PROMPT(pathlib.Path.cwd().name,'None')
    ruler = '='
    lastcmd = ''
    intro = None
    doc_leader = ""
    doc_header = "Documented commands (type help <topic>):"
    misc_header = "Miscellaneous help topics:"
    undoc_header = "Undocumented commands:"
    nohelp = "%s: command not found"
    use_rawinput = 1

    Path=[x+'/' if os.path.isdir(os.path.join('.',x))else x+' ' for x in os.listdir('.')]

    def propath(self,text,args):
        if not text:a=self.Path
        else:a=[f for f in self.Path if f.startswith(text)]
        e=args.strip().split(' ')[-1]
        if e in self.Path:return self.viewdir(e)
        e=(e.split('/'))
        if os.path.isdir('/'.join(e[:-1])):return [f+'/' if os.path.isdir('/'.join(e[:-1])+'/'+f) else f+' ' for f in os.listdir('/'.join(e[:-1])) if f.startswith(e[-1])]
        return a

    def viewdir(self,path):
        return [x+'/' if os.path.isdir(os.path.join(path,x)) else x+' ' for x in os.listdir(path)]

    def cmdloop(self, intro=None):
        #print ('cmdloop(%s)' % intro)
        return cmd.Cmd.cmdloop(self, intro)

    def postloop(self):
        #print ('postloop()')
        pass

    def default(self, line):
        try:
            os.system(line)
        except:pass
#        return cmd.Cmd.default(self, line)

    def completedefault(self, text, *args):
        return self.propath(text,args[0])

    def postcmd(self, stop, line):
        if len(line) == 0:
            return None
        return cmd.Cmd.postcmd(self, stop, line)

class BinCommands(BaseShell):
    for package in os.listdir(os.path.join(System.BASE_PATH,'bin')):
        exec (f'''
        \rdef do_{package[0:-3]}(self,arg):
        try:
            os.system('python3 {os.path.join(os.path.join(System.BASE_PATH,"bin"),package)} '+arg)
        except:pass
''')

class BaseCommands(BinCommands):
    def do_ls(self, arg):
        if System.PLATFORME == 'termux':
            os.system('ls '+arg)
            return

        if arg:
            os.system('ls '+arg)
            return

        path = str(pathlib.Path.cwd() if not os.path.exists(arg) else arg)
        files = os.popen('ls').read()
        files = files.split('\n')
        output = []
        for i in files:
            if os.path.isfile(os.path.join(path, i)):
                if i.endswith('.png') or i.endswith('.jpg'):
                    output.append('\033[1;95m' + i + '\033[0m')
                else:
                    output.append('\033[0;37m' + i + '\033[0m')
                if ' ' in i:
                    i = f"'{i}'"
            elif os.path.isdir(os.path.join(path, i)):
                output.append('\033[1;34m' + i + '\033[0m')
            else:
                output.append(i)
        self.columnize(output, displaywidth=terminal.size['width'])

    def do_cd(self, arg):
        try:
            if arg in ['~', '$HOME', '']:
                os.chdir(str(pathlib.Path.home()))
                self.Path=self.viewdir(pathlib.PurePath())
            else:
                os.chdir(os.path.join(os.getcwd(), arg))
                self.Path=self.viewdir(pathlib.PurePath())
            self.prompt = PROMPT(pathlib.Path.cwd().name,'None')
        except FileNotFoundError as e:
            print(e)
        except NotADirectoryError as e:
            print(e)

    def do_HackerMode(self, line):
        if line:
            os.system('HackerMode '+line)
        if line.strip() in ['install','update','upgrade']:
            def refresh():
                time.sleep(1)
                os.system('HackerMode')
            threading.Thread(target=refresh).start()
            exit()

    def do_c(self, line):
        print(chr(27)+"[2J\x1b[H",end='')

    def do_clear(self, line):
        os.system('clear')

    def do_EOF(self, line):
        print ('\n# to exit write "exit"')
        return True

    def do_exit(self, line):
        exit()

if __name__ == '__main__':
    print(BaseCommands().__dir__())
    BaseCommands().cmdloop()
