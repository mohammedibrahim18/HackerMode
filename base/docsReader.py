from bs4 import BeautifulSoup
from N4Tools.Design import Text,Square,Color
from N4Tools.terminal import terminal
from system import System

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
        return self.soup.find('title').text

    @property
    def sections(self):
        data = {}
        for section in self.soup.find_all('section'):
            data[section['title']] = {command['command']:command.text for command in section.find_all('line')}
        return data

    @property
    def style(self):
        title = '\n'
        square_text = 6
        terminal_width = terminal.size['width']-square_text
        RULER = lambda : '[$WIHTE]' + '╌' * (terminal_width)
        if self.title:
            title = f"<[ [$LCYAN]{self.title}[$NORMAL] ]>"
            title = ' '*( (terminal_width//2)-(len(Color.del_colors(title))//2) )+title
            title = '\n'+title+'\n'

        sections = []
        temp = 0
        for section_title,commands in self.sections.items():
            sections.append('')
            sections[temp] += ' '+section_title+':\n'+RULER()+'\n'

            # commands
            tempFixwidth = [key for key in commands.keys()]
            tempFixwidth = Text.full(tempFixwidth)
            tempCommands = [key for key in commands.keys()]

            for command,helpMsg in commands.items():
                command = tempFixwidth[tempCommands.index(command)]
                if System.PLATFORME == 'termux':
                    helpMsg = Text.arabic(helpMsg)
                sections[temp] += '  '+command+'  '+helpMsg+'\n'

            sections[temp] += '\n'
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