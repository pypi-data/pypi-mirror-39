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

in addition to that sug sock will have an attributes module
this attributes will be able to hold an attribut name and data.
so if i want to store the socket or peer name i could store them on the socket attributes
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
try:
	from Attribute import *
except:
	print("[-] Attribute module not found")
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
			self.attributes = []
			self.ip = ip
			self.port = port
			self.proc = proc
			self.type = type
		except Exception as e:
			print("[-] an error has occured in creating the sugsock. recheck values")
			print(str(e))
		return		
	def bind(self,ip,port):
		try:
			self.sock.bind(ip,port)
			self.ip = ip
			self.port = port
		except Exception as e:
			print("[-] an error has occured in binding the sugsock. recheck values")
			print(str(e))
		return
	def addAttribute(self,name,attribute):
		try:
			a = attr(name,attribute)
			self.attributes.append(a)
		except:
			print("[-] attribute addition has failled.")
		return
	def getAttribute(self,name):
		try:
			for x in range(0,len(self.attributes)):
				if self.attributes[x].name == name:
					val = self.attributes[x].value
					return val
			print("[-] getAttribute -  attribute to be returned not found.")
			return None
		except:
			print("[-] get attribute procces has failled")
			return None
	def changeAttribute(self,name,attribute):
		try:
			for x in range(0,len(self.attributes)):
				if self.attributes[x].name == name:
					self.attributes[x].value = attribute
					return 
			print("[-] changeAttribute - attribute to be changed not found.")
			return
		except:
			print("[-] change attribute procces has failled")
			return None