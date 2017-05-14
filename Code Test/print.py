import cups
conn = cups.Connection()
printers = conn.getPrinters ()
print (printers)
file="/home/julio/Documents/Estacionamiento/Code Test/1.pdf"
#printer_name=printers.keys()[0]
#conn.printFile (printer_name, file, "PDF Print", {})