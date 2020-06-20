from socket import *
from threading import *
import time

clients = {}
hostSocket = socket(AF_INET,SOCK_STREAM)
hostIP = '127.0.0.1'
portNumber = 4002
hostSocket.bind((hostIP,portNumber))
hostSocket.listen(15)
print("Waiting for connection....")

def estructura(origen=None,tipo=None,mensaje = None,destino = None, socket_cliente = None):
	diccionario_envio={"type":tipo,"destiny":destino,"message":mensaje,"lista_clientes":list(clients.keys()),"origin":origen}
	socket_cliente.send(bytes(str(diccionario_envio),"utf-8"))

def clientThread(clientSocket,clientAddress):
	while True:
		recibido = eval(clientSocket.recv(2048).decode("utf-8"))
		print(recibido)
		if recibido["type"] == "desconectar":
			del clients[list(clients.keys())[list(clients.values()).index(clientSocket)]]
			for i in list(clients.values()):
				estructura(origen=recibido["origin"],mensaje=str(list(clients.keys())[list(clients.values()).index(clientSocket)])+" se ha desconectado",socket_cliente=i,group="global")
			return False
		
		elif recibido["type"] == "broadcast":
			for i in list(clients.values()):
				estructura(origen=recibido["origin"],mensaje=recibido["message"],socket_cliente=i)
			continue
		elif recibido["type"] == "multicast":
			for i in recibido["destiny"]:
				estructura(origen = recibido["origin"],mensaje = recibido["message"],socket_cliente = clients[i])

def clientes_cada_segundo(socket):#Envia cada segundo a los clientes la lista de clientes conectados
	#time.sleep(5)
	while True:
		estructura(origen="servidor",socket_cliente=socket)
		time.sleep(2)
		continue

while True:
	clientSocket, clientAddress = hostSocket.accept()
	clients[eval(clientSocket.recv(2048).decode("utf-8"))["origin"]]=clientSocket#Discovery
	print(clients)
	thread = Thread(target=clientThread,args=(clientSocket,clientAddress))
	thread_clientes= Thread(target=clientes_cada_segundo,args=(clientSocket,))
	thread.start()
	thread_clientes.start()
