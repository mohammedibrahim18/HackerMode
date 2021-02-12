from N4Tools.Design import Color,ThreadAnimation
import os,json,sys
sys.path.append(os.path.abspath(__file__).split('/bin')[0])
from shell import BaseShell
path=input(Color().reader('[$LYELLOW]Path[$GREEN]~[$LRED]/[$LWIHTE]$ [$WIHTE]'))

if not os.path.isdir(path):print(f"[Errno 20] Not a directory: '{path}'");exit()

def getsize(num):
	G=num/1024
	tmp="KB"
	if G>1024:G,tmp=G/1024,'MB'
	if G>1024:G,tmp=G/1024,'GB'
	G=str(G).split('.')
	return f"{G[0]}.{G[1][0:2]} {tmp}"

@ThreadAnimation()
def getnumpers(Thread):
	all={}
	for d,i,r in os.walk(path):
		for n in r:
			a=str(n[n.rfind('.'):][1:])
			p=(os.path.join(d,n))
			s=os.path.getsize(p)
			size=getsize(s)
			if a in all:all[a].append((p,size,s))
			else:all[a]=[(p,size,s)]
	Thread.kill=True
	return all



class NumFile(BaseShell):
	ToolName="infofile"
	all=getnumpers()
	DoneSearch={}
	for x in all.keys():
		if ' ' in x or '-' in x or '_' in x or x.isnumeric():pass
		else:
			exec(f'''\
			\rdef do_{x}(self,arg):
			@ThreadAnimation()
			def th(Thread):
				out=''
				if not arg:out=''
				elif arg=='num':
					out=(Color().reader("[$LYELLOW]Numper:[$LGREEN] ")+str(len(self.all['{x}'])))
				elif arg=='sizeall':out=Color().reader('[$LYELLOW]Sizeall:[$LGREEN] ')+getsize(sum([x[-1] for x in self.all['{x}']]))
				
				elif arg=='paths':
					for x in self.all["{x}"]:
						out+=Color().reader("[$LGREEN]"+x[0]+" [$LYELLOW]Size: [$LRED]"+x[1]+'\\n')
				Thread.kill=True
				return out[:-1] if out.endswith('\\n') else out
			if arg=='repeat':self.lops('{x}')
			elif arg=='delrepeat':self.lops('{x}',mode='rm')
			elif arg=='delpaths':self.delpaths("{x}")
			else:
				G=(th())
				if G:print(G)
			\rdef complete_{x}(self,arg,*args):
			a=['paths','repeat','sizeall','num','delrepeat','delpaths']
			if not arg:return a
			else:return [x for x in a if x.startswith(arg)]
			''')
	def Lexer(self,text):###
		a=highlight(text,JsonLexer(), TerminalFormatter())
		return('\r'+a)
	def delpaths(self,arg):
		point=lambda t:Color().reader(f'[$LYELLOW]Loading... [$LRED][ [$GREEN]{t}[$YELLOW]%[$GREEN]100 [$LRED]]')
		rm=0
		for x in self.all[arg]:
			os.system(f'rm {x[0]}')
			print(point(str(rm/len(self.all[arg])*100).split('.')[0]),end='\r')
			rm+=1
		print(point('100'),end='\r')
		
		self.all[arg]=[]
		print(' '*len(Color().del_colors(point('100'))),end='\r')
		print((Color().reader(f"[$LYELLOW]DelPaths:[$LGREEN] {rm}")))
	def lops(self,arg,mode='show'):
		point=lambda t:Color().reader(f'[$LYELLOW]Loading... [$LRED][ [$GREEN]{t}[$YELLOW]%[$GREEN]100 [$LRED]]')
		
		if arg in self.DoneSearch:
			if mode=='show':(self.styledata(self.DoneSearch[arg][0],self.DoneSearch[arg][1]));return None
			elif mode=='rm':
				self.Remove(arg,self.DoneSearch[arg][-1]);return None
				

		print(point('0'),end='\r')
		tmp,done,all,Num,i,rm,info=[],[],self.all[arg],0,0,0,[]
		All=list(self.all[arg])
		Doneremove=[]
		if mode=='rm':rem=list(self.all[arg])
		for x in all:
			try:
				with open(x[0],'rb')as f:tmp1=f.read()
				t=[]
				if x[0]not in done:
					for d in All:
						if not d[0]==x[0]:
							with open(d[0],'rb')as ff:tmp2=ff.read()
							if tmp1==tmp2:
								
								
								t.append(d[0]);i+=1 #tmp repeat
								done.append(d[0]) #Done repeat
								info.append(d)
								#elif mode=='rm':
								All.remove(d) #remove is done repeat
								
					if len(t+[x[0]])>1:tmp.append(t+[x[0]])
					print(point(str(Num/len(self.all[arg])*100).split('.')[0]),end='\r')
					Num+=1
			except FileNotFoundError as e:print(e)
		print(point('100'),end='\r')
		print(' '*len(Color().del_colors(point('100'))),end='\r')
		if mode=='show':
			if tmp:
				self.DoneSearch[arg]=[tmp,done,info]
				self.styledata(tmp,done)
			else:print((Color().reader("[$LYELLOW]Repeat:[$LGREEN] 0")))
		elif mode=='rm':
			self.Remove(arg,info)
			
	def styledata(self,tmp,done):
		if done==True:print((Color().reader("[$LYELLOW]Repeat:[$LGREEN] 0")));return None
		string=''
		for x in tmp:
			for p in range(len(x)):
				if p==0:string+='[$LYELLOW]╭[$LRED][[$LGREEN]'+x[p]+'[$LRED]]\n'
				elif p==len(x)-1:string+='[$LYELLOW]╰[$LRED][[$LGREEN]'+x[p]+'[$LRED]]\n'
				else:string+='[$LYELLOW]┝[$LRED][[$LGREEN]'+x[p]+'[$LRED]]\n'
		Repeat=((Color().reader("[$LYELLOW]Repeat:[$LGREEN] ")+str(len(done))))
		out=Color().reader(string)+Repeat
		print(out)
	def Remove(self,arg,a):
		point=lambda t:Color().reader(f'[$LYELLOW]Loading... [$LRED][ [$GREEN]{t}[$YELLOW]%[$GREEN]100 [$LRED]]')
		print(point('0'),end='\r')
		i=0
		rem=list(self.all[arg])
		for x in a:
			os.remove(x[0])
			rem.remove(x)
			print(point(str(i/len(a)*100).split('.')[0]),end='\r')
			i+=1
		print(point('100'),end='\r')
		self.all[arg]=rem
		self.DoneSearch[arg]=[[],True,[]]
		print(' '*len(Color().del_colors(point('100'))),end='\r')
		print((Color().reader("[$LYELLOW]DelRepeat:[$LGREEN] ")+str(i)))
		
	def do__maim(self,arg):
		return True
NumFile().cmdloop()
	
	
