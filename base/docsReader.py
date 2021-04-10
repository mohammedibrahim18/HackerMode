from bs4 import BeautifulSoup
from N4Tools.Design import Text, Square, Color
from N4Tools.terminal import terminal
from config import Config
from rich import print
from rich import box
from rich.panel import Panel

Text = Text()
Square = Square()
Color = Color()


class DocsReader:
    def __init__(self, file):
        self.file = file
        with open(file, 'r') as f:
            doc = f.read()
        self.soup = BeautifulSoup(self.values_reader(doc), 'html.parser')

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
            data[section['title']] = []
            for command in section.find_all('line'):
                data[section['title']] += [[command['command'], command.text]]
        return data

    def values_reader(self, text):
        text = text.replace('{{ TOOL_NAME }}', self.file.split('/')[-1].split('.')[0])
        return text

    def style(self):
        title = 'HELP MESSAGE'

        def terminal_width(width: int) -> int:
            '''controle the ruler width
            max width = 1
            minmim width = 0
            '''
            square_text = 6
            terminal_width = terminal().size['width'] - square_text
            return int(terminal_width * float(width) / float(1))

        # RULER = lambda: '[white]' + '─' * (terminal_width(1))
        RULER = lambda: f'[bold][white]{"─" * terminal_width(1)}[/bold][/white]'

        if self.title:
            title = f"[bold][green]{self.title.upper()}[/green]"

        sections = []
        temp = 0
        for section_title, commands in self.sections.items():
            sections.append('')
            sections[temp] += f'[white][bold] {section_title.lower()}: [/bold]\n' + RULER() + '\n'

            # commands
            tempFixwidth = [key[0] for key in commands]
            tempFixwidth = Text.full(tempFixwidth)
            tempCommands = [key[0] for key in commands]

            for command, helpMsg in commands:
                command = tempFixwidth[tempCommands.index(command)]
                if Config.get('settings', 'ARABIC_RESHAPER'):
                    helpMsg = Text.arabic(helpMsg)
                sections[temp] += f'  [yellow]{command}[/yellow]  [white]{helpMsg}\n'

            # sections[temp] += RULER() + '\n\n'
            sections[temp] += '\n\n'
            temp += 1

        style = ''
        for section in sections:
            style += section

        print(
            Panel(
                style[:-3],
                box=box.ROUNDED,
                padding=(1, 2),
                title=title,
                border_style='bold green',
            )
        )
