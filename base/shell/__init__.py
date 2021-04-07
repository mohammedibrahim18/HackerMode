import cmd
import os
import pathlib
import threading
import time
import re
import json

from typing import List, Tuple
from config import Config
from docsReader import DocsReader
from system import System, AppApi

from N4Tools.terminal import terminal
from N4Tools.Design import Color
from rich import print

from .shelltheme import ShellTheme

terminal = terminal()


class BaseShell(cmd.Cmd):
    ToolName: str = 'Main'
    is_error: bool = False
    Path: Tuple[str] = (
        x + '/'
        if os.path.isdir(os.path.join('.', x))
        else x + ' '
        for x in os.listdir('.')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = ShellTheme.prompt(self)

    def pathCompleter(self, text: str, args):
        if not text:
            a = self.Path
        else:
            a = [f for f in self.Path if f.startswith(text)]
        e = args.strip().split(' ')[-1]
        if e in self.Path: return self.viewdir(e)
        e = (e.split('/'))
        if os.path.isdir('/'.join(e[:-1])): return [
            f + '/' if os.path.isdir('/'.join(e[:-1]) + '/' + f) else f + ' '
            for f in os.listdir('/'.join(e[:-1])) if f.startswith(e[-1])
        ]
        return a

    def viewdir(self, path: str) -> List[str]:
        return [
            x + '/'
            if os.path.isdir(os.path.join(path, x))
            else x + ' '
            for x in os.listdir(path)
        ]

    def cmdloop(self, intro=None):
        return cmd.Cmd.cmdloop(self, intro)

    def default(self, line: str):
        if self.ToolName.lower() == 'main':
            # allow linux commands in Main mode only
            try:
                a = os.system(line)
                self.Path = self.viewdir(pathlib.PurePath())
                if a != 0:
                    if System.PLATFORME == 'termux':
                        self.is_error = True
                        os.system(f'/data/data/com.termux/files/usr/libexec/termux/command-not-found "{line}"')
            except:
                pass

    def completedefault(
            self,
            text: str,
            line: str,
            begidx: int,
            endidx: int
    ) -> List[str]:

        if len(line.split(' ')) == 1:
            # linux commands complete
            return [
                a[begidx:] for a in self.completenames(line, line, begidx, endidx)
            ]
        if len(l := line.split(' ')) > 1 and [ x for x in re.findall('([\W]*)',l[-1])if '/' not in x and x ]: # -^[ ...
            # path complete
            return [
                a[len(l[-1].split('/')[-1]) - len(text):]
                for a in self.pathCompleter(l[-1], line)
            ]
        return self.pathCompleter(text, line)

    def completenames(
            self,
            text: str,
            *ignored
    ) -> List[str]:

        base_commands: Tuple[str] = ('ls','c','cd','clear','EOF','exit','help')

        packages: List[str] = [
            # add class command to shell
            a[3:] for a in self.get_names()
            if a.startswith('do_' + text)
        ]

        if self.ToolName.lower() != 'main':
            packages = [i for i in packages if i not in base_commands]

        # complete linux commands and HackerMode commands
        # in Main mode only.
        if self.ToolName.lower() != 'main': return packages

        packages += [
            # add HakerMode commands to shell
            a for a in System.HACKERMODE_PACKAGES
            if a.startswith(text)
        ]
        packages += [
            # add linux commands to shell
            a for a in System.SYSTEM_PACKAGES
            if a.startswith(text)
        ]
        return list(set(packages))

    def postcmd(self, stop: bool, line: str):
        self.prompt = ShellTheme.prompt(self)
        return stop

    def onecmd(self, line: str):
        cmd, arg, line = self.parseline(line)
        self.is_error = False
        if not AppApi.activ():
            exit("# Time out.\n# Refresh the time from within the 'Hacker Mode' application.")
        if not line.strip():
            if Config.get("settings","LAST_COMMAND",default=False):
                return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd.replace('-', '_'))
            except AttributeError:
                return self.default(line)
            return func(arg)

    def do_ls(self, arg: str):
        if System.PLATFORME == 'termux':
            os.system('ls ' + arg)
            return

        if arg:
            os.system('ls ' + arg)
            return

        path = str(pathlib.Path.cwd() if not os.path.exists(arg) else arg)
        files = os.popen('ls').read()
        files = files.split('\n')
        c = Color().reader

        output = []
        for i in files:
            if os.path.isfile(os.path.join(path, i)):
                if i.split('.')[-1] in ('jpg','png'):
                    output.append(c(f'[$LPINK]{i}[$NORMAL]'))
                else:
                    output.append(c(f'[$NORMAL]{i}'))
                if ' ' in i:
                    i = f"'{i}'"
            elif os.path.isdir(os.path.join(path, i)):
                output.append(c(f'[$LBLUE]{i}[$NORMAL]'))
            else:
                output.append(i)

        list = output
        displaywidth = terminal.size['width']
        if not list:
            self.stdout.write("<empty>\n")
            return

        size = len(list)
        if size == 1:
            self.stdout.write('%s\n'%str(list[0]))
            return
        # Try every row count from 1 upwards
        for nrows in range(1, len(list)):
            ncols = (size+nrows-1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows*col
                    if i >= size:
                        break
                    x = Color().del_colors(list[i])
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(list)
            ncols = 1
            colwidths = [0]

        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows*col
                if i >= size:
                    x = ""
                else:
                    x = list[i]
                texts.append(x)

            for col in range(len(texts)):
                x = Color().del_colors(texts[col])
                padding = x.ljust(colwidths[col])
                texts[col] += padding[len(x):]
            self.stdout.write("%s\n"%str("  ".join(texts)))

    def do_cd(self, arg: str):
        try:
            if arg in ['~', '$HOME', '']:
                os.chdir(str(pathlib.Path.home()))
                self.Path = self.viewdir(pathlib.PurePath())
            else:
                os.chdir(os.path.join(os.getcwd(), arg))
                self.Path = self.viewdir(pathlib.PurePath())
            self.prompt = ShellTheme.prompt(self)
        except FileNotFoundError as e:
            print(e)
        except NotADirectoryError as e:
            print(e)

    def do_c(self, line: str):
        os.system('clear')

    def do_clear(self, line: str):
        os.system('clear')

    def complete_help(self, *args) -> List[str]:
        if self.ToolName.lower() == 'main':
            commands = set(
                [
                    a for a in System.HACKERMODE_PACKAGES
                    if a.startswith(args[0])
                ]
            )
        else:
            commands = set([])
        topics = set(a[5:] for a in self.get_names()
                     if a.startswith('help_' + args[0]))
        return list(commands | topics)

    def do_help(self, arg: str):
        def help_xml_path(package):
            language = Config.get('settings','LANGUAGE',default='ar')
            return os.path.join(
                os.path.join(System.BASE_PATH, f"helpDocs/{language}"), package
            )

        try:
            if self.ToolName.lower() == 'main' and not arg.strip():
                # to show hakcermode help menu.
                obj = DocsReader(
                    f'{help_xml_path(System.TOOL_NAME.lower())}.xml')

            elif self.ToolName.lower() != 'main' and not arg.strip():
                # to show shell help menu.
                obj = DocsReader(
                    f'{help_xml_path(self.ToolName.split(".")[0])}.xml')

            else:
                # to show any package help menu.
                obj = DocsReader(
                    f'{help_xml_path(arg)}.xml')
            obj.style()
            return
        except FileNotFoundError:
            self.stdout.write("%s\n" % str(self.nohelp % (arg,)))

    def do_main(self, arg):
        if self.ToolName.lower() != 'main':
            exit()

    def do_EOF(self, line):
        print('\n# to exit write "exit"')

    def do_exit(self, line):
        exit()


class HackerModeCommands(BaseShell):
    def get_package_ext(self, package: str) -> bool:
        bin: List[str] = os.listdir(
            os.path.join(System.BASE_PATH, 'bin')
        )
        tools: List[str] = os.listdir(
            os.path.join(System.BASE_PATH, 'tools')
        )
        for file in bin:
            if ''.join(file.split('.')[0:-1]) == package: return file
        for dir in tools:
            if package == dir:
                for path, dirs, files in os.walk(
                        os.path.join(
                            System.BASE_PATH, f'tools/{dir}'
                        )
                ):
                    for main_file in files:
                        if main_file.startswith('main'):
                            return main_file
        return False

    def default(self, line: str):
        package = self.get_package_ext(line.split(' ')[0])
        tool_name = line.split(' ')[0]
        arg = ' '.join(line.split(' ')[1:])
        run = f'python3 -B  {os.path.join(os.path.join(System.BASE_PATH, "bin"), "run.py")}'
        try:
            if os.path.isfile(file := os.path.join(os.path.join(System.BASE_PATH, "bin"), package)):
                os.system(f'{run} {file} {arg}')
                return
            if os.path.isdir(folder := os.path.join(System.BASE_PATH, f"tools/{tool_name}")):
                if not package:
                    print("# HackerMode can't find main file")
                    print("# in {tool_name}.")
                    print("# this is 'Developer Error'")
                    return
                try:
                    system_path = os.getcwd()
                    os.chdir(folder)
                    os.system(f'{run} {package} {arg}')
                except:
                    pass

                finally:
                    os.chdir(system_path)
                return
        except:
            pass
        super(HackerModeCommands, self).default(line)


class Settings(HackerModeCommands):
    def do_SHOW_SETTINGS(self, arg):
        max_width: int= 0
        with open(Config.file) as file:
            data = json.load(file)
            if arg.strip():
                try:
                    data = data[arg]
                except KeyError:
                    print(f'# support only {data.keys()}')
            else:
                data = data['settings']
        for key in data.keys():
            max_width = len(key) if max_width < len(key) else max_width
        for key, value in data.items():
            print(key+' '*(max_width-len( key )+2), value)

    def do_SET_PROMPT(self, arg: str):
        try:
            prompt_theme = int(arg)
            themes = len(ShellTheme.prompts)
            if prompt_theme in list(range(themes)):
                Config.set('SETTINGS', 'prompt', prompt_theme)
                self.prompt = ShellTheme.prompt(self)
            else:
                raise IndexError()
        except:
            print(f'# support only {list(range(len(ShellTheme.prompts)))}')

    def do_SET_LANGUAGE(self, arg: str):
        lang_support: List[str] = os.listdir(
            os.path.join(System.BASE_PATH,"helpDocs")
        )
        if arg.strip() in lang_support:
            Config.set('settings','LANGUAGE',arg.strip())
            print('# DONE')
        else:
            print(f'# support only {lang_support}')

    def do_SET_ARABIC_RESHAPER(self, arg: str):
        if arg.title() == 'True':
            Config.set('settings','ARABIC_RESHAPER',True)
            print('# DONE')
        elif arg.title() == 'False':
            Config.set('settings','ARABIC_RESHAPER',False)
            print('# DONE')
        else:
            print(f'# support only {[True,False]}')

    def do_SET_LAST_COMMAND(self, arg: str):
        if arg.title() == 'True':
            Config.set('settings','LAST_COMMAND',True)
            print('# DONE')
        elif arg.title() == 'False':
            Config.set('settings','LAST_COMMAND',False)
            print('# DONE')
        else:
            print(f'# support only {[True,False]}')



class MainShell(Settings):
    def do_HackerMode(self, line: str):
        if line:
            os.system('HackerMode ' + line)
        if line.strip() in ['install', 'update', 'upgrade']:
            def refresh():
                time.sleep(1)
                os.system('HackerMode')

            threading.Thread(target=refresh).start()
            exit()

    def complete_HackerMode(self, text: str, *args) -> List[str]:
        argvs: List[str] = ['update', 'upgrade', 'install', 'check']
        return [argv for argv in argvs if argv.startswith(text)]
