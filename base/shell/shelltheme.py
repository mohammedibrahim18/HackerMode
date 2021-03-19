import pathlib
import datetime

from config import Config
from N4Tools.Design import Color

Color = Color()


class ShellTheme:

    @property
    def prompts(self):
        return [
            lambda root: Color.reader(
                f'[$/]╭───[$LBLUE][ [$LCYAN]{pathlib.Path.cwd().name}[$LBLUE] ][$/]#[$LBLUE][ [$LYELLOW]{root.ToolName} [$LBLUE]][$/]>>>\n│\n╰─>>>$ '
            ),
            # ╭───[ home ]#[ Main ]>>>
            # │
            # ╰─>>>$

            lambda root: Color.reader(
                f'[$/]╭[$LRED][[$LGREEN]{pathlib.Path.cwd().name}[$YELLOW]@[$LWIHTE]{root.ToolName}[$LRED]][$/]\n╰>>>$'
            ),
            # ╭[home@Main]
            # ╰>>>$D

            lambda root: Color.reader(
                f'[$/]╭[$LRED][[$LCYAN] {pathlib.Path.cwd().name} [$LRED]][$LWIHTE]-[$LRED][[$LWIHTE] {str(datetime.datetime.now()).split(" ")[-1].split(".")[0]} [$LRED]][$LWIHTE]-[$LRED][[$LYELLOW] {root.ToolName} [$LRED]]\n[$/]╰>>>$'),
            # ╭[ home ]-[ 11:41:02 ]-[ Main ]
            # ╰>>>$

            lambda root: Color.reader(
                f'[$BLUE]┌──[$LBLUE]([$LRED]HACKER💀MODE[$LBLUE])[$BLUE]-[$LBLUE][[$LYELLOW]{root.ToolName}[$LBLUE]][$BLUE]-[$LBLUE][[$/]{pathlib.Path.cwd().name}[$LBLUE]]\n[$BLUE]└─[$LRED]$[$/] '),
            # ┌──(HACKER💀MODE)-[Main]-[home]>>>
            # └─$

            lambda root: Color.reader(
                f'[$/]╭[$LRED]({"❌" if root.is_error else "✅"})[$/]─[$LGREEN]{{[$LYELLOW]home[$LRED]:[$LBLUE]Main[$LGREEN]}}[$/]>>>\n╰>>>$')
            # ╭(✅)─{home:Main}─>>>
            # ╰>>>$
        ]

    def prompt(self, root):
        try:
            Config.get('SETTINGS', 'prompt', cast=int)
        except KeyError:
            Config.set('SETTINGS', 'prompt', 0)
        prompt_theme = Config.get('SETTINGS', 'prompt', cast=int)
        return self.prompts[prompt_theme](root)


ShellTheme = ShellTheme()
