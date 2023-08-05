#FIX DE THING
#might switch for asyncio if threads are not fitting

#use tcp for fail safe transport of info.
#use udp for fast transport of info.
#tcp - text, info, file sender.
#udp - voice chat, video chat.
#-----using "select" stuff for now, might switch for more purpose buit libarys or threads.
#using threads becuse select and asyncio are for python 3
import string
from threading import * 
#from socket import *
#import selectors
import socket
#def login():
IP = "0.0.0.0"
PORT = 1034
Ports = [1035,1036,1037,1038,1039]
#store logged in users
clients = []
#store an array of arrays, first object in array is the server name, next objects are usernames allowed in the server
servers=[]
#suppose to stop the program, dosnt work, fix it
STOP = True
######
#so this is my server api for now:
# A  /  B  /  C  /  D
#A - can be either 'private' , 'server' , 'req' depending on who the message is for or if this is a request.
#B - the reciver, who the message is intedent to.
#C - the type, is it a txt, data, or other kind of info being transsferred.
#D - the data itself.
class Server:
	def __init__(self,name,id = 0):
		self.allowed = []
		self.name = name
		temp = self.pickId()
		if temp == False:
			print("oh fuck")
		else:
			self.id = temp
		
	def addAllow(self,us):
		self.allowed.append(us)
		return
	def pickId(self):
		file = open("serverInfo.txt",'r')
		for line in file:
			nick = line.split("  :  ")[0]
			if nick == self.name:
				number = line.split("  :  ")[1]
				file.close()
				return number
		file.close()
		return False
	def sendData(self,val,whom,type):
		if type == "txt":
			for user in self.allowed:
				print("sending to: " + str(user.name)+" val: "+val)
				t = Thread(target = self.sendsTxt,args = (val,user,whom,))
				t.start()
		return
	def sendsTxt(self,val,user,whom):
		print(user.name +"   "+str(user.sock))
		if user.sock!=0:
			print("sending")		
			print(b"msg  /  server  /  "+ whom.name+b"  /  "+self.name +b"  /  txt  /  "+str(val))
			user.sock.send(b"msg  /  server  /  "+ whom.name+b"  /  "+self.name +b"  /  txt  /  "+str(val))
		return		
			
#user object
class User:
	def __init__(self,name,password,id,sock = 0):
		self.name = name
		self.password = password
		self.id = id
		self.sock = sock
		self.friends = []
		
	#set this user connection port
	#if sock = 0 user is offline
	def setSock(self,sock):
		self.sock = sock
		return
	def removeSock(self):
		self.sock = 0
		return
	def addFriend(self,friend):
		self.friends.append(friend)
		return
		
def gui():
	#gui
	root = Tk()
	#gui settings
	root.title("SugCord")
	root.geometry("200x100")
	app = Frame(root)
	app.grid()
	#text
	button1 = Button(app,text = "push me")
	button1.grid()
	button2 = Button(app)
	button2.grid()
	button2.configure(text = "weh")
	#start gui
	root.mainloop()
#check if the user name and password are correct with the users.txt
def validUser(Aname,Apassword):
	#get the users file
	us = open("users.txt",'r')
	try:
		#for every line in the file
		for line in us:
			#if the name = the name given
			name = line.split("  :  ")[0]
			if name == Aname:
				#if the password = the password given
				password = line.split("  :  ")[1]
				if password == Apassword:
					us.close()
					print("noice")
					#return the id
					return line.split("  :  ")[2]
	except:
		print("[-] username or password are wrong")
	#us.sock.close()
	return False
	
#make dis
def createUser():
	#maybe later
	return

#verifies the user logging in and puts the sock obj in the correct user obj
def addUser(sock):
	ok = False
	while not(ok):
		#request the user info
		sock.send(b"req  /  username")
		name = str(sock.recv(1024))
		#if got some sort of commend, do it.
		if name == 'create new user':
			createUser()
		if name == 'exit':
			us.sock.send("logout")
			us.sock.close()
			return
		#request the user password
		sock.send(b"req  /  password")
		password = str(sock.recv(1024))
		#check if its valid with the users.txt
		valid = validUser(name,password)
		#if its ok
		if valid!=False:
			#get the correct user id
			id = valid
			ok = True
	#get the correct user object by id
	us = getUser(id)
	if us == False:
		return
	#set this user sock as this current connection sock
	us.setSock(sock)
	#send succes report
	us.sock.send(b"req  /  login ok")
	#start the thread
	startThread(us)
	return

#sets up server listen socket
def setServer():
	lsock = socket.socket()
	lsock.bind((IP,PORT))
	return lsock
def testLoop(sock):
	while True:
		print 'nice'
		print(sock.recv(1024))
		sock.send('test')
#waits for new connections from clients	
def waitConn(sock):
	print(str(sock.getsockname()))
	while STOP:
		sock.listen(1)
		(cSock,cAdd) = sock.accept()
		print("connection from: "+str(cAdd))
		#testLoop(cSock)
		t = Thread(target = addUser,args = (cSock,))
		t.start()
	removeClients()#####change this
	return
#removes socket from clients array###################################
def removeClients():
	for us in clients:
		logout(us)
	return
#handle client requests	
def handleClients(us):
	lsock = us.sock
	while STOP:
		#if got data :
		val = lsock.recv(1024)
		if val != "logout":
			handleData(val,us)
		else:
			logout(us)
			return
	
#logs the user out.
def logout(us):
	try:
		if us.sock != 0:
			print (us.name +" is logging out.")
			#send the user the logout confirmation
			us.sock.send(b"logout")
			#close the socket
			us.sock.close()
			us.removeSock()
		else:
			print(us.name +" is already logged out.")
	except:
		print("error logging out")
	return
#starts the thread
def startThread(us):
	lsock = us.sock
	#this was suppose the send the log of everything that happened while the user was not online
	#file = open("log.txt",'r')
	#for line in file:
	#	lsock.send(line)
	#file.close()
	t= Thread(target = handleClients,args = (us,))
	t.start()
#checks what type of data it is and what to do with it.
#ok so data should come like this
#serv OR user  /  server OR user  /  type  /  val 
def handleData(val,us):
	mode = val.split("  /  ")[0]
	if mode == 'req':
		handleRequest(val,us)
		return
	mode,whom,type,data = val.split("  /  ")
	if type == "txt":
		#checkSend(whom,data,mode,us)
		sendText(whom,data,mode,us)
	if type == 'file':
		sendFile(val,us)
	return
def sendFile(val,us):
	User= ''
	for user in clients:
		#if the user in the clients array got the same name as the person the data is sent to.
		if user.name == whom:
			#send the data to that user.
			user.sock.send(b"msg  /  private  /  "+ us.name+b"  /  file  /  "+data)
			User = user
	try:
		mode,whom,type,data = val.split("  /  ")
		sock = us.sock
		sock.send(User.recive(1024))
		val = sock.recv(1024)
		if val.split("  /  ")[0] == 'req':
			if val.split("  /  ")[1] == 'openFileSocket':
				lsock = socket.socket()
				prt = Ports[0]
				ports.remove(prt)
				lsock.bind((IP,prt))
				msg = 'req  /  transferPort  /  '+str(prt))
				sock.send(msg)
				User.send(msg)
				lsock.recive()
			
			
	
	
#sends text to either servers or clients########################might change it from name based to id based after ill get the client interface done.
#whom - the reciver of info, data - the data to be sent , arrayPick - is it a server or a private client, us - the sender user object.
def sendText(whom,data,arrayPick,us):
	#if its for a private user
	if arrayPick =="private":
		#go over the clients array
		#checkSend(whom,data,arrayPick,us)
		#return
		if checkSend(whom,data,arrayPick,us):
			for user in clients:
				#if the user in the clients array got the same name as the person the data is sent to.
				if user.name == whom:
					#send the data to that user.
					#print("private message from " + us.name+": "+data)
					#user.sock.send(b"private message from " + us.name+b": "+data)
					user.sock.send(b"msg  /  private  /  "+ us.name+b"  /  txt  /  "+data)
					return
			#if the user was not found
			us.sock.send(b"[-] ERROR. User "+ whom+b" not found")
			return
	#if its for a server
	elif arrayPick == "server":
		#go over the servers array
		for serv in servers:
			#if the server in the servers array got the same name as the server the data is sent to.
			if serv.name == whom:
				#call the server send data function.
				serv.sendData(data,us,'txt')
				return
		#if the server was not found.
		us.sock.send(b"[-] ERROR. Server "+ whom+b" not found")
		return
def checkSend(whom , data , arrayPick , us):
	if arrayPick =="private":
		reciver = getUserByName(whom)
		for id in us.friends:
			if id = reciver.id:
				return True
		return False	
	return
#checks for admin input
def adminLoop():
	global STOP
	while(STOP):
		a = raw_input()
		if a == 'stop':
			STOP = False
			print("stop: " + str(STOP))
			removeClients()
		if a == 'users':
			arr = []
			for us in clients:
				if us.sock!= 0:
					arr.append(us.name)
			print (str(len(arr))+" "+str(arr))
	return
def handleRequest(val,us):
	mode,request = val.split("  /  ")
	if request.split(" ")[0] == 'getLog':
		print("boop")#################get the log of the user specified after the : and send it back
	if request.split(" ")[0] == 'getList':
		srv,prv = getAvailable(us)
		msg = 'req  /  reply  /  getAvailable  /  '+str(srv)+'  /  '+str(prv)
		us.sock.send(msg)
	return
def getAvailable(us):
	private = []
	serv = []
	friends = us.friends
	for friend in friends:
		cl = getUser(friend)
		clname = cl.name
		private.append(clname)
	for server in servers:
		for user in server.allowed:
			if user.id == us.id:
				serv.append(server.name)
	return serv,private
		
def sendLoop():
	logFile = open("log.txt",'r+')
	while(STOP):
		#if ya got something in the buffer
		if len(BUFFER)>0:####################################33gotta change alot here to make it send only to appropriate clients
			#go over all the clients
			for x in range(0,len(clients)):#might wanna switch things up here to fix end case probloms
				sk = clients[x].sock
				#send everything in buffer
				for y in range(0,len(BUFFER)):
					sk.send(BUFFER[y])		
			#remove objects from buffer
			for x in range(0,len(BUFFER)):
				logFile.write(BUFFER[x]+"\n")
				BUFFER.remove(BUFFER[x])
	for x in range(0,len(clients)):
		sk = clients[x]
		sk.send("sToPPP")
	file.close()
	return
#goes over the clients list and returns the user object with the correct id. returns False if none found.
def getUserByName(name):
	for x in range(0,len(clients)):
		us = clients[x]
		Name = us.name
		if Name == name:
			return us
		return False
def getUser(ID):
	#for x in the range of all clients
	for x in range(0,len(clients)):
		us = clients[x]
		id = us.id
		if id==ID:
			return us
	return False
	
#creates the users objects and stores them into the clients array.	
def getUSERS():
	#open the users info file
	file = open("users.txt",'r')
	#for every line in the users file
	for line in file:
		#put the data into the correct varables.
		name = line.split("  :  ")[0]
		password = line.split("  :  ")[1]
		id = line.split("  :  ")[2]
		friends = line.split("  :  ")[3]
		#create a user object
		us = User(name,password,id)
		#add friends
		for x in range(1,len(friends.split("  ,  "))+1):
			friend = line.split('  ,  ')[x]
			if x == len(friends.split("  ,  ")):
				friend = friend.split('\n')[0]
			us.addFriend(friend)
		#add the user object to the clients array.
		clients.append(us)
	return
#creates the servers objects and stores them into the servers array.	
def getServers():
	#open server info file
	file = open("serverInfo.txt",'r')
	#for every line in the server file
	for line in file:
		#put the data from the line into fitting varables.
		name = line.split("  :  ")[0]
		id = line.split("  :  ")[1]
		#create Server object
		se = Server(name,id)
		#go other all the users allowed on this specific server
		for x in range(1,len(line.split("  ,  "))):
			#put the allowed user id in a varable
			usr = line.split("  ,  ")[x]
			#get the correct user object from the clients array.
			us = getUser(usr)
			#if it exists
			if us!=False:
				#add the user object to the server allowed array.
				se.addAllow(us)
		#add the server to the servers list
		servers.append(se)
	return
#main
def main():
	#set up server
	sock = setServer()
	#start checking for admin orders
	s = Thread(target = adminLoop)
	s.start()
	#get users and put em into the client list
	getUSERS()
	#get servers and put em in the buffer
	getServers()
	#start looking for clients
	t = Thread(target = waitConn,args = (sock,))
	t.start()
	return

	

if __name__ == "__main__":
	main()
	