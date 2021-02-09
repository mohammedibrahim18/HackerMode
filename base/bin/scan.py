from N4Tools.Design import Text,Square
import requests as req
import socket,os,time,sys
from threading import Thread
import signal
class Main:
	def __init__(self):
		try:
			self.Sq = Square()
			self.Sq.color = '[$LCYAN]'
			self.T = Text()
			self.eip = req.get('https://api.ipify.org').text
			self.work = True
			s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			self.iip = s.getsockname()[0]
			s.close()
			self.open_ports1 = []
			self.open_ports1.sort()
			self.open_ports2 = []
			self.open_ports2.sort()
			self.ports=set(list(range(1,6535)) + [8080,7547,6666,8888,7777,5555])
			self.mw=os.get_terminal_size().columns
		except socket.gaierror:
			exit()
		except socket.error:
			print('\033[1;31m[-] Check your internet connection..!\033[0m')
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
	def scan(self,ip,a):
		myl=self.open_ports1 if a=='eip' else self.open_ports2
		for port in self.ports:
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(0.1)
			if s.connect_ex((ip,port))==0:
				myl.append(port)
		self.work = False
	def serv(self,p):
		try:
			x=socket.getservbyport(p)
		except socket.error:
			x='Unknown'
		return x
	def bscan(self):
		ban1,ban2 = ["•","••","•••","••••"],["/","-","\\","|"]
		while self.work:
			for x in range(4):
				if not self.work:
					break
				sys.stdout.write("\033[1;37m\r[\033[1;31m%s\033[1;37m]\033[1;32m Scaning\033[1;33m %s "%(ban2[x%4],ban1[x%4]))
				time.sleep(0.1)
				sys.stdout.flush()
	def display(self,i,a):
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

	def run(self):
		p1=Thread(target=self.scan,args=(self.eip,'eip'))
		p1.start()
		p1.join()
		p2=Thread(target=self.scan,args=(self.iip,'iip'))
		p2.start()
		p2.join()
		s1=Thread(target=self.display,args=(self.eip,'eip'))
		s2=Thread(target=self.display,args=(self.iip,'iip'))
		s1.start();s1.join()
		s2.start();s2.join()
	def main(self):
		zm2=Thread(target=self.run,args=())
		zm2.start()
		zm1=Thread(target=self.bscan,args=())
		zm1.start()
if __name__ == '__main__':
	myrun = Main()
	myrun.main()
