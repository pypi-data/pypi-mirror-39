import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
def add_handler(task, importance):
	f = open(dir_path+'/todo.txt', 'a')
	f.write('\n'+task+'-'+importance)
	f.close()
	sys.exit()
