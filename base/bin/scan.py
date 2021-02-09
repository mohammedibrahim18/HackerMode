from N4Tools.Design import Text,Square,ThreadAnimation,Animation,AnimationTools
import requests as req
import socket,os,time,sys
from threading import Thread as u
A = Animation()
class MA:
	def CustomAnimation(min=0,max=5639,**kwargs):
                yield A.Prograsse(min=min,max=max,prograsse=['│','\033[1;36m█','\033[1;34m▒','│'],text='Scanning',**kwargs)[0]+f'\033[1;37m({round(min*100/max,1)}/100.0) '

class Main(MA):
	ips=[]
	def __init__(self):
		try:
			self.Sq = Square()
			self.Sq.color = '[$LCYAN]'
			self.T = Text()
			eip = req.get('https://api.ipify.org').text
			self.ips.append(eip+'+eip')
			s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			iip = s.getsockname()[0]
			self.ips.append(iip+'+iip')
			self.open_ports1 = []
			self.open_ports1.sort()
			self.open_ports2 = []
			self.open_ports2.sort()
			self.ports=set(list(range(1,6535)) + [8080,7547,6666,8888,7777])
			self.mw=os.get_terminal_size().columns
		except socket.gaierror:
			exit()
		except socket.error:
			print('\033[1;31m[-] Check your internet connection..!\033[0m')
			exit()
		except KeyboardInterrupt:
			exit()
		b='''
	   _____		   _--_
	  / ___/_________ _____	 .'    '.
	  \__ \/ ___/ __ `/ __ \ |\033[1;30m((0)) \033[1;35m|
	 ___/ / /__/ /_/ / / / / |      |
	/____/\___/\__,_/_/ /_/   '.  .'
			           |""|
                        '''
		print('\033[0;32m',b,'\033[0m')


	def serv(self,p):
		try:
			x=socket.getservbyport(p)
		except socket.error:
			x='Unknown'
		return x

	def display(self,i):
		i,a=i.split('+')
		myl=self.open_ports1 if a=='eip' else self.open_ports2
		fu = '''
    port    Service    Status
[$LCYAN]═══════════════════════════════'''
		Ip = f'\n\n[$LYELLOW][{i}]'
		if not len(myl):
                                fu+='\n[$LRED]      No Service Is Runing\b'
		else:
			for p in myl:
				fu+=f'\n[$LBLUE]   {str(p).ljust(4)}   {self.serv(p).rjust(8)}    {"Open".rjust(7)} '
		box_info=self.Sq.base(fu[1:-1])
		output = self.T.CentreAlignPro([Ip,box_info])
		for x in output.split('\n'):
			print("\t"+x)

	@ThreadAnimation(Animation=MA.CustomAnimation)
	def scan(Thread,self):
		p=0

		for ip in self.ips:
			i,a=ip.split('+')
			myl=self.open_ports1 if a=='eip' else self.open_ports2
			for port in self.ports:
				s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(0.1)
				if s.connect_ex((i,port))==0:
					myl.append(port)
				Thread.set_kwargs(min=p+1, max=6539*2)
				p+=1
		Thread.kill()

	def d(self):
		for ip in self.ips:
			self.display(ip)

	def runs(self):
		p1=u(target=self.scan,args=())
		p1.start()
		p1.join()
		s1=u(target=self.d,args=())
		s1.start()

if __name__ == '__main__':
	Main().runs()
