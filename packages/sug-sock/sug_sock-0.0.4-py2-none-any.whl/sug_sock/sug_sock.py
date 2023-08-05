'''
socket extention api.
builds on the standart socket library and adds more advance functions,
making it easier to make more varied sockets.

so the sugsock would contain a regular socket object, with easy functions
stuff in a sock:
	port
	ip
	protocol
	ip type
	
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
	# so a call for a sugsock object goes like sugsock(ip,port,protocol,type), enter 0 or nothing for defult
	def __init__(self,ip = 0 , port = 0 , proc = 'tcp',type = 'v4'):
		try:
			if proc == 'tcp':
				if type == 'v4':
					self.sock = socket.socket()
				elif type == 'v6':
					self.sock = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
			if proc == 'udp':
				if type == 'v4':
					self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				elif type == 'v6':
					self.sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
			if (ip !=0)and(port != 0):
				self.sock.bind(ip,port)
		except e:
			print("[-] an error has occured in creating the sugsock. recheck values")
			print(str(e))
		return
		
	def bind(self,ip,port):
		try:
			self.sock.bind(ip,port)
		except e:
			print("[-] an error has occured in binding the sugsock. recheck values")
			print(str(e))
		return