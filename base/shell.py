import cmd, os, pathlib, threading, time
from N4Tools.terminal import terminal
from N4Tools.Design import Color
from system import System
from docsReader import DocsReader

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
[$LGREEN]╭───[$LBLUE][ [$LCYAN]{path}[$LBLUE] ][$LGREEN]#[$LBLUE][ [$LYELLOW]{ToolName} [$LBLUE]][$LGREEN]>>>\n\
[$LGREEN]│\n\
[$LGREEN]╰─>>>[$LWIHTE]$ [$WIHTE]')

class BaseShell(cmd.Cmd):
    ToolName = 'Main'
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

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.prompt = PROMPT(pathlib.Path.cwd().name, self.ToolName)

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
            self.prompt = PROMPT(pathlib.Path.cwd().name,self.ToolName)
        except FileNotFoundError as e:
            print(e)
        except NotADirectoryError as e:
            print(e)

    def do_c(self, line):
        print(chr(27)+"[2J\x1b[H",end='')

    def do_clear(self, line):
        os.system('clear')

class HackerModeCommands(BaseShell):
    for package in os.listdir(os.path.join(System.BASE_PATH,'bin')):
        function_name = package.split('.')[0]
        exec (f'''
        \rdef do_{function_name}(self,arg):
        run = 'python3 -B  {os.path.join(os.path.join(System.BASE_PATH,"bin"),"run.py")}'
        try:
            os.system(run+' {os.path.join(os.path.join(System.BASE_PATH,"bin"),package)} '+arg)
        except:pass
''')

        exec(f'''
                \rdef help_{function_name}(self,*arg):
                try:
                    obj = DocsReader('{os.path.join(os.path.join(System.BASE_PATH, "helpDocs"), function_name)}.html')
                    print (obj.style)
                except FileNotFoundError:
                    print ('Error: command not found')
    ''')

    for tool_name in os.listdir(os.path.join(System.BASE_PATH,'tools')):
        exec (f'''
        \rdef do_{tool_name}(self,arg):
        run = 'python3 -B  {os.path.join(os.path.join(System.BASE_PATH,"bin"),"run.py")}'
        tool_path = "{os.path.join(os.path.join(System.BASE_PATH,"tools"),tool_name)}"
        system_path = os.getcwd()
        main = ''
        for path,dirs,files in os.walk(tool_path):
            for file in files:
                if file.startswith('main'):
                    main = os.path.join(path,file)
                    break
            break
        if not main:
            print ("# HackerMode can't find main file")
            print ("# in {tool_name}.")
            print ("# this is 'Developer Error'")
            return

        try:
            os.chdir(tool_path)
            os.system(run+' '+main+' '+arg)
        except:pass
        
        finally:
            os.chdir(system_path)
''')

class MainShell(HackerModeCommands):

    def do_HackerMode(self, line):
        if line:
            os.system('HackerMode '+line)
        if line.strip() in ['install','update','upgrade']:
            def refresh():
                time.sleep(1)
                os.system('HackerMode')
            threading.Thread(target=refresh).start()
            exit()

    def do_EOF(self, line):
        print ('\n# to exit write "exit"')
        return True

    def do_exit(self, line):
        exit()

if __name__ == '__main__':
    print(MainShell().__dir__())
    MainShell().cmdloop()
