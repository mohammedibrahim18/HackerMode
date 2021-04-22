import os

if os.path.isfile("dart_main.exe"):
	os.system("./dart_main.exe")
else:
	os.system("python3 python_main.py")