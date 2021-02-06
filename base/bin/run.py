import os

class runfile:
	def __init__(self,path):
		self.path=path
		self.args=['.py',".sh",'.c','.php']
	def isfile(self):
		for x in self.args:
			if self.path.endswith(x):return True
	def run(self):
		if self.isfile():os.system(f'python {self.path}')
		
