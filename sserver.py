from socket import *
from threading import *
from time import *
#struct ={"origin":"","type":"","group":"","destiny":"","message":"","clients":"",}

clients = {}
grupos = {} #diccionario que contiene por llave el nombre de los grupos y por valor un array con los clientsocket asociados al grupo.
hostSocket = socket(AF_INET,SOCK_STREAM)
hostIP = '127.0.0.1'
portNumber = 4000
hostSocket.bind((hostIP,portNumber))
hostSocket.listen(15)
print("Waiting for connection....")

def estructura(origen=None,tipo=None,group=None,destiny =None, message = None, socket_cliente = None,lista_clientes=None,clientes_conectados=clients):

    diccionario_envio={"origin":origen,"type":tipo,"group":group,"destiny":destiny,"message":message,"lista_clientes":lista_clientes}
    socket_cliente.send(bytes(str(diccionario_envio),"utf-8"))

def clientThread(clientSocket,clientAddress):
    while True:
        estructura(origen="servidor",message="Bienvenido al chat", socket_cliente=clientSocket)
        recibido = eval(clientSocket.recv(1024).decode("utf-8"))
        if recibido["type"] == "desconectar":
            print(list(clients.keys())[list(clients.values()).index(clientSocket)], " se ha desconectado")
            del clients[list(clients.keys())[list(clients.values()).index(clientSocket)]]
            for i in list(clients.values()):
                estructura(message=str(list(clients.keys())[list(clients.values()).index(clientSocket)])+" se ha desconectado",socket_cliente=i)
            return False
        if recibido["type"] == "broadcast":
            for i in list(clients.values()):
                estructura(message=recibido["message"],socket_cliente=i)
        if recibido["type"]== "multicast":
            grupo(recibido)

def grupo(recibido):
    if recibido["group"] in grupos:
        for i in grupos[recibido["group"]]:
            estructura(message=recibido["message"],socket_cliente=i,group=recibido["group"])
    else:
        grupos[recibido["group"]]=[]
        for i in recibido["lista_clientes"]:
            grupos[recibido["group"]].append(clients[i])
            estructura(message=recibido["message"],socket_cliente=clients[i],group=recibido["group"])



while True:
    clientSocket, clientAddress = hostSocket.accept()
    clients[clientSocket.recv(1024).decode("utf-8")]=clientSocket
    print(clients)
    print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
    print("Longitud ",len(clients))
    thread = Thread(target=clientThread,args=(clientSocket,clientAddress))
    thread.start()