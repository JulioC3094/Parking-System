# En primer lugar debemos de abrir el fichero que vamos a leer.
# Usa 'rb' en vez de 'r' si se trata de un fichero binario.
infile = open('mtp://[usb:003,004]/Card/smart_jni.txt', 'r')
# Mostramos por pantalla lo que leemos desde el fichero
print('>>> Lectura completa del fichero')
print(infile.read())
# Cerramos el fichero.
infile.close()