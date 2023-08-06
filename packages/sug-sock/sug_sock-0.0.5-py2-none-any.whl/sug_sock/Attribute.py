'''
Attribute class.
'''
	
class attr:
	# so a call for a sugsock object goes like sugsock(ip,port,protocol,type), enter 0 or nothing for defult
	def __init__(self,name,value):
		self.name = name
		self.value = value