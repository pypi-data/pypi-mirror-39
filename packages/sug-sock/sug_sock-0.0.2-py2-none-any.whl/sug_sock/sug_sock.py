'''
socket extention api.
builds on the standart socket library and adds more advance functions,
making it easier to make more varied sockets.

so the sugsock would contain a regular socket object, with easy functions
stuff in a sock:
	port
	ip
	protocol
	
'''
try:
	import socket
except:
	print("[-] socket library not found")
	exit(1)
try:
    import threading
except:
	print("[-] threading library not found")
	exit(1)
class sugsock:
	def __init__(self):
		self.sock = socket.socket()
		