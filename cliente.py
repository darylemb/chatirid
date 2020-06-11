import tkinter
from tkinter import messagebox
from tkinter import filedialog
from numpy import array
import tkinter as tk
from socket import *
import threading
from threading import *
import pickle


#global selec
#selec=tk.IntVar()
#-----------------------------SOCKET------------------------------------
HOST = "127.0.0.1"
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST, 4000))

##################################***************************************************##########################################


def Send_Lista_Clientes(clientList):
	
	clave ="El cliente creo un grupo"
    #clavehbreak="fin"
	clientSocket.send(clave.encode("utf-8"))
	
	#msg=pickle.dumps(clientList)
	#clientSocket.send(bytes(msg,"utf8"))
	#for i in range(6):
	clientSocket.send(bytes(str(clientList),"utf-8"))    
	#clientSocket.send(clavehbreak
    
###################Verificar agregar al cliente
	
##################################***************************************************##########################################

def recibe():
	while True:
		recmsj = clientSocket.recv(1024).decode("utf-8")
		print(recmsj)
		interfaz.config(state="normal")
		interfaz.insert(tk.END,"\n"+"PonemosID:"+recmsj)
		interfaz.config(state="disabled")
		
			
#-----------------------------VENTANA GRAFICA---------------------------
#ventana de chat        
def grupo():
	grupo=messagebox.askquestion("Crear chat","Realmente quiere hace un nuevo grupo que al final muchas veces no te contestan o ni lo usan :(")
	if grupo=="yes":
		global chat
		chat = tk.Toplevel()
		chat.title("Nuevo grupo")
		chat.geometry("400x400")
		chat.resizable(0,0)
		chat.configure(background="dark slate gray")
		mensaje=tk.Label(chat,text="Eliga con quienes tener un grupo :(",bg="dark slate gray",fg="white")
		mensaje.pack(padx=11,pady=11,ipadx=3,ipady=3)
		global c1,c2,c3,c4,c5,c6
		c1=tk.IntVar()
		c2=tk.IntVar()
		c3=tk.IntVar()
		c4=tk.IntVar()
		c5=tk.IntVar()
		c6=tk.IntVar()
		cliente1=tk.Checkbutton(chat,variable=c1,text="C1",onvalue=1,offvalue=0).pack()#str(clientAdress[0])
		#if usuario2==1: Verificando si el usuario 2 existe
		cliente2=tk.Checkbutton(chat,variable=c2,text="C2",onvalue=1,offvalue=0).pack()
		cliente3=tk.Checkbutton(chat,variable=c3,text="C3",onvalue=1,offvalue=0).pack()
		cliente4=tk.Checkbutton(chat,variable=c4,text="C4",onvalue=1,offvalue=0).pack()
		cliente5=tk.Checkbutton(chat,variable=c5,text="C5",onvalue=1,offvalue=0).pack()
		cliente6=tk.Checkbutton(chat,variable=c6,text="C6",onvalue=1,offvalue=0).pack()
	
		
		boton = tk.Button(chat, text='Aceptar',command=Lista).pack()#(padx=21,pady=11,ipadx=3,ipady=3)
		#chat.destroy()
	#mylabel=tk.Label(chat,text=selec.get()).pack
		#print("El nuevo estado es: ",estado)
		#chat.mainloop()
		#chat.transient(master=ventana)
		#chat.grab_set()#posible a borrar
		#ventana.wait_window(chat)#posible a borrar
		#print("El nuevo, nuevo estado es: ",estado)
   

		
#aqui poner los if para pasar al diccionario ademas de poder pasar direccion y "reconocer las IP"
		#cliente1=tk.Checkbutton(chat,state=ACTIVE,variable=select).pack()#str(clientAdress[0])

def Lista():
	#mylabel=tk.Label(chat,text=estado).pack()
	#print("El estado es:",estado)
 
##################################***************************************************##########################################
#Añadimos todas las elecciones a la lista
##################################***************************************************##########################################
	clientList = str(c1.get())+str(c2.get())+str(c3.get())+str(c4.get())+str(c5.get())+str(c6.get())
	print(clientList)
	Send_Lista_Clientes(clientList)
	chat.destroy()
	
		#añadimos el diccionario al arreglo
	
	#client1.append()
	#le pasa una lista de clientes y s es "1" 
	#Añadir los clientes dependiendo de la dirección de memoria
	"""aux=grupo().estado
	if aux==1:
		print("Se añadio cliente")
	else:
		print("se quito")"""
	
	
	

#def Agregar():
	#Añadimos los valores que se seleccionaron, 
	#Cerramos la ventana que se creó 
	
		

#ventana de desarrolladores
def desarrolladores():
	messagebox.showinfo("Desarolladores","*Iridian Fernández\n*Karla López\n*Angel Mejía")

#ventana de salir
def salir():
	valor=messagebox.askquestion("Salir","¿Esta seguro de salir y perder la mejor conversación de su vida?")
	if valor=="yes":
		ventana.destroy()

#Función para seleccionar archivo
"""def SelArchivo():
	global result
	result=filedialog.askopenfilename()#Dirección
	print(result)
	file=open(result,'rb')
	file_data=file.read(1024)
	clientSocket.send(file_data)
	#interfaz.insert(tk.END,"\n"+"Tú:"+msj)
	#clientSocket.send(msj.encode("utf-8"))
	#interfaz.config(state="disabled")
	#cajamensaje.delete(0, 'end')

def RecibirArchivo():
	interfaz.config(state="normal")
	interfaz.insert(tk.END,"\n"+"PonemosID: envió imagen")
	interfaz.config(state="disabled")
	filename="Archivo1"
	file=open(filename,'wb')
	#totalRecv=len(data)
	file_data=clientSocket.recv(1024)
	file.write(file_data)
	file.close()
	
"""  
	

#función para el boton
def enviar():
	interfaz.config(state="normal")
	msj=cajamensaje.get()
	if msj != '':
		interfaz.insert(tk.END,"\n"+"Tú:"+msj)
		clientSocket.send(msj.encode("utf-8"))
		interfaz.config(state="disabled")
		cajamensaje.delete(0, 'end')


#ventana principal
ventana = tk.Tk()
frame=tk.Frame(ventana)
frame.pack()
ventana.title("SecretodeAmorXXX")
ventana.resizable(0,0)
frame.config(bg="black")
#ventana.iconbitmap(r'C:/Users/Elitebook/Desktop/fuego.ico')

#barra opciones
barraopc=tk.Menu(frame)
ventana.config(menu=barraopc,width=1,height=1)
opciones=tk.Menu(barraopc,tearoff=0)
opciones.add_command(label="Nuevo grupo", command=grupo)
opciones.add_separator()
###########opciones.add_command(label="Añadir Archivo",command=SelArchivo)
opciones.add_command(label="Desarolladores...", command=desarrolladores)
opciones.add_command(label="Salir", command=salir)
barraopc.add_cascade(label="Opciones", menu=opciones)

#interfaz interna mensajes 
interfaz=tk.Text(frame,width=77)
interfaz.grid(row=0,column=0,padx=11,pady=11)
interfaz.config(relief="sunken",state="disabled")
interfaz.config(bd=3)
scroll=tk.Scrollbar(frame, command=interfaz.yview)
scroll.grid(row=0, column=1,padx=0,pady=0,sticky="nsew")
interfaz.config(yscrollcommand=scroll.set)

#caja de mensaje
cajamensaje=tk.Entry(frame,width=65)
cajamensaje.grid(row=1,column=0,padx=11,pady=11,sticky="w")
cajamensaje.config(relief="sunken")
cajamensaje.config(bd=3)
cajamensaje.config(cursor="hand2")

#boton
boton=tk.Button(frame,text="Enviar",width=5,command=enviar)
boton.grid(row=1,column=0,padx=11,pady=11,sticky="e")
boton.config(relief="sunken")
boton.config(bd=3)
boton.config(cursor="hand2")

#Boton para Archivo
#botArchivo=tk.Button(frame,text="Añadir Archivo",width=0,command=SelArchivo)
#botArchivo.grid(row=1,column=0,padx=11,pady=11,sticky="e")
#botArchivo.config(relief="sunken")
#botArchivo.config(bd=3)
#botArchivo.config(cursor="hand2")




#hilos
Threads = Thread(target=recibe)
Threads.daemon = True
Threads.start()

#pickThre= Thread(target=Lista_Clientes)
#pickThre.daemon = True
#pickThre.start()

#Hilo de archivo
####TArchivo = Thread(target=RecibirArchivo)
####TArchivo.daemon = True
####TArchivo.start()

#para que quede abierta
ventana.mainloop()