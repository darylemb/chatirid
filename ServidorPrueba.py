
from socket import *
from threading import *
import tkinter as tk
import pickle

clients = set()
client_List= [0,0,0,0,0,0]
global Chatgrupal
Chatgrupal=[]
listagrupo=[]
dirClients=[]
#msg= pickle.dumps(client_List)

#Server
def clientThread(clientSocket, clientAddress):
	while True:
		message = clientSocket.recv(1024).decode("utf-8")
		if message=="El cliente creo un grupo":
			#While True:
			for i in range(6):
				listagrupo.append(clientSocket.recv(1024).decode("utf-8"))
				print(listagrupo[i])
				valor=int(listagrupo[i])
				print("valor: ",valor)
				if valor==1:
					if i<=len(dirClients):
						Chatgrupal.append(dirClients[i])
					#print(clients.next())
		print(clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message)
		for client in clients:
			print("Losclientesson: ",clients)
			if client is not clientSocket:
				client.send((clientAddress[0] + ":" +" says: "+ message).encode("utf-8"))
		if not message:
			clients.remove(clientSocket)
			print(clientAddress[0] + ":" + str(clientAddress[1]) +" disconnected")
			break
	clientSocket.close()
    
    

hostSocket = socket(AF_INET, SOCK_STREAM)
#hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)

hostIp = "127.0.0.1"
portNumber = 4000
hostSocket.bind((hostIp, portNumber))
hostSocket.listen(10)
#hostSocket.listen()
print ("Waiting for connection...")

##################################***************************************************##########################################
def grupo(client_List):
	for i in range(len(clients)):
		valor=client_List[i]
		if valor==1:
			Chatgrupal.append(clients.next())
			print(clients.next())


#Tenemos que limpiar el diccionario            
##################################***************************************************##########################################

while True:
	clientSocket, clientAddress = hostSocket.accept()
	clients.add(clientSocket)
	client_List.append((clientSocket,clientAddress))
	print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
	ent=int(clientAddress[1])
	dirClients.append(ent)
	#clientSocket.send(bytes(msg))
	print("Longitud ",len(clients))
	for i in range(len(dirClients)):
		print("cliente",i,": ",dirClients)
	thread = Thread(target=clientThread, args=(clientSocket, clientAddress, ))
	thread.start()
