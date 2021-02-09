from N4Tools.Design import Color,ThreadAnimation
from bs4 import BeautifulSoup as Soup
from subprocess import Popen,PIPE
from pygments import highlight
from pygments.lexers import HtmlLexer,JsonLexer
from pygments.formatters import TerminalFormatter
import requests,os,cmd,json

url=input(Color().reader('[$LYELLOW]URL[$GREEN]~[$LRED]/[$LWIHTE]$ [$WIHTE]'))
PROMPT=lambda url:Color().reader(f'\
[$LYELLOW]╭[$LRED][[$LBLUE]URL[$YELLOW]@[$LWIHTE]{url}[$LRED]] \n\
[$LYELLOW]╰>>>[$WIHTE]')
@ThreadAnimation()
def GET(Thread):
	req=requests.get(url)
	Thread.kill=True
	return req
run=False
try:HTML=GET()#open('/sdcard/soup.py','r').read()
except Exception as e:print('\r'+str(e));exit()


header={k.replace('-','_'):v for k,v in HTML.headers.items()}
soup=Soup(HTML.text,'html.parser')
class BaseCmd(cmd.Cmd):
	prompt=PROMPT(url)
	Image=['.jpeg','.bmp','.gif','.png','.jpg','.svg']
	URL=['.com','.edu','.gov','.int','.mil','.net','.org','.co','.info','.tv']
	Allbody=['html','body','title','div','img','link','form','p','h1','h2','h3','h4','h5','h6','input','nobr','label','center','ul','u','b','td','li','style','span','noscript','a','head']
	def do_show(self,arg):
		print (soup.prettify())
	def do__link(self,arg):
		arg=arg.strip().split(' ')
		out=self.Getlink(arg,'link').split('\n')
		out+=[*self.Getlink(arg,'a').split('\n')]
		print('\n'.join(set(out)))
	def Getlink(self,arg,name):
		out=[]
		for x in soup.find_all(name):
			a=(x.get('href'))
			if ('css' in arg) and a.endswith(f'.css'):out.append(url+a if a.startswith('/') else a)
			if ('json' in arg) and a.endswith('.json'):out.append(url+a if a.startswith('/') else a)
			if ('image' in arg):
				for _ in self.Image:
					if a.endswith(_):out.append(a)
			if ('url' in arg):
				f=self.GetUrl(a)
				if f:out.append(f)
		return('\n'.join((set(out))))
	def GetUrl(self,a):
		if a.startswith('http'):
			isurl=True
			for _ in self.Image+['.css','.js','.json']:
				if a.endswith(_):isurl=False
			if isurl:return a#out.append(a)
		else:
			for _ in self.URL:
				if a.endswith(_) or a.endswith('/'):return(url+a if a.startswith('/') else a)#out.append(url+a if a.startswith('/') else a)
			
		
		
	def complete__link(self,arg,*args):
		all=['css ','json ','url ','image ']
		return self.Com(all,arg)
	def Com(self,all,arg):
		if not arg:a=all
		else:a=[_ for _ in all if _.startswith(arg)]
		return a
	def do__script(self,arg):
		arg=arg.strip().split(' ')
		print(self.GetScript(arg))
	def GetScript(self,arg):
		out=[]
		for x in soup.find_all('script'):
			a=x.get('data-src')
			if a==None:a=x.get('src')
			if a!=None:
				if ('js' in arg) and a.endswith('.js'):out.append(a)
		return '\n'.join(sorted(set(out)))
	def Lexer(self,text,mode='html'):
		@ThreadAnimation()
		def lexer(Thread):
			a=highlight(text,(HtmlLexer() if mode=='html' else JsonLexer()), TerminalFormatter())
			Thread.END=' '
			Thread.kill=True
			return('\r'+a)
		print(lexer())
	def complete__script(self,arg,*args):
		all=['js']
		return self.Com(all,arg)
	def do__meta(self,arg):
		arg=arg.strip().split(' ')
		print(self.GetMeta(arg))
	def do__allurl(self,arg):
		a=[]
		for x in ['image','url']:a.append(self.GetMeta(x))
		for x in ['css ','json ','url ','image ']:
			a.append(self.Getlink(x,'link'))
			a.append(self.Getlink(x,'a'))
		a.append(self.GetScript('js'))
		print('\n'.join(x for x in a if x.strip()))
	def GetMeta(self,arg):
		out=[]
		for x in soup.find_all('meta'):
			a=x.get('content')
			if a!=None:
				if ('image' in arg):
					for _ in self.Image:
						if a.endswith(_):out.append(a)
				if ('url' in arg):
					f=self.GetUrl(a)
					if f:out.append(f)
					
		return '\n'.join(sorted(set(out)))
	def complete__meta(self,arg,*args):
		all=['image ','url ']
		return self.Com(all,arg)

	def Getattr(self,arg,name):
		out=[]
		for x in soup.find_all(name):
			for _ in arg:
				a=_.split('.')
				for __ in x.find_all(a[0]):
					if len(a)>1:
						for f in a[1:]:
							if f=='text':out.append(eval(f'__.{f}'))
							else:
								p=__.get(f)
								if p:out.append(''.join(p))
					else:
						p=__.prettify()
						if not p in out:out.append(p)#[:p.rfind('\n')] if p.endswith('\n') else p)
		return '\n'.join(out)
	def do_seva(self,arg):
		with open(arg,'w')as f:f.write(soup.prettify())
	def do_EOF(self,arg):
		return True
	for x in Allbody:
		exec(f'''\
		\rdef do_{x}(self,arg):
		arg=arg.strip().split(' ')
		if arg==['']:self.Lexer(self.AllAttr('{x}'))
		else:self.Lexer(self.Getattr(arg,'{x}'))
		\rdef complete_{x}(self,arg,*args):
		all=self.Allbody
		return self.Com(all,arg)''')
	def AllAttr(self,arg):
		out=[]
		for x in soup.find_all(''.join(arg)):
			x=x.prettify()
			out.append(x)#[:x.rfind('\n')] if x.endswith('\n') else x)
		return '\n'.join(out)
	def do_headers(self,arg):
		arg=arg.strip().split(' ')
		if ''.join(arg).strip():(self.Lexer(json.dumps(self.GetHeader(arg),indent=3),mode='json'))
		else:self.Lexer(json.dumps(header,indent=3),mode='json')
	def GetHeader(self,arg):
		out={}
		for x in arg:
			if x in list(header.keys()):out[x]=header[x]
		return out
	def complete_headers(self,arg,*args):
		all=list(header.keys())
		return self.Com(all,arg)

	for x in dir(HTML):
		if not (x.startswith('__')):
			if x not in ['headers','close','raise_for_status','iter_content','iter_lines','json','content']:
				exec(f'''\
				\rdef do_{x}(self,arg):
				print(HTML.{x})
				''')
				
BaseCmd().cmdloop()
		
