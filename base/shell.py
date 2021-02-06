import cmd,os,pathlib
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

    def cmdloop(self, intro=None):
        #print ('cmdloop(%s)' % intro)
        return cmd.Cmd.cmdloop(self, intro)

    def postloop(self):
        print ('postloop()')
        pass

    def default(self, line):
        #print ('default(%s)' % line)
        return cmd.Cmd.default(self, line)

    def completedefault(self, *ignored):
        return ['test']

    def postcmd(self, stop, line):
        #print (f'# commands stop:[{stop}],line[{line}]')
        if len(line) == 0:
            return None
        return cmd.Cmd.postcmd(self, stop, line)

class BinCommands(BaseShell):
    for package in os.listdir(os.path.join(System.BASE_PATH,'bin')):
        exec(f'''
    \rdef do_{package[0:-3]}(self,arg):
        os.system(\'{"python3 -B "+os.path.join(os.path.join(System.BASE_PATH,'bin'),package)}\')
''')

class BaseCommands(BinCommands):
    def do_ls(self, arg):
        path = str(pathlib.Path.cwd())
        files = os.popen('ls').read()
        files = files.split('\n')
        output = ''
        for i in files:
            if os.path.isfile(os.path.join(path, i)):
                if i.endswith('.png') or i.endswith('.jpg'):
                    output += '\033[1;95m' + i + ' '
                else:
                    output += '\033[0;37m' + i + ' '
                if ' ' in i:
                    i = f"'{i}'"
            elif os.path.isdir(os.path.join(path, i)):
                output += '\033[1;34m' + i + ' '
            else:
                output += i
        output = output[0:-8].split(' ')
        self.columnize(output, displaywidth=terminal.size['width'])

    def do_cd(self, arg):
        try:
            if arg in ['~', '$HOME', '']:
                os.chdir(str(pathlib.Path.home()))
            else:
                os.chdir(os.path.join(os.getcwd(), arg))
            self.prompt = PROMPT(pathlib.Path.cwd().name,'None')
        except FileNotFoundError as e:
            print(e)
        except NotADirectoryError as e:
            print(e)

    def do_HackerMode(self, line):
        print('# command: HackerMode '+line)

    def do_c(self, line):
        print(chr(27)+"[2J\x1b[H")

    def do_clear(self, line):
        print(chr(27)+"[2J\x1b[H")

    def do_nano(self, line):
        os.system('nano '+line)

    def do_EOF(self, line):
        "Exit"
        return True

    def do_quit(self, line):
        exit()

if __name__ == '__main__':
    print(BaseCommands().__dir__())
    BaseCommands().cmdloop()