import sys

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
def delete_handler(serial):
	f = open(dir_path+'/todo.txt', 'r')
	previousContent = f.read()
	f.close()
	previousContent = previousContent.split('\n')
	del previousContent[serial]
	previousContent = '\n'.join(previousContent)
	f = open(dir_path+'/todo.txt', 'w')
	f.write(previousContent)
	f.close()