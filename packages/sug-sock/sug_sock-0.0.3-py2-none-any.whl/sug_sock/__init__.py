'''
socket extention api.
builds on the standart socket library and adds more advance functions,
making it easier to make more varied sockets.
'''
try:
	from .sug_sock import *
except:
	print('[-] sug_sock library not found')
try:
	import os
except:
	print('[-] os library not found')

def debug():
	print('debug function: ')
	print(dir(sug_sock)) 
	print(dir(os))
	print(os.getcwd())

def meme():
	print("nice")