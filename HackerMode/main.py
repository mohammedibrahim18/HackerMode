from base import system
import pathlib

current_dir = pathlib.Path(__file__).parent
current_file = pathlib.Path(__file__)

print(system.get_platform())
print (current_file)
print (current_dir)

#print ( os.path.dirname(__file__) )
#print ( os.getcwd() )