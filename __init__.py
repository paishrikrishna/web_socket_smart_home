#outside libs
import socket
import netifaces as ni

# my libs
from coffee_maker import coffee_maker


class server:
	def __init__(self):
		ni.ifaddresses('wlp2s0')
		self.ip = ni.ifaddresses('wlp2s0')[ni.AF_INET][0]['addr']
		self.listensocket = socket.socket()
		self.Port = 8000
		self.maxConnections = 999
		self.IP = socket.gethostname() #Gets Hostname Of Current Macheine
		self.listensocket.bind(('',self.Port))
		#Opens Server
		self.listensocket.listen(self.maxConnections)
		print("Server started at " + self.IP + " on port " + str(self.Port))
		print("Your IP Address IS "+self.ip)

	
	def listen_from_clients(self):
		while True:
		    (self.clientsocket, self.address) = self.listensocket.accept()
		    self.msg = self.clientsocket.recv(1024).decode() #Receives Message
		    print(self.address)
		    print(self.msg)
		    self.clientsocket.send(b"Hi")


class client:
	def __init__(self,host):
		self.HOST = host  # The server's hostname or IP address
		self.PORT = 80        # The port used by the server

	def listen_from_server(self,step):		
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.connect((self.HOST, self.PORT))
				s.sendall(step.encode())
				self.data = s.recv(1024)

			#print('Received',(self.data.decode()))
			return self.data.decode()
		except:
			return "p"	 

	def status_from_server(self):		
		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.connect((self.HOST, self.PORT))
				#s.sendall(step.encode())
				#self.data = s.recv(1024)

			#print('Received',(self.data.decode()))
			return s.recv(1024).decode()
		except:
			pass
		return "false"	 


class task_creater:
	def __init__(self,task):
		self.access = "free"
		self.device=""
		# create task and make a manager and status
		self.task = task
		if task in coffee_maker.recipie.keys():
			self.task_manager = coffee_maker.steps
			self.task_status = ['p','p','p','p','p','p','p','p']
			#print(self.task_manager)
		elif task == "shaker":
			self.task_manager = coffee_maker.work['shaker']
			self.task_status = ['p','p']
		elif task == "dispensor":
			self.task_manager = coffee_maker.work['dispensor']
			self.task_status = ['p','p','p','p']

	def decide_device(self):
		# decide if the task is for dispensor or shaker
		if self.task_manager[0] in coffee_maker.work["dispensor"]:
			self.host = client('192.168.43.8')
			if self.device != "dispensor":
				self.device="dispensor"
				self.access="free"
		elif self.task_manager[0] in coffee_maker.work["shaker"]:
			self.host = client('192.168.43.128')
			if self.device!="shaker":
				self.device="shaker"
				self.access="free"
		print(self.device)
		#return self.host

	def send_step(self,step):
		if(self.host.listen_from_server("status")==self.access and self.host.listen_from_server(step) == step):
			self.access = "busy"
			self.task_status[self.task_manager.index(step)]='o'

	def on_complete(self):
		del self.task_manager[0]
		del self.task_status[0]

	def decide_step(self):
		if self.task_status[0] == 'p':
			return True
		else:
			return False




if __name__ == '__main__':
	objects=[]

	inp = input("Enter Task ")
	objects.append(task_creater(inp))
	
	while len(objects[0].task_manager) > 0:
		#print("Processing")
		print(objects[0].task_manager)
		objects[0].decide_device()
		if(objects[0].decide_step()):
			objects[0].send_step(objects[0].task_manager[0])

		elif bool(objects[0].host.status_from_server()):
			objects[0].on_complete()
			

		#print(objects[0].decide_device())

	#	print(objects[0].task_manager)
	#	print(objects[0].task_status)
		
	#	print(objects[0].task)

	#	server().listen_from_clients()
		


			