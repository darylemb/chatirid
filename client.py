from tkinter import *
from tkinter import scrolledtext as st
from tkinter import Menu
from tkinter import messagebox
from socket import *
from threading import *

HOST = '127.0.0.1'
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((HOST,4002))
clientes = []

def desarrolladores():
	messagebox.showinfo("Desarolladores","Iridian Fernández\nKarla López\nAngel Mejía")

def estructura(origen=None,tipo=None,destino = None, mensaje = None):
	diccionario_envio={"origin":origen,"type":tipo,"destiny":destino,"message":mensaje}	
	print("ENVIO: ",diccionario_envio)
	clientSocket.send(bytes(str(diccionario_envio)+'\n',"utf-8"))
		
def mensaje_recibir(grupo_propio,messages):
	while True:
		mensaje = eval(clientSocket.recv(2048).decode("utf8"))
		#print(mensaje)
		if mensaje["origin"] == "servidor":
			#clientes = mensaje["lista_clientes"]
			for i in mensaje["lista_clientes"]:
				if i not in clientes:
					clientes.append(i)
			#print(clientes)
		else:
			messages.insert(INSERT, '%s' % mensaje["origin"]+": "+mensaje["message"]+"\n")

def enviar_a_grupo():
	global nombre
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
		print(clientes_buscados)
		clientes_seleccionados=[]
		for i in clientes_buscados:
			clientes_seleccionados.append(clientes[i]) #agrega a la lista clientes_seleccionados los clientes seleccionados en la interfaz
		print(clientes_seleccionados)
		input_get_group=input_group_field.get() #Variable que contiene el nombre del grupo
		estructura(origen=nombre, tipo="multicast", destino=clientes_seleccionados,mensaje=input_get_group)
		seleccion.destroy()
	boton = Button(seleccion,text="Enviar mensaje",command=enviar_grupo)
	boton.pack()
	
def interface(nombre_de_grupo):
	global nombre
	window = Tk()
	window.title("Chat: "+str(nombre_de_grupo)+" Del Usuario: "+str(nombre))
	menubar = Menu(window)
	window.config(menu = menubar)
	menubar.add_command(label = "Enviar a usuarios especificos",command = enviar_a_grupo)
	menubar.add_command(label = "Desarrolladores",command = desarrolladores)
	messages = st.ScrolledText(window)
	hilo = Thread(target=mensaje_recibir,args=(nombre_de_grupo,messages))
	hilo.start()
	messages.pack()
	input_user = StringVar()
	input_field = Entry(window, text=input_user)
	input_field.pack(side=TOP, fill=X)

	def Enter_pressed(event):
		input_get = input_field.get()
		if input_get !='':
			estructura(origen=nombre,tipo = "broadcast", mensaje=input_get)
		input_user.set('')
		return "break"

	frame = Frame(window)
	input_field.bind("<Return>", Enter_pressed)
	frame.pack()
	window.mainloop()

print("ingresa tu nombre de usuario")
nombre = str(input())
estructura(nombre,"broadcast") #discovery
interface("global")
