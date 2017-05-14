import sys
import qrcode
from pymongo import *
import datetime
import time
import random
from insertclient import *
import threading
import socket
from Queue import Queue


	#def hilo(##self.q,add,serversocket,stop_e):
	#	q.put(data)


def hilo(add,serversocket,stop_e):
	while(not stop_e.is_set()):
		(clientsocket, address) = serversocket.accept()
		print ("connection found!")
		data = clientsocket.recv(1024).decode()
		print(data)
		mensaje='No hay datos validos'
		if (data!=''):
			mensaje = check(data)
			clientsocket.send(mensaje.encode())
			clientsocket.close()


def servidor():
	port = 7777
	add= '192.168.1.77'
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((add, port))
	sock.listen(5)
	r = threading.Thread(target=Reporte)
	r.start()
	print ('Empezo el hilo del Reporte')
	t_stop=threading.Event()
	t=threading.Thread(target=hilo,args=(add,sock,t_stop))
	t.start()
	print('Empezo el hilo del servidor')

def TotalPagar(horaen, fechaen):
	FecyHo= str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).split(' ')
	horasal = FecyHo[1]
	fechasal = FecyHo[0]
	d1 = datetime.datetime.strptime(fechaen+" "+ horaen, "%Y-%m-%d %H:%M:%S")
	d2 = datetime.datetime.strptime(fechasal + " " + horasal, "%Y-%m-%d %H:%M:%S")
	dr= d2-d1
	pay=str(dr).split(' ')
	print (pay)
	deb=0
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

		#coneccion
def check(data):
	datos= data.split(' ')
	mensaje=''
	if (len(datos)==3):
		#conexion a BD
		mongoClient = MongoClient('localhost',27017)
		db = mongoClient.estacionamiento
		collection = db.Autos
		cursor = collection.find({'IDusable': int(datos[0]), 'FechaEntrada': datos[1] , 'HoraEntrada': datos[2]})
		curs = cursor.count()
		if curs >0:
			fechaen=None
			horaen=None
			Candado=None
			for document in cursor:
				##self.TXTPay.setText(document['FechaEntrada'] + document['HoraEntrada'] + str(document['IDusable']) + str(document['FechaSalida']) + str(document['Candado']))
				fechaen=document['FechaEntrada']
				horaen=document['HoraEntrada']
				candado=document['Candado']
				print('Entro para sacar datos')

			if candado==False:
				##self.TXTPay.append('Usted debe dinero')

				deb, fechasal, horasal, HMS= TotalPagar(horaen, fechaen)

				result = collection.update_one({'IDusable': int(datos[0]), 'FechaEntrada': datos[1] , 'HoraEntrada': datos[2]},{'$set': {'FechaSalida':fechasal, 'HoraSalida': horasal, 'Monto': deb, 'Candado': True}})
				if result.modified_count==1:
				##self.TXTPay.setText('----------------Hora de entrada----------------\n' +'Hora de entrada: '+ horaen + '\nFecha de entrada: ' + fechaen)
				##self.TXTPay.append('----------------Datos de Salida de Auto-----------------\nHora de salida: '+horasal+'\nFecha de salida: '+ fechasal + '\nHoras en estacionamiento: '+ str(HMS[0])+ ':'+ str(HMS[1])+':'+ str(HMS[2])+'\nTotal a pagar: $'+ str(deb))
				##self.TXTPay.append('----------------Gracias por su visita-----------------')
					print('Actualizo Datos')
					mensaje='Horas en estacionamiento: '+ str(HMS[0])+ ':'+ str(HMS[1])+':'+ str(HMS[2])+'\nTotal a pagar: $'+ str(deb) + '\n----------------Gracias por su visita-----------------'
				else:
					##self.TXTPay.setText('------------Error en la actualizacion de datos------------')
					print('Error en la actualizacion de datos')
					mensaje='Error en la actualizacion de datos'
			else:
			#self.TXTPay.setText('Su ticket ya ha expirado(ticket ya se pago anteriormente).')
				mensaje='Ticket expirado'
				print(mensaje)

		else:
		##self.TXTPay.setText("No se encontraron coincidencias.\nPor favor revise su boleto")
			print('No hay coincidencias')
			mensaje='No hay coincidencias'
		mongoClient.close()
		#cierra la conexion de DB
	else:
		print('Datos no validos')
		mensaje='Datos no validos'
	return mensaje



def Reporte():
	while (True):
		HoFec= str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).split(' ')
		Ho = datetime.datetime.strptime(HoFec[1],"%H:%M:%S")
		hrin= datetime.datetime.strptime("23:59:00","%H:%M:%S")
		hrsup= datetime.datetime.strptime("00:00:00","%H:%M:%S")
		#print(str(Ho) + " "+str(hrin)+ " "+ str(hrsup))
		if Ho == hrin: # and Ho <= hrsup:
			mongoClient = MongoClient('localhost',27017)
			db = mongoClient.estacionamiento
			collection = db.Autos
			cursor = collection.find({'FechaSalida': HoFec[1]})
			curs = cursor.count()
			sumamonto=0
			for document in cursor:
				sumamonto=document['Monto']+sumamonto
			mongoClient.close()
			sourceHTML = """
				<!DOCTYPE html>
				<html>
				<body >
	    			<h2 style="text-align: center;">Reporte de Estacionamiento</h2>
    				<h3 style="text-align: center;">CMMi Poject</h3>
    				<p><br/>En la fecha """+ str(HoFec[0]) +""" se ingresaron """+ str(curs) + """ autos dando una ganacia de $"""+ str(sumamonto) + """ pesos</p>
    				<p><br/>Reporte generado a la hora: """ + HoFec[1]+ """</p>
    			</body>
				</html>
				<style>
		    		@page {
       					size: letter portrait;
       					margin: 2cm;
    				}
				</style>
				"""
 			outFilename = "/home/julio/Documents/Estacionamiento/Reportes/Reporte-"+str(HoFec[0])+ ".pdf"
			outFile = open(outFilename, "w+b")
			pisaStatus = pisa.CreatePDF(sourceHTML, dest=outFile)
			outFile.close()
			print pisaStatus.err
			print('---Reporte generado---')
			time.sleep(100)

servidor()
