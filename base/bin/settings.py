import sys,os,json
sys.path.append(os.path.abspath(__file__).split('/bin')[0])
from shell import BaseShell
from pygments import highlight
from pygments.lexers import HtmlLexer,JsonLexer
from pygments.formatters import TerminalFormatter
from N4Tools.Design import ThreadAnimation
class JSON:
    Path="/data/data/com.termux/files/home/.HackerMode/settings.json"
    def reader(self):
        with open(self.Path)as f:data=f.read()
        return json.loads(data)
    def Write(self,key,value):
        data=self.reader()
        data['settings'][key]=value
        with open(self.Path,'w')as f:f.write(json.dumps(data,indent=4));
class Settings(BaseShell):
    ToolName="Settings"
    Data=JSON().reader()
    isbool=False
    def do_options(self,arg):
        self.Lexer(self.Data)
    def Lexer(self,text):###
        @ThreadAnimation()
        def lexer(Thread):
            a=highlight(json.dumps(text,indent=4),JsonLexer(), TerminalFormatter())
            Thread.kill=True
            return('\r'+a)
        print(lexer())
    def do_set(self,value):
        d=(value.split(' '))
        if len(d)<2:print("\033[1;33mNot Value")
        elif d[0] not in self.Data["settings"]:print(f"\033[1;33mNot \033[1;31m{d[0]} \033[1;33min Settings")
        else:
            value=d[1]
            try:value=value if (not(value in ["true","false"])and self.isbool==True) else {"true":True,"false":False}[value]
            except:print("\033[1;33mValue not in \033[1;31m[\033[1;32mtrue\033[1;31m,\033[1;32mfalse\033[1;31m]")
            else:
                JSON().Write(d[0],value)
                self.Data=JSON().reader()
                print(f"\033[1;33m{d[0]}:\033[1;32m {value}")
    def complete_set(self,arg,*args):
        a,at=[a+" "for a in self.Data["settings"].keys()],[]
        Name=args[0].split("set ")[1]
        if Name in a:
            if type(self.Data["settings"][Name[:-1]])==bool:at=["true","false"];self.isbool=True
            return at
        else:
            if not arg:return a
            else:return[x for x in a if x.startswith(arg)]
    def do_get(self,arg):
        print(f"\033[1;32m{self.Data['settings'][arg]}")
    def complete_get(self,arg,*args):
        a=[x+' 'for x in self.Data['settings']]
        if not arg:return a
        else:return[x for x in a if x.startswith(arg)]
    def do_main(self,arg):return True
Settings().cmdloop()
