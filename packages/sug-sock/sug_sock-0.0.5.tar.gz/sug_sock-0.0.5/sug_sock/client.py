#from Tkinter import *

#add screen lock

#ok so igotta come up with an api for the client messages
import socket
import string
from threading import *
#def login():

VIEW = ''
Host = 'localhost'
def connect():
	sock = socket.socket()
	sock.connect((Host,1034))
	#sock.connect(("79.182.12.79",1034))
	#sock.connect(("10.0.0.2",1034))
	return sock
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
def viewData(sock):
	data = raw_input("what user do you want to view?: ")
	dataFile = open("clientData.txt" , 'r')
	for line in dataFile:
		if line.split("  /  ")[2] == data:
				message = "private message from "+data+": "+line.split("  /  ")[4] 
				print (message)
		if line.split("  /  ")[3] == data:
				message = "private message from "+line.split("  /  ")[2]+" at: "+data+": "+line.split("  /  ")[4] 
				print (message)
	return
		
def communicate(sock):
	try:
		while True:
			data = raw_input("")
			if data == 'view':#this could go wrong very easly
				viewData(sock)
			elif data == 'file':
				sendFile(sock)
			else:	
				sock.send(data)
			if data == "logout":
				print("logging out")
				return
	except:
		print("simething went wrong on the communucate function")
def handleRequest(val,sock):
	kind = val.split("  /  ")[0]
	what = val.split("  /  ")[1]
	if what == 'reply':
		type = val.split("  /  ")[2]
		if type == 'getAvailable':
			srv = val.split('  /  ')[3]
			prv = val.split('  /  ')[4]
			print('users available: ' +prv)
			print('servers available: ' +srv)
	if what == 'password':
		password = raw_input("enter password: ")
		sock.send(password)
	if what == 'username':
		username = raw_input("enter username: ")
		sock.send(username)
	if what == 'login ok':
		t = Thread(target = communicate, args = (sock,))
		t.start()
	if what == 'Error':
		error = val.split('  /  ')[2]
		print (error)
	return
def recivePrivate(val):
	kind,senderType,sender,type,data = val.split("  /  ")
	if type == "txt":
		log = open("clientData.txt",'a')
		header = val#make sure the message dosnt have a new line charachter in it
		print("appending")
		log.write(val+"  /  \n")
		log.close()
	if type == "file":
		t = Thread(target = handleFile,args = (val,))
		t.start()	
	return
def handleFile(val):
	kind,senderType,sender,type,data = val.split("  /  ")
	if VIEW == sender:
			print("incoming file from: "+sender+" " +data+". accept download?")
			answer = raw_input("yes to accept download, anything else to discard: ")
			if answer == 'yes':
				print ('downloading')
				download()
				
			else:
				print ('discarded')
	else:
		print('file from: ' + sender+ ' discarded.')
	return
def download():
	try:
		transferPort = socket.socket()
		transferPort.connect((Host,transferPort))
		RecivedFile= transferPort.recv(length)
		savedFile = ("downloadedfile" ,'w+')
		savedFile.write(RecivedFile)
		savedFile.close()
		transferPort.send("req  /  done")
		transferPort.close()
	except:
		print('download failed')
	return
def sendFile(sock):
	whom = raw_input("to: ")
	filename = raw_input("file name: ")
	msg = ('msg  /  '+whom+'  /  file  /  '+filename)
	sock.send(msg)
	answer = sock.recv(1024)
	if(answer.split("  /  ")[0] == 'req':
		if(answer.split("  /  ")[1] != 'yes':
			print('sending denied')
			return
	else:
		print('sending failed')
		return
	try:
		file = open(filename,'rb')
		sock.send("req  /  openFileSocket")
		val = sock.recv(1024)
		if(val.split("  /  ")[0] == 'req'):
			if(val.split("  /  ")[1] == 'transferPort'):
				Fport = val.split("  /  ")[2]
				length = val.split("  /  ")[3]
		transferPort = socket.socket()
		transferPort.connect((Host,transferPort))
	except:
		print('sending failed')
	return
	
def handleMessage(val):
	senderType = val.split("  /  ")[1]
	if(senderType == 'private'):
		recivePrivate(val)
	elif(senderType == 'server'):
		reciveServer(val)
	
def checkInfo(sock):
	while True:
		val =sock.recv(1024)
		kind = val.split("  /  ")[0]
		print val
		if kind == 'req':
			handleRequest(val,sock)
		if kind == 'msg':
			handleMessage(val)
		#print(val)
		if val == "logout":
			return
	
def main():
	#gui()
	sock = connect()
	#t = Thread(target = checkInfo , args = (sock,))
	#t.start()
	checkInfo(sock)
	#checkInfo()
	#communicate(sock)
	sock.close()
	return
	

if __name__ == "__main__":
	main()
	
	
	
	