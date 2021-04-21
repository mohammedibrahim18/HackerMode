import os
import sys
import requests
import json
import re

from bs4 import BeautifulSoup

from N4Tools.Design import ThreadAnimation

from pygments import highlight
from pygments.lexers import HtmlLexer, JsonLexer
from pygments.formatters import TerminalFormatter

sys.path.append(os.path.abspath(__file__).split('/bin')[0])

from shell import BaseShell

app = """
# Flask - Server
from flask import Flask
from flask import render_template

from random import randint as PORT

app = Flask(__name__)

@app.route('/')
def index():
    # Code...
    return render_template('index.html')

app.run(port=PORT(999, 65535))
"""


class Source:
    def __init__(self, url, Name, html):
        # url -> domin
        self.url = url
        self.domin = '//'.join([x for x in url.split('/') if x][:2])
        self.html = BeautifulSoup(html, "html.parser")
        self.urls = []
        self.Name = Name
        # paths -> app
        self.Paths = [
            f"{Name}",
            f"{Name}/__main__.py",
            f"{Name}/static",
            f"{Name}/templates",
        ]

    def write(self, Name, text):
        with open(Name, "wb") as f:
            f.write(text)

    def Text(self, text):
        for nc in range(8):
            text = text.replace(f"${nc}", f"\033[1;3{nc}m")
        return text.replace("$$", "\033[0m")

    @ThreadAnimation()
    def Install(self, Thread, url):
        out = None
        try:
            out = requests.get(url)
        except Exception as e:
            print(f"\033[1;31mERROR    \033[1;32m: \033[0m{e}")
            out = None
        Thread.kill = True
        return out

    def Create(self, tag, attr, expr):
        Name = self.Name
        isurl = lambda u: True if re.findall('((http|ftp)s?://.*?)', get) else False
        for src in self.html.find_all(tag):
            if (get := src.get(attr)) and (get := get.strip()) and not get.endswith('/'):
                path = f"{{{{ url_for('static', filename='{get.split('/')[-1].replace(' ', '_')}') }}}}"
                if isurl(get):
                    self.urls.append(get)
                    src[attr] = path
                elif ((st := get.startswith('/')) or expr):
                    self.urls.append(self.domin + ("/" if not st else '') + get)
                    src[attr] = path

    def Setup(self):
        Name = self.Name
        # print -> Setup: NameFile
        for s in self.Paths:
            if not os.path.exists(s) and not s.endswith('index.py'):
                if s.endswith('__main__.py'):
                    # write __main__.py -> Flask server
                    self.write(s, app.encode())
                else:
                    os.mkdir(s)
                print(self.Text(f"$2Setup    $1: $$") + s)
            else:
                print(self.Text(f"$3Exists   $1: $$") + s)
        index = os.path.join(Name, "templates", "index.html")
        print(self.Text(f"$2Setup    $1: $$") + index)

    def Start(self):
        # Setup dir and file -> app
        self.Setup()
        self.Create("link", "href", True)
        self.Create("script", "src", True)
        self.Create("img", "src", True)
        #self.Create("meta", "content", False)
        self.write(os.path.join(self.Name, "templates", "index.html"), self.html.prettify().encode())

        for url in set(self.urls):
            path = os.path.join(self.Name, "static", url.split('/')[-1])
            print(self.Text(f"$2Download$1 :$$ {path}"))
            if (install := self.Install(url)):
                self.write(path, install.content)
            else:
                print(self.Text(f"$1ERROR    :$$ {url}"))


class Input(BaseShell):
    value = None

    def __init__(self, Prompt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Prompt = Prompt
        self.prompt = Prompt

    def completenames(self, arg, *args):
        all = ["file ", "url "]
        return [x for x in all if x.startswith(arg)] if arg else all

    def onecmd(self, *args):
        pass

    def Req(self, line):
        @ThreadAnimation()
        def _Req(Thread):
            try:
                r = requests.get(line)
            except Exception as e:
                print(e)
                Thread.kill = True
                return False
            Thread.kill = True
            return r

        return _Req()

    def postcmd(self, arg, line):
        Mode = line[:line.find(' ')]
        line = line[line.find(' '):].strip()
        if Mode == "file":
            if os.path.isfile(line):
                with open(line, 'r')as f:
                    self.value = ThreadAnimation()((lambda Thread: f.read()))()

                return line
            else:
                print("not File...!")
        elif Mode == "url":

            if (req := self.Req(line)) != False:
                self.value = req

                return line
        else:
            print('Enter File or url')
            self.prompt = self.Prompt


value = Input("\033[0;32mfile\033[0m -\033[0;33m url\033[0m ->\033[0m\n     -> ")
value.cmdloop()
value = value.value
if type(value) == str:
    html = BeautifulSoup(value, "html.parser")
    URL = None
else:
    html = BeautifulSoup(value.text, "html.parser")
    URL = value.url


class HtmlShell(BaseShell):
    ToolName = "Shell-Web.Html"

    for Tag in html.open_tag_counter.keys():
        Tag = Tag.replace('-', "_")
        exec(f"""


def do_{Tag}(self,arg):
	arg = BeautifulSoup(arg, "html.parser")
	a = lambda Name: {{ attr[0]: (' '.join(attr[1]) if type(attr[1]) == list else attr[1]) for x in arg.find_all(Name) for attr in x.attrs.items() }}
	get = a('get')
	_if = a(f'{{ "{Tag}" }}_if')
	g = self.GetAttr(arg, "{Tag}", _if)
	attr = [x for x in arg.text.split(' ')if x]
	Done = []
	if not g and not attr:
		for s in html.find_all("{Tag}", _if):
			print(self.Lexer_Html(s.prettify()))
	else:
		for s in html.find_all("{Tag}", _if):
			for p in attr:
				f = s.get(p)
				if f:
					if f not in Done:
						print(f"\033[1;32m{{ '{Tag}' }}\033[1;31m - \033[1;33m{{p}}\033[1;31m ->\033[1;37m",(' '.join(f) if type(f) == list else f),'\033[0m')
						Done.append(f)
		
		
def complete_{Tag}(self, arg, line, *args):
		al = html.{Tag}.attrs
		params = ' '.join([x[0]+' = '+'"'+(' '.join(x[1]) if type(x[1]) == list else x[1])+'"' for x in al.items()])
		com = {{
					"__get__":"<get   ></get>",
					"__if__":"<if   />",
					f"__{{ '{Tag}' }}_if__":f"<{{ '{Tag}' }}_if  {{ params }} />",
					"__attr__": "<attr   />"
		}}
		
		al = list(al)
		all = al + list(com.keys())
		if (l := line.split(' ')[-1]).endswith('-') or '-' in l:
			p = [
					x[len(l) - len(l[l.rfind('-'):]) + 1:] + ' ' 
					for x in al if x.startswith(l)
			]
 
			return [x for x in p if x.startswith(arg)] if arg else p
			
		out = [x for x in all if x.startswith(arg)] if arg  else list(all)
		 
		return [ com[ out[0] ] ] if len(out) == 1 and out[0] in list(com.keys()) else out
def help_{Tag}(self,*args):
		print(self.Lexer_Html("exaple:\
		\\r-> {Tag} class\
		\\r-> {Tag} class style <div_if class='Name' />\
		\\r-> {Tag} <get button  ></get>\
		\\r-> {Tag} <get button input  ></get>\
		\\r-> {Tag} <get button input  ><attr class name type /></get>\
		\\r-> {Tag} <get button input  ><if type='text' name='search'><attr type /></get>")[0:-1])
		""")

    def GetAttr(self, arg, tag, if_):
        get = []
        _if = {}
        attr = []
        Done = []
        for a in arg.find_all('get'):
            get += list(a.attrs.keys())
            for b in a.find_all('if'):
                for c in b.attrs.items():
                    _if[c[0]] = ' '.join(c[1]) if type(c[1]) == list else c[1]

            for d in a.find_all('attr'):
                for x in d.attrs.keys():
                    attr.append(x)

        for a in html.findChildren(tag, if_):
            for b in get:
                for x in a.find_all(b, _if):
                    if attr:
                        for g in attr:
                            s = x.get(g)
                            if s:
                                if s not in Done:
                                    print(f"\033[1;32m{b}\033[1;31m - \033[1;33m{g}\033[1;31m ->\033[1;37m",
                                          (' '.join(s) if type(s) == list else s), '\033[0m')
                                    Done.append(s)
                    else:
                        if x not in Done:
                            print(self.Lexer_Html(x.prettify()))
                            Done.append(x)

        return get != []

    def completenames(self, line, *args):
        all = [tag[3:].replace("_", "-") + ' ' for tag in self.get_names() if tag.startswith('do_')]
        return [x for x in all if x.startswith(line)] if line else all

    @ThreadAnimation()
    def Lexer_Html(self, Thread, Code):
        out = highlight(Code, HtmlLexer(), TerminalFormatter())
        Thread.kill = True
        return out

    def do_exit(self, arg):
        return True


class MainShell(BaseShell):  # Main Shell
    ToolName = "Shell-Web"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.Names = {"rest": []}  # Mode: [ Urls ]
        for x in re.findall('"((http|ftp)s?://.*?)"', html.prettify()):
            x = x[0]
            if x.endswith('/'):
                self.Names["rest"].append(x)
            else:
                line = x.split('/')[-1]
                if '.' in line:
                    line = line.split('.')[-1]
                    if [c for c in re.findall('[\W]*', line) if c] or '_' in line:
                        self.Names["rest"].append(x)
                    else:
                        if line in self.Names:
                            self.Names[line].append(x)
                        else:
                            self.Names[line] = [x]
                else:
                    self.Names["rest"].append(x)
        self.Names = {
            a: list(set(self.Names[a]))
            for a in sorted(list(self.Names.keys()))
        }

    def do_html(self, arg):  # html Shell
        HtmlShell().cmdloop()

    def do_Flask(self, arg):
        if URL:
            all = BeautifulSoup(arg, "html.parser")
            try:
                if (get := all.find("flask").get('filename')):
                    obj = Source(URL, get, html.prettify())
                    obj.Start()
                else:
                    print("Flask <flask filename='Name' />")
            except:
                print("Flask <flask filename='Name' />")
        else:
            print("Not URL...!")

    def complete_Flask(self, *args):
        return ["<flask filename=' ' />"]

    @ThreadAnimation()
    def Lexer_Json(self, Thread, Code):
        out = highlight(Code, JsonLexer(), TerminalFormatter())
        Thread.kill = True
        return out

    def do_Info(self, arg):
        if type(value) == str:
            print("Not info...!")
        elif len((f := [x for x in re.findall("[\W]*",arg.strip()) if x])) > 0:
            print(f"Not {f}...!")
        else:
            try:
                temp = eval(f'value.{arg}')
            except Exception as e:
                print("\033[1;31mERROR:\033[0m", e)
            else:
                if type(temp) == dict or arg == "headers":
                    print(
                        self.Lexer_Json(
                            str(
                                json.dumps(
                                    dict(temp),
                                    indent=3
                                )
                            )
                        )
                    )
                else:
                    print(temp)

    def complete_Info(self, line, *args):
        if type(value) == str:
            return ["None"]
        Del = ["text", "_content", "iter_content", "iter_lines", "json"]
        all = [
            x for x in dir(value)
            if not x.startswith('__') and x not in Del
        ]
        return [x for x in all if x.startswith(line)] if line else all

    def do_Link(self, arg):  # Links-Urls
        if arg:
            for x in (self.Names[arg]):
                print(f'\033[1;31m-> \033[1;37m{x}\033[0m')

    def complete_Link(self, line, *args):
        all = list(self.Names.keys()) + ["rest"]
        return [x for x in all if x.startswith(line)] if line else all


if __name__ == "__main__":
    MainShell().cmdloop()
