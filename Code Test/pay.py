import sys
import qrcode
from pymongo import *
import datetime
import time
import random
from insertclient import *
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import threading
import socket
from Queue import Queue 

form_class = uic.loadUiType("Pay.ui")[0]


class MyWindowClass(QtGui.QMainWindow, form_class):
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		q=Queue()
		self.setupUi(self)
		self.servidor(q)
		time=threading.Timer(1,self.dato,args=q)
		time.start()

		#self.BTNPay.clicked.connect(self.BTNPay_clicked)
	def dato(self,q):
		if (not(q.empty())):
			print('entro')
			self.TXTPay.setText(str(q.get()))

	def hilo(self,q,add,serversocket,stop_e):
		while(not stop_e.is_set()):
			(clientsocket, address) = serversocket.accept()
			print ("connection found!")
			data = clientsocket.recv(1024).decode()
			print(data)
			q.put(data)
			

	def servidor(self,q):
		port = 7777
		add= '192.168.1.76'
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((add, port))
		sock.listen(5)
		t_stop=threading.Event()
		t=threading.Thread(target=self.hilo,args=(q,add,sock,t_stop))
		t.start()


	def CheckData(self,stop):
		stop.set()
		self.check()

		#coneccion 
	def check(self):
		mongoClient = MongoClient('localhost',27017)
		db = mongoClient.estacionamiento
		collection = db.Autos
		cursor = collection.find({'IDusable': 527680, 'FechaEntrada': '2016-05-09' , 'HoraEntrada': '13:36:35'})
		curs = cursor.count()
		if curs >0:
			fechaen=None
			horaen=None
			Candado=None
			for document in cursor:
				#self.TXTPay.setText(document['FechaEntrada'] + document['HoraEntrada'] + str(document['IDusable']) + str(document['FechaSalida']) + str(document['Candado']))
				fechaen=document['FechaEntrada']
				horaen=document['HoraEntrada']
				candado=document['Candado']
				print('Entro para sacar datos')
				
				
			if candado==False:
				#self.TXTPay.append('Usted debe dinero')
				deb, fechasal, horasal, HMS = self.TotalPagar(horaen, fechaen)
				result = collection.update_one({'IDusable': 527680, 'FechaEntrada': '2016-05-09' , 'HoraEntrada': '13:36:35'},{'$set': {'FechaSalida':fechasal, 'HoraSalida': horasal, 'Monto': deb, 'Candado': True}})
				if result.modified_count==1:
					self.TXTPay.setText('----------------Hora de entrada----------------\n' +'Hora de entrada: '+ horaen + '\nFecha de entrada: ' + fechaen)
					self.TXTPay.append('----------------Datos de Salida de Auto-----------------\nHora de salida: '+horasal+'\nFecha de salida: '+ fechasal + '\nHoras en estacionamiento: '+ str(HMS[0])+ ':'+ str(HMS[1])+':'+ str(HMS[2])+'\nTotal a pagar: $'+ str(deb))
					self.TXTPay.append('----------------Gracias por su visita-----------------')
					print('Actualizo Datos')
				else:
					self.TXTPay.setText('------------Error en la actualizacion de datos------------')

			else:
				self.TXTPay.setText('Su ticket ya ha expirado(ticket ya se pago anteriormente).')
				print('Mensaje Enviado')
		else:
			self.TXTPay.setText("No se encontraron coincidencias.\nPor favor revise su boleto")
		mongoClient.close()#cierra la conexion de DB
		print(cursor)

	def TotalPagar(self, horaen, fechaen):
		FecyHo= str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).split(' ')
		horasal = FecyHo[1]
		fechasal = FecyHo[0]
		d1 = datetime.datetime.strptime(fechaen+" "+ horaen, "%Y-%m-%d %H:%M:%S")
		d2 = datetime.datetime.strptime(fechasal + " " + horasal, "%Y-%m-%d %H:%M:%S")
		dr= d2-d1
		pay=str(dr).split(' ')
		print (pay)
		dias=False
		for i in pay:
			if (i=="day," or i=="days,"): 
				print ("hay un dia")
				diaH= int(pay[0])*24
				HMS= pay[2].split(':')
				HMS[0]= int(HMS[0])+diaH
				print( "DiasH ", diaH, " Horas ", HMS)
				dias=True
				break
		if (dias==False):
			HMS= pay[0].split(':')
		print (HMS)
		horas=0
		if (HMS[0]>1):
			if(int(HMS[1])>0):
				horas= int(HMS[0])+1
			deb= 25 + ((int(horas)-1) *15)
			print(HMS)
		else:
			deb=25
		return deb, fechasal, horasal, HMS

	
	
#Iniciar la interfaz grafica(siempre al final):
app = QtGui.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
#t = QtCore.QTimer()
#t.singleShot(0,MyWindow.servidor)
app.exec_()
