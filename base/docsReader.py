from bs4 import BeautifulSoup
from N4Tools.Design import Text as Text,Square,Color
from N4Tools.terminal import terminal
from config import Config
from rich import print
from rich import box
from rich.align import Align
from rich.console import RenderGroup
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout


Text = Text()
Square = Square()
terminal = terminal()
Color = Color()

class DocsReader:
    def __init__(self,file):
        self.file = file
        with open(file, 'r') as f:
            doc = f.read()
        self.soup = BeautifulSoup(self.ValuesReader(doc), 'html.parser')

    @property
    def title(self):
        try:
            return self.soup.find('title').text
        except:
            return None

    @property
    def sections(self):
        data = {}
        for section in self.soup.find_all('section'):
            data[section['title']] = {}
            for command in section.find_all('line'):
                 data[section['title']][command['command']] = command.text
        return data

    def ValuesReader(self,text):
        text = text.replace('{{ TOOL_NAME }}',self.file.split('/')[-1].split('.')[0])
        return text

    def style(self):
        title = 'HELP MESSAGE'
        square_text = 6
        terminal_width = terminal.size['width'] - square_text
        RULER = lambda: '[white]' + '╌' * (terminal_width)

        if self.title:
            title = f"[cyan]{self.title.upper()}[/cyan]"

        sections = []
        temp = 0
        for section_title, commands in self.sections.items():
            sections.append('')
            sections[temp] += f'[white][bold][on blue] {section_title}: [/on blue]\n' + RULER() + '\n'

            # commands
            tempFixwidth = [key for key in commands.keys()]
            tempFixwidth = Text.full(tempFixwidth)
            tempCommands = [key for key in commands.keys()]

            for command, helpMsg in commands.items():
                command = tempFixwidth[tempCommands.index(command)]
                if Config.get('settings', 'ARABIC_RESHAPER'):
                    helpMsg = Text.arabic(helpMsg)
                sections[temp] += '  [yellow]' + command + '  [white]' + helpMsg + '\n'

            sections[temp] += RULER() + '\n\n'
            temp += 1

        style = ''
        for section in sections:
            style += section

        print (
            Panel(
                style[:-2],
                box=box.ROUNDED,
                padding=(1, 2),
                title=title,
                border_style='green',
            )
        )

