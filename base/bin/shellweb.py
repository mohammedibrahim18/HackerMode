from N4Tools.Design import Color,ThreadAnimation
from bs4 import BeautifulSoup as Soup
from pygments import highlight
from pygments.lexers import HtmlLexer,JsonLexer
from pygments.formatters import TerminalFormatter
import requests,cmd,json,re

import sys, os
sys.path.append(os.path.abspath(__file__).split('/bin')[0])
from shell import BaseShell

url=input(Color().reader('[$LYELLOW]URL[$GREEN]~[$LRED]/[$LWIHTE]$ [$WIHTE]'))

@ThreadAnimation()
def GET(Thread):
	req=requests.get(url)
	Thread.kill=True
	return req
run=False
try:HTML=GET()#open('/sdcard/soup.py','r').read()
except Exception as e:print('\r'+str(e));exit()


#header={k.replace('-','_'):v for k,v in HTML.headers.items()}
soup=Soup(HTML.text,'html.parser')
class HtmlCmd(BaseShell):
	ToolName = "shellweb.[$LPINK]Html"
	AllDag=['ins', 'frame', 'area', 'option', 'wbr', 'b', 'code', 'head', 'audio', 'main', 'optgroup', 'dialog', 'big', 'acronym', 'hr', 'dir', 'data', 'div', 'h5', 'h4', 'h6', 'h1', 'h3', 'h2', 'span', 'picture', 'output', 'link', 'video', 'pagh', 'section', 'map', 'em', 'small', 'nav', 's', 'object', 'noscript', 'cite', 'html', 'ul', 'mark', 'button', 'title', 'figure', 'ruby', 'font', 'br', 'aside', 'rp', 'ol', 'rt', 'progress', 'time', 'details', 'dfn', 'applet', 'summary', 'svg', 'samp', 'meta', 'p', 'li', 'track', 'script', 'style', 'table', 'del', 'figcaption', 'dd', 'basefont', 'colgroup', 'dl', 'strong', 'dt', 'input', 'base', 'tr', 'tt', 'footer', 'canvas', 'noframes', 'select', 'circle', 'td', 'embed', 'template', 'th', 'caption', 'bdi', 'bdo', 'i', 'a', 'thead', 'abbr', 'u', 'nobr', 'q', 'meter', 'stop', 'datalist', 'radialgradient', 'form', 'frameset', 'body', 'pre', 'col', 'blockquote', 'address', 'heada', 'label', 'param', 'tbody', 'img', 'sub', 'fieldset', 'article', 'sup', 'header', 'kbd', 'var', 'textarea', 'center', 'legend', 'strike', 'iframe', 'tfoot', 'source']
	doc_header='Example Comments:'
	for x in AllDag:
		exec(f"""\
		\rdef do_{x}(self,arg):
		self.MainRunDag(arg,'{x}')
		\rdef help_{x}(self):
		print('example:{x} --class="Name" ')
		print('example:{x} --id="Name" -a')
		print('example:{x} --id="Name" -{x}.id')
		print('example:{x} --style="{{backgrund:red}}" -a.href')
		print('example:{x}')
		print('example:{x}.class or {x}.text or....')
		print('example:{x} -a')
		print('example:{x} -a.href')
		""")

	def MainRunDag(self,arg,name):
		r=re.findall('^[\w]*.[\w]*$',arg)
		if len(r)==1 and  len(r[0])==len(arg): #tagattr link.href
			Com=(f'{name}{arg}').strip()
		else:Com=(f"{name} {arg}").strip()
		r=re.findall('^[\w]*[\s]*-[\w]*$',arg)
		if len(r)==1 and  len(r[0])==len(arg): #tagattr link -a
			Com=(f'{name} {arg}').strip()
		TC=(self.SortData(Com)) #TypeComment
		@ThreadAnimation()
		def GT(Thread,N):
			a=(self.TypeComment(N))
			a=Soup(a,'html.parser').prettify()
			a=self.Lexer('\n'.join([x for x in a.split('\n') if x]))
			Thread.kill=True
			return a
		a=(GT(TC))
		print(a[:-1] if a.endswith('\n') else a)
	def Lexer(self,text):
		a=highlight(text,HtmlLexer(), TerminalFormatter())      
		return('\r'+a)
	
	def TypeComment(self,TC): #Type Comment...
		out=''
		isnotnone=lambda t:str(t)+'\n' if t!=None else ''
		if TC!=None:
			if TC[-1]=='if': #do if
				for x in soup.find_all(TC[0],TC[1]):
					out+=str(x)+'\n'
			elif TC[-1]=='ifto': #do ifto
				for x in soup.find_all(TC[0],TC[1]):
					s=Soup(f'{x}','html.parser')
					for c in s.find_all(TC[2]):
						out+=str(c)+'\n'
			elif TC[-1]=='iftoatr': #do iftoatr
					for x in soup.find_all(TC[0],TC[1]):
						s=Soup(f'{x}','html.parser')
						for c in s.find_all(TC[2][0]):
							if TC[2][-1]=='text':out+=str(c.text)+'\n'
							else:
								u=c.get(TC[2][-1])
								if u!=None:out+=str(u)+'\n'
			elif TC[-1]=='tagall': #do tagall
				for x in soup.find_all(TC[0]):
					out+=str(x)+'\n'
			elif TC[-1]=='tagattr': #do tagattr
				for x in soup.find_all(TC[0]):
					if TC[1]=='text':out+=str(x.text)+'\n'
					else:
						u=x.get(TC[1])
						if u:out+=isnotnone(u)
			elif TC[-1]=='tagtoall': #to tagtoall
				for x in soup.find_all(TC[0]):
					s=Soup(f'{x}','html.parser')
					for c in s.find_all(TC[1]):
						out+=str(c)+'\n'
			elif TC[-1]=='tagtoatrall': #do tagtoatrall
					for x in soup.find_all(TC[0]):
						s=Soup(f'{x}','html.parser')
						for c in s.find_all(TC[1][0]):
							if TC[1][1]=='text':out+=str(c.text)+'\n'
							else:
								u=c.get(TC[1][1])
								if u:out+=str(u)+'\n'
		return(out)
							
					
	def SortData(self,arg):
		arg=arg.replace("'",'"').strip()
		n=lambda a:[x for x in a if x.strip()]
		r=re.findall('^[\w\s]*--[\w\s]*=[\s]*"[\w\S\s]*"$',arg)

		if len(r)==1:
			if len(r[0])==len(arg): ##if div -id="help"
				tag=(re.findall('^[\w\s]*',arg)[0].strip())
				k=(re.findall('--[\w]*',arg)[0][2:])
				v=(re.findall('"[\w\s\S]*"',arg)[0][1:-1])
				return ([tag,{k:v},'if'])
		else:
			r=re.findall('^[\w\s]*--[\w\s]*=[\s]*"[\w\S\s]*"[\s]*-[\w]*$',arg)

			if len(r)==1 and  len(r[0])==len(arg): ##ifto div -id="help" -a
				tag=(re.findall('^[\w\s]*',arg)[0].strip())
				k=(re.findall('--[\w]*',arg)[0][2:])
				v=(re.findall('"[\w\S\s]*"',arg)[0][1:-1])
				totag=(re.findall('-[\w)]*$',arg)[0][1:])
				return ([tag,{k:v},totag,'ifto'])
			else:
				r=re.findall('^[\w\s]*--[\w\s]*=[\s]*"[\w\S\s]*"[\s]*-[\w]*.[\w]*$',arg)

				if len(r)==1 and  len(r[0])==len(arg): # iftoatr div -id="help" -a.text
					tag=(re.findall('^[\w\s]*',arg)[0].strip())
					k=(re.findall('--[\w]*',arg)[0][2:])
					v=(re.findall('"[\w\S\s]*"',arg)[0][1:-1])
					totag=(re.findall('-[\w]*.',arg)[-1][1:-1])
					attrtag=(re.findall('.[\w]*$',arg)[0][1:])
					return ([tag,{k:v},[totag,attrtag],'iftoatr'])
				else:
					r=re.findall('^[\w]*$',arg)
					if len(r)==1 and  len(r[0])==len(arg): #tagll div
						tag=re.findall('^[\w]*$',arg)[0]
						return([tag,'tagall'])
					else:
						r=re.findall('^[\w]*.[\w]*$',arg)
						if len(r)==1 and  len(r[0])==len(arg): #tagattr link.href
							tag=(re.findall('^[\w]*.',arg)[0][:-1])
							attr=(re.findall('.[\w]*$',arg)[0][1:])
							return ([tag,attr,'tagattr'])
						else:
							r=re.findall('^[\w]*[\s]*-[\w]*$',arg)
	
							if len(r)==1 and  len(r[0])==len(arg): #tagtoall div -link
								tag=(re.findall('^[\w]*',arg)[0])
								totag=(re.findall('-[\w]*$',arg)[0][1:])
								return ([tag,totag,'tagtoall'])
							else:
								r=re.findall('^[\w]*[\s]*-[\w]*.[\w]*$',arg)
	
								if len(r)==1 and  len(r[0])==len(arg): #tagtoatrall div -link.href
									tag=(re.findall('^[\w]*',arg)[0])
									totag=(re.findall('-[\w]*.',arg)[0][1:-1])
									attrtotag=(re.findall('.[\w]*$',arg)[0][1:])
									return ([tag,[totag,attrtotag],'tagtoatrall'])

	def default(self, line): #not in Code
		self.stdout.write('Not Tag: "<%s>" in Code\n'%line)

	def do_back(self,arg):
		return True

class InfoCmd(BaseShell):
	ToolName = "shellweb.[$LGREEN]Info"
	header={k.replace('-','_'):v for k,v in HTML.headers.items()}
	AllCommentInfo=['encoding','reason','request','status_code','url','ok','links','history','is_permanent_redirect','is_redirect','apparent_encoding','cookies','elapsed']
	for x in AllCommentInfo:
		exec(f'''\
		\rdef do_{x}(self,arg):
		@ThreadAnimation()
		def get(Thread):
			a=(HTML.{x})
			Thread.kill=True
			return('\\r'+str(a)+' '*7)
		print(get())
		\rdef help_{x}(self):
		print('example:{x}')
		''')
	def do_headers(self,arg):###
		if not arg.strip():self.Lexer(self.header)
		else:self.Lexer(self.getheader(arg))
	def getheader(self,arg):
		out={}
		for x in arg.split(' '):
			if x in self.header.keys():
				out[x]=self.header[x]
		return out
			
	def Lexer(self,text):###
		@ThreadAnimation()
		def lexer(Thread):
			a=highlight(json.dumps(text,indent=3),JsonLexer(), TerminalFormatter())
			Thread.kill=True
			return('\r'+a)
		print(lexer())
	def complete_headers(self,arg,*args):###
		all=[k for k in self.header.keys()]
		if not arg:return all
		else:return [k+' ' for k in all if k.startswith(arg)]
	def do_back(self,arg):
		return True

class LinkCmd(BaseShell):
	ToolName = "shellweb.[$LCYAN]Link"
	all=set(list(map((lambda t:t[0]),re.findall('"((http|ftp)s?://.*?)"', HTML.text))))
	file=set([x for x in all if re.findall('[\w]*\.[\w]*$',x)])
	ends=set([x[x.rfind('.'):] for x in file])
	for x in ends:
		exec(f'''\
		\rdef do_{x[1:]}(self,arg):
		for x in self.file:
			if x.endswith('{x}'):print(x)
		''')
	def do_rest(self,arg):
		print('\n'.join([x for x in self.all if  not x in self.file]))
	def do_back(self,arg):
		return True

class MainCmd(BaseShell):
	ToolName = "shellweb"
	def do_html(self,arg):
		HtmlCmd().cmdloop()
	def do_info(self,arg):
		InfoCmd().cmdloop()
	def do_links(self,arg):
		LinkCmd().cmdloop()
	def do_main(self,arg):
		return True

MainCmd().cmdloop()
		
