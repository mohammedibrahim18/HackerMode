import os,re,json
from N4Tools.Design import ThreadAnimation
from rich.table import Table
from rich.live import Live
from rich import box
from time import sleep
import sys, os

sys.path.append(os.path.abspath(__file__).split('/bin')[0])
from shell import BaseShell

class GetInfo:
    def __init__(self,path):
        self.path = path
    def getsize(self,num):
        G = num / 1024
        tmp = "KB"
        if G > 1024 :
            G,tmp = G / 1024, 'MB'
        if G > 1024 :
            G,tmp = G / 1024, 'GB'
        G = str(G).split('.')
        return f"{G[0]}.{G[1][0:2]} {tmp}"
    def dictinfo(self):
        #Mode      -> { NameFile : [ repeat , sizeAllrepeat , { NameFile : SizeFile } ] }
        #rest      -> [ SizeAll , { NameFile : SizeFile }]
        #in_repeat -> { NumSize  : {Num:[ Paths] } } 
        data={'Mode':{},
              'rest':[0, {}],
              'in_repeat': None}
        in_repeat = {}
        In_Repeat = {}
        def addrest(n, k, v):
            data['rest'][0] += n
            data['rest'][1][k] = v

        for p,d,f in os.walk(self.path):
            for Mode in f:
                path = os.path.join(p,Mode)
                size = os.path.getsize(path)
                get_size = self.getsize(size)
                #a=Mode.rfind('.')
                out = Mode[Mode.rfind('.'):][1:]
                if out:
                    if not (len([x for x in (re.findall('[\W]*',out))if x])>0) \
                    and '_' not in out and not out.isnumeric():
                        if out not in data['Mode']:
                            data['Mode'][out] = [1, size, {path: get_size}]
                        if out not in In_Repeat:
                            In_Repeat[out] = {}
                        if size not in in_repeat:
                            in_repeat[size] = path
                        else:
                            if size in In_Repeat[out]:
                                In_Repeat[out][size] += [in_repeat[size], path]
                            else:
                                In_Repeat[out][size] = [in_repeat[size], path]
                            In_Repeat[out][size] = list(set(In_Repeat[out][size]))
                        data['Mode'][out][0] += 1
                        data['Mode'][out][1] += size
                        data['Mode'][out][2][path] = get_size
#                        else:data['Mode'][out]=[1,size,{path:get_size}]
                    else:
                        addrest(size, path, get_size)
                else:
                    addrest(size, path, get_size)
        Mode={}
        for x in sorted(data['Mode']):
            info = data['Mode'][x]
            Mode[x] =data['Mode'][x] # [info[0], self.getsize(info[1]) ,info[2]]
        data['Mode'] = Mode
        data['rest'][0] = self.getsize(data['rest'][0])
        In_Repeat = {x: In_Repeat[x] for x in sorted(In_Repeat)}
        data['in_repeat'] = In_Repeat
        return data

@ThreadAnimation()
def GETdata(Thread, path):
    data = GetInfo(path).dictinfo()
    Thread.kill = True
    return data

class Input(BaseShell): #input...
      def __init__(self, P, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.P = P
        self.prompt = P
        self.value = '.'
        self.cmdloop()
      do_dir = lambda self, arg: 'pass'
      completenames = lambda self, *args: ['dir ']
      def postcmd(self, *args):
          self.prompt = self.P
          if os.path.isdir(self.value):
              return True
          else:
              print('Not Dir...!')
      def onecmd(self, line):
          line = line[line.find(' '):].strip()
          self.value = line


Data = GETdata(Input('\033[1;33mPath\033[1;36m~\033[1;31m/\033[1;37m$\033[0m').value)

class Main(BaseShell):
    ToolName = "Info-File"
    remove = []
    for x in Data['Mode'].keys():
        exec(f'''
def do_{x}(self, arg):
    if arg == 'paths' :
        self.paths("{x}")
    elif arg == "size_all" :
        print ('\033[0;33mSize_All \033[1;31m: \033[0;32m',GetInfo(".").getsize(Data["Mode"]["{x}"][1]))
    elif arg == 'repeat' :
        self.repeat("{x}")

def complete_{x}(self, arg, *args):
    all=['repeat', 'size_all',
         'paths',
        ]
    return all if not arg else [x for x in all if x.startswith(arg)]''')
    def paths(self, arg):
        table = Table(
                    expand=True, box=box.SQUARE_DOUBLE_HEAD,
                    title="Paths", title_style="none")
        table.add_column('Path', style="green")
        table.add_column('Size', style='blue')
        all = 0
        with Live(table, refresh_per_second=1)as live:
            for k,v in Data['Mode'][arg][2].items():
                if k not in self.remove:
                    table.add_row(k, str(v))
                    all += 1
        print (f'\033[0;33mPath_All\033[1;31m : \033[0;32m{all}\n\033[0;33mSize_All \033[1;31m: \033[0;32m{GetInfo(".").getsize(Data["Mode"][arg][1])}')

    def reader(self, path):
        with open(path, 'rb')as f:
            return f.read()

    def repeat(self, arg):
        all = Data['in_repeat'][arg]
        k = list(all.keys())
        P = []
        Done = []
        table = Table(
                    expand=True, box=box.SQUARE_DOUBLE_HEAD,
                    title="Repeat", title_style='none')
        table.add_column('Path', style='green')
        table.add_column('Size', style='blue')
        table.add_column("Mode", style="cyan")
        size_all = 0
        size_all_repeat = 0
        D = ''
        with Live(table)as live:
            a=[0]
            repeat_all=0
            for k,v in all.items():
                a[0]+=k
                a.append([k,v])#a.append([GetInfo('.').getsize(k),v])
            #print (json.dumps(a,indent=2))
            for x in a[1:]:
                S=GetInfo('.').getsize(x[0])
                if len(x[1]) == 2:
                    if self.reader(x[1][0]) == self.reader(x[1][1]):
                        size_all_repeat += x[0]
                        repeat_all += 1
                        table.add_row(x[1][0] , S, "orignal")
                        table.add_row(x[1][1] , S, "plus")
                elif len(x[1]) > 2:
                    original=x[1][0]
                    r=self.reader(original)
                    N = 0
                    for p in x[1][1:]:
                        if r == self.reader(p):
                            if N==0:
                                table.add_row(original, S, "original")
                            table.add_row(p,S,"plus")
                            size_all_repeat += x[0]
                            N+=1
                            repeat_all+=1
                    live.update(table)
        print (f'\033[0;33mRepeat_All\033[1;31m :\033[0;32m {repeat_all}\n\033[0;33mSize_All_Repeat \033[1;31m:\033[0;32m {GetInfo(".").getsize(size_all_repeat)}')
Main().cmdloop()

