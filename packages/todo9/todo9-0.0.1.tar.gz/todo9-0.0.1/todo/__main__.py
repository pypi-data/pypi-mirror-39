import argparse
import sys
from .add import add_handler
from .delete import delete_handler
from .edit import edit_handler
import os 

def modify(flag):
	f = open(dir_path+'/todo.txt', 'r')
	previousContent = f.read()
	f.close()
	previousContent = previousContent.split('\n')
	previousContent[0] = flag
	previousContent = '\n'.join(previousContent)
	f = open(dir_path+'/todo.txt', 'w')
	f.write(previousContent)
	f.close()
def maingl():

	dir_path = os.path.dirname(os.path.realpath(__file__))
	parser = argparse.ArgumentParser(description='Simple todo CLI')
	parser.add_argument('-en','--enable', help="Enable the todo", action="store_true")
	parser.add_argument('-db','--disable', help="Disable the todo", action="store_true")
	parser.add_argument('-n','--newtask', help="Add new task")
	parser.add_argument('-d','--delete', type=int,help="Delete a task")
	parser.add_argument('-e','--edit', type=int,help="Edit a task")
	args = parser.parse_args()


	#check for enabled flag, create todo.txt if not created
	try:
		f = open(dir_path+'/todo.txt', 'r')
	except:
		f = open(dir_path+'/todo.txt', 'w')
		f.write('e')
		f.close()
		f = open(dir_path+'/todo.txt', 'w')

	flag = f.read().split('\n')[0]


	if args.enable and args.disable:
		print ("Pass any one flag!")
		sys.exit()

	if args.enable:
		modify('e')
		sys.exit()

	if args.disable:
		modify('d')
		sys.exit()

	if(flag is 'd'):
		sys.exit()


	if args.newtask:
		priority = input("Priority on a scale of 1-3?")
		add_handler(args.newtask, priority)
		sys.exit()

	if args.delete:
		delete_handler(args.delete)
		sys.exit()

	if args.edit:
		edit_handler(args.edit)
		sys.exit()

	"""
	WAS USED TO say status-(e/d)
	previousContent[0] = previousContent[0].split('-')
		previousContent[0][1] = 'd'
	"""

	f = open(dir_path+'/todo.txt', 'r')
	content = f.read().split('\n')
	count = len(content)
	if count == 1:
		print("todo list is empty!")
	i = 1
	while i<= count-1:
		line = content[i].split('-')
		priority = int(line.pop())
		line = '-'.join(line)
		print ( "\033[1;36;40m"+'*'*priority +"\033[0m"+str(i)+') '+ line)
		i+=1

	f.close()
	"""content = f.read().split('\n')
	for line in content:
		print line
		"""