import sys
import qrcode
from pymongo import *
import datetime
import time
import random
from insertclient import *
import qrcode
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PIL import Image
from xhtml2pdf import pisa
import cups
# 	import media

form_class = uic.loadUiType("Estacionamiento.ui")[0]


class MyWindowClass(QtGui.QMainWindow, form_class):

	def __init__(self, parent=None):
	  QtGui.QMainWindow.__init__(self, parent)
	  self.setupUi(self)
	  self.BTNGen.clicked.connect(self.BTNGen_clicked)
	def BTNGen_clicked(self):
		#coneccion
		mongoClient = MongoClient('localhost',27017)
		db = mongoClient.estacionamiento
		collection = db.Autos
		#Insecion
		IDusable = random.randint(1, 1000000)
		FecyHo= str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).split(' ')
		horaen = FecyHo[1]
		fechaen = FecyHo[0]
		horasal = "0"
		fechasal = "0"
		monto = 0
		candado= False
		#crear codigo QR
		self.QR(IDusable, horaen, fechaen) #recibe la imagen
		self.ticket(horaen, fechaen)

		x = Cliente(IDusable, horaen, fechaen, horasal, fechasal, monto, candado)
		collection.insert(x.toDBCollection())
		mongoClient.close()
		self.Print(horaen)
		######
		self.TXTReg.setText("Se ha ingresado un auto. \nTicket Generado\n---------Datos de entrada---------\nFecha: " + fechaen + "\nHora: "+ horaen )
		self.TXTReg.append("\n---------Bienvenido---------")
	def QR(self, IDusable,horaen, fechaen):
		img = qrcode.make(str(IDusable)+' '+str(fechaen)+' '+ str(horaen))
		img.save('/home/julio/Documents/Estacionamiento/QR/'+str(horaen)+ '.png')
		#f = Image.open('/home/julio/Documents/Estacionamiento/QR/'+str(horaen)+ '.png')
 		#f.show()
 		#return f
		###

	def ticket(self, hora, fecha):
		sourceHTML = """
			<!DOCTYPE html>
			<html>
			<body style="text-align: center;">
    			<h2>Ticket de Estacionamiento</h2>
    			<h3>CMMi Poject</h3>
    			<p>NOTA: No nos hacemos responsables de cualquier Robo, Perdida o Da&ntilde;os<br/>
    			causados por terceros a su veh&iacute;culo o a su contenido, as&iacute; como de <br/>
     			las sancciones por mal aparcamiento.</p>
    			<img src="/home/julio/Documents/Estacionamiento/QR/""" + hora +""".png">
    			<p>Fecha y hora de ingreso: """ + str(fecha)+" "+ str(hora)+ """</p>
    			<p><h4>&#161;GRACIAS POR SU VISITA&#33;</h4></p>
    			</body>
			</html>
			<style>
    			@page {
        			size: letter portrait;
        			margin: 2cm;
    			}
			</style>
			"""
 		outFilename = "/home/julio/Documents/Estacionamiento/Tickets/" +hora+ ".pdf"
		outFile = open(outFilename, "w+b")
		pisaStatus = pisa.CreatePDF(sourceHTML, dest=outFile)
		outFile.close()
		print pisaStatus.err
	def Print (self, horaen): #imprimir documento
		conn = cups.Connection()
		printers = conn.getPrinters ()
		file="/home/julio/Documents/Estacionamiento/Tickets/" +horaen+ ".pdf"
		printer_name=printers.keys()[0]
		conn.printFile (printer_name, file, "PDF Print", {})
		print("Print Successful")


#Iniciar la interfaz grafica(siempre al final):
app = QtGui.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()
