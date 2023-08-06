def modify(flag):
	f = open('/home/shivashis/Documents/lifeLine/projPer/todo/todo.txt', 'r')
	previousContent = f.read()
	f.close()
	previousContent = previousContent.split('\n')
	previousContent[0] = flag
	previousContent = '\n'.join(previousContent)
	f = open('/home/shivashis/Documents/lifeLine/projPer/todo/todo.txt', 'w')
	f.write(previousContent)
	f.close()