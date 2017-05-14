import datetime
import time
from pymongo import *
from xhtml2pdf import pisa
import threading

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
			cursor = collection.find({'FechaSalida': HoFec[1]})#str(FecHo[0]
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
		#else:
		#	print('Aun no se puede generar el reporte')

threads = list()
t = threading.Thread(target=Reporte)
threads.append(t)
t.start()
print ('Empezo el hilo')
n=10
while n==0:
	print("Impresiones en: "+ str(n))
	n=n-1
input()