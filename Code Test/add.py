from pymongo import *
import datetime
import time
import random
from insertclient import *
def Conectar():
	mongoClient = MongoClient('localhost',27017)
	db = mongoClient.estacionamiento
	collection = db.Autos

def insertar():

	IDusable = random.randint(1, 1000000)
	horaen = time.strftime("%X")
	fechaen = time.strftime("%x")
	horasal = 0
	fechasal = 0
	monto = 0
	candado= False
	x = Cliente(IDusable, horaen, fechaen, horasal, fechasal, monto, candado)
	collection.insert(x.toDBCollection())
	print("Insertados correctamente")
Conectar()
insertar()