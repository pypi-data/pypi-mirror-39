'''
socket extention api.
builds on the standart socket library and adds more advance functions,
making it easier to make more varied sockets.
'''
try:
	#from sug_sock import *
	from sug_sock import *
except:
	print('[-] sug_sock library not found')
	exit(1)
'''
try:
	import os
except:
	print('[-] os library not found')
	exit(1)
'''
def debug():
	print('debug function: ')
	print(dir('sug_sock')) 
	#print(dir(os))
	#print(os.getcwd())

def meme():
	print("nice")
def test():
	a = sugsock()
	print(str(a.ip))
	print(str(a.port))
	print(str(a.proc))
	print(str(a.type))
	a.addAttribute('name','boop')
	print(str(a.getAttribute('name')))
	a.changeAttribute('name' , 'doop')
	print(str(a.getAttribute('name')))
#debug()
test()