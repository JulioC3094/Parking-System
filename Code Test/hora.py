import time
import datetime

#25 la primera hora y luego 15 las siguientes hora o fraccion.
def TotalP(HMS):
	if (HMS[0]>1):
		if(int(HMS[1])>0):
			HMS[0]= int(HMS[0])+1
		deb= 25 + ((int(HMS[0])-1) *15)
		print(HMS)
	else:
		deb=25
	return deb

FecyHo= str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).split(' ')
horaen = FecyHo[1]
fechaen = FecyHo[0]
d1 = datetime.datetime.strptime(fechaen+" "+ horaen, "%Y-%m-%d %H:%M:%S")
d2 = datetime.datetime.strptime("2016-05-09 13:16:10", "%Y-%m-%d %H:%M:%S")
dr= d2-d1
print(dr)
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
deb = TotalP(HMS)
print("Usted debe pagar: $"+ str(deb))
#pago=str(dr).split(',')
#dias=pago[0][0]
#HMS= pago[1].split(':')
#res=int(HMS[0])+2
#print (pago, "Dias", dias, "Horas", HMS, "Res", res)

