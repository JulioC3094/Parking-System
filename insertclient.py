class Cliente:
	def __init__(self, IDusable, HoraEntrada, FechaEntrada, HoraSalida, FechaSalida, Monto, Candado):
		self.IDusable=IDusable
		self.HoraEntrada=HoraEntrada
		self.FechaEntrada=FechaEntrada
		self.HoraSalida=HoraSalida
		self.FechaSalida=FechaSalida
		self.Monto=Monto
		self.Candado=Candado

	def toDBCollection(self):
		return{
			"IDusable":self.IDusable,
			"HoraEntrada":self.HoraEntrada,
			"FechaEntrada":self.FechaEntrada,
			"HoraSalida":self.HoraSalida,
			"FechaSalida":self.FechaSalida,
			"Monto":self.Monto,
			"Candado":self.Candado 
		}