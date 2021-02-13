from bs4 import BeautifulSoup
from N4Tools.Design import Text,Square,Color
from N4Tools.terminal import terminal
from config import Config

Text = Text()
Square = Square()
terminal = terminal()
Color = Color()

class DocsReader:
    def __init__(self,file):
        with open(file, 'r') as f:
            doc = f.read()
        self.soup = BeautifulSoup(doc, 'html.parser')

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

    @property
    def style(self):
        title = ''
        square_text = 6
        terminal_width = terminal.size['width']-square_text
        RULER = lambda : '[$WIHTE]' + '╌' * (terminal_width)

        if self.title:
            title = f"[$LBLUE]<<< [$LCYAN]{self.title}[$NORMAL] [$LBLUE]>>>"
            title = ' '*( (terminal_width//2)-(len(Color.del_colors(title))//2) )+title
            title = '\n'+title+'\n'

        sections = []
        temp = 0
        for section_title,commands in self.sections.items():
            sections.append('')
            sections[temp] += '[$WIHTE][$BOLD][$LBLUEBG] '+section_title+': [$NORMAL]\n'+RULER()+'\n'

            # commands
            tempFixwidth = [key for key in commands.keys()]
            tempFixwidth = Text.full(tempFixwidth)
            tempCommands = [key for key in commands.keys()]

            for command,helpMsg in commands.items():
                command = tempFixwidth[tempCommands.index(command)]
                if Config.get('settings','ARABIC_RESHAPER'):
                    helpMsg = Text.arabic(helpMsg)
                sections[temp] += '  [$YELLOW]'+command+'  [$WIHTE]'+helpMsg+'\n'

            sections[temp] += RULER()+'\n\n'
            temp += 1

        style = title+'\n'
        for section in sections:
            style += section

        Square.color = Color.LGREEN
        Square.center = True
        temp = '[$LBLUE][[$LYELLOW]+[$LBLUE]]'
        Square.square = [
            temp,
            ' │ ',
            temp,
            '─',
            temp,
            ' │',
            temp,
            '─']
        return Square.base(style[:-1])