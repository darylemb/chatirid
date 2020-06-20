from socket import *
from threading import *
import time

clients = {}
grupos = {} 
hostSocket = socket(AF_INET,SOCK_STREAM)
hostIP = '127.0.0.1'
portNumber = 4014
hostSocket.bind((hostIP,portNumber))
hostSocket.listen(15)
print("Waiting for connection....")

def estructura(origen=None,tipo=None,group=None,destiny =None, message = None, socket_cliente = None,lista_clientes=clients):
	diccionario_envio={"origin":origen,"type":tipo,"group":group,"destiny":destiny,"message":message,"lista_clientes":list(clients.keys())}
	socket_cliente.send(bytes(str(diccionario_envio),"utf-8"))

def clientThread(clientSocket,clientAddress):
	while True:
		
		#clientes_cada_segundo(clientSocket)
		recibido = eval(clientSocket.recv(2048).decode("utf-8"))#Eval convierte string a cualquier tipo de estructura que detecte en el string
		if recibido["group"]== None or recibido["group"]=='':
			continue
		print(recibido)
	#if recibido["type"] == "conectar":
	#	if recibido["origin"] not in list(clients.keys()):
	#		clients[recibido["origin"]]=clientSocket
		if recibido["type"] == "desconectar":
			#print(list(clients.keys())[list(clients.values()).index(clientSocket)], " se ha desconectado")
			del clients[list(clients.keys())[list(clients.values()).index(clientSocket)]]
			for i in list(clients.values()):
				estructura(origen=recibido["origin"],message=str(list(clients.keys())[list(clients.values()).index(clientSocket)])+" se ha desconectado",socket_cliente=i,group="global")
			return False
		if recibido["destiny"] == "broadcast":
			for i in list(clients.values()):
				estructura(origen=recibido["origin"],message=recibido["message"],group=recibido["group"],socket_cliente=i)
			continue
		if recibido["destiny"] == "multicast":
			grupo(recibido)
def clientes_cada_segundo(socket):#Envia cada segundo a los clientes la lista de clientes conectados
	while True:
		estructura(origen="servidor",socket_cliente=socket)
		time.sleep(1)
		continue

def grupo(recibido):
	if recibido["group"] == "global":#Broadcast
		for i in list(clients.values()):
			#print(i)
			estructura(origen=recibido["origin"],group=recibido["group"],message=recibido["message"],socket_cliente=i)
			print(estructura(origen=recibido["origin"],group=recibido["group"],message=recibido["message"],socket_cliente=i))
	elif recibido["group"] in grupos:
		for i in grupos[recibido["group"]]:#Multicasts, si está el grupo, envía el mensaje a los miembros del grupo
			estructura(origen=recibido["origin"],message=recibido["message"],socket_cliente=i,group=recibido["group"])
			print(estructura(origen=recibido["origin"],message=recibido["message"],socket_cliente=i,group=recibido["group"]))
	else:
		grupos[recibido["group"]]=[]#Multicast, crea el grupo si no existe
		for i in recibido["clientes_destinos"]:
			grupos[recibido["group"]].append(clients[i])
			estructura(origen=recibido["origin"],message=recibido["message"],socket_cliente=clients.get(i),group=recibido["group"])
			print(estructura(origen=recibido["origin"],message=recibido["message"],socket_cliente=clients.get(i),group=recibido["group"]))

while True:
	clientSocket, clientAddress = hostSocket.accept()
	clients[eval(clientSocket.recv(2048).decode("utf-8"))["origin"]]=clientSocket#Discovery
	#print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
	thread = Thread(target=clientThread,args=(clientSocket,clientAddress))
	thread_clientes= Thread(target=clientes_cada_segundo,args=(clientSocket,))
	thread.start()
	thread_clientes.start()
