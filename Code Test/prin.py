from reportlab.pdfgen import canvas
def hello(c):
    c.drawString(100,100,"Hello World")
    canvas.drawImage(self, "/home/julio/Documents/Estacionamiento/QR/10:05:32 PM.png", 50,50, width=None,height=None,mask=None)
c = canvas.Canvas("hello.pdf")
hello(c)
c.showPage()
c.save()