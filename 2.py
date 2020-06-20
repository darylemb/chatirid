from tkinter import *
from tkinter import scrolledtext as st
from tkinter import Menu
from tkinter import messagebox
from socket import *
from threading import *

HOST = '127.0.0.1'
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((HOST,4014))
clientes = []
grupos_conectado=[]
mensaje_global = {}
def estructura(origen=None,tipo=None,group=None,destiny ="multicast", message = None, socket_cliente = None,lista_clientes=None,clientes_destinos=None):
	diccionario_envio={"origin":origen,"type":tipo,"group":group,"destiny":destiny,"message":message,"lista_clientes":lista_clientes,"clientes_destinos":clientes_destinos}	
	if diccionario_envio["group"]!= None or diccionario_envio["group"]!='':
		print("ENVIO: ",diccionario_envio)
		clientSocket.send(bytes(str(diccionario_envio),"utf-8"))

def listen_permanente():
	global mensaje_global
	while True:
		mensaje = eval(clientSocket.recv(2048).decode("utf8"))
		print(mensaje_global)
		if mensaje["origin"] == "servidor":
			for i in mensaje["lista_clientes"]:
				if i not in clientes:
					clientes.append(i)
			continue
		elif mensaje["group"]!=None:
			if mensaje["group"] not in grupos_conectado:
				interface(mensaje["group"])
			mensaje_global = mensaje
			
def mensaje_recibir(grupo_propio,messages):
	global mensaje_global
	while True:
		mensaje = mensaje_global
		if any(mensaje):
			if mensaje["group"] == grupo_propio:
				messages.insert(INSERT, '%s' % mensaje["origin"]+": "+mensaje["message"]+"\n")
				mensaje_global = {}
def desarrolladores():
	messagebox.showinfo("Desarolladores","Iridian Fernández\nKarla López\nAngel Mejía")

def grupo():
	seleccion= Toplevel()
	lista_clientes = Listbox(seleccion,selectmode=EXTENDED)
	seleccion.title("Creación de grupo")
	seleccion.minsize(300,300)
	Label(seleccion,text="Escribe el nombre del nuevo grupo").pack()
	input_group = StringVar() #Nombre del nuevo grupo
	input_group_field=Entry(seleccion,text = input_group)
	input_group_field.pack()
	for i in clientes:
		lista_clientes.insert(clientes.index(i),i)
	lista_clientes.pack()
	
	def enviar_grupo():
		clientes_buscados = list(lista_clientes.curselection())#Lista de los clientes con el grupo a formar
		clientes_seleccionados=[]
		for i in range(len(clientes_buscados)):
			clientes_seleccionados.append(clientes[i])
		print(clientes_seleccionados)
		print("")
		input_get_group=input_group_field.get() #Variable que contiene el nombre del grupo
		grupos_conectado.append(input_get_group)
		estructura(destiny="multicast",group = input_get_group,clientes_destinos=clientes_seleccionados,message="Te has unido a un grupo")
		print(input_get_group)
		print(clientes_seleccionados)
		interface(input_get_group)
	boton = Button(seleccion,text="Crear grupo",command=enviar_grupo)
	boton.pack()

def interface(nombre_de_grupo):
	global nombre
	grupos_conectado.append(nombre_de_grupo)
	print(grupos_conectado)
	window = Tk()
	window.title("Chat: "+str(nombre_de_grupo)+" Del Usuario: "+str(nombre))
	menubar = Menu(window)
	window.config(menu = menubar)
	menubar.add_command(label = "Crear grupo",command = grupo)
	menubar.add_command(label = "Desarrolladores",command = desarrolladores)
	messages = st.ScrolledText(window)
	#messages.pack()
	hilo = Thread(target=mensaje_recibir,args=(nombre_de_grupo,messages))
	hilo.start()
	messages.pack()
	input_user = StringVar()
	input_field = Entry(window, text=input_user)
	input_field.pack(side=TOP, fill=X)

	def Enter_pressed(event):
		input_get = input_field.get()
		if input_get !='':
			estructura(origen=nombre,message=input_get,group=nombre_de_grupo)
		#messages.insert(INSERT, '%s' % nombre+": "+input_get)
		input_user.set('')
		return "break"

	frame = Frame(window)  # , width=300, height=300)
	input_field.bind("<Return>", Enter_pressed)
	frame.pack()
	window.mainloop()

print("ingresa tu nombre de usuario")
nombre = str(input())
thread_listen = Thread(target = listen_permanente)
thread_listen.start()
estructura(nombre) #discovery
interface("global")
