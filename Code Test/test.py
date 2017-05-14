from xhtml2pdf import pisa
import sys, qrcode
n="10:04:03 PM"
sourceHTML = """
<!DOCTYPE html>
<html>
<body style="text-align: center;">
    <h2>Ticket de Estacionamiento</h2>
    <h3>CMMi Poject</h3>
    <p>NOTA: No nos hacemos responsables de cualquier Robo, Perdida o Da&ntilde;os<br/> 
    causados por terceros a su veh&iacute;culo o a su contenido, as&iacute; como de <br/>
     las sancciones por mal aparcamiento.</p>
    <img src="/home/julio/Documents/Estacionamiento/QR/""" + n +""".png">
    <p>Fecha y hora de ingreso:</p>
    <p><h4>&#161;GRACIAS POR SU VISITA&#33;</h4></p>
    <table border="1" align="center">

				<tr><td><img src="ima/ps.jpg"></td><td>
					<h3>Consola PlayStation 4 de 500GB + FIFA 16 - Fifa 16 Bundle Edition<br/>
					de Sony Computer Entertainment<br/></h3>
					PlayStation 4<br/>
					$869.00
					<ul >
						<li id="carrito"><a href=""><span>A&ntilde;adir al carrito</span></a></li>
					</ul>
				</td></tr>

				<tr><td><img src="ima/3ds.jpg"></td><td>
					<h3>Consola Nintendo 3DS XL New - Color NegroNintendo 3DS<br/>
					de Nintendo<br/></h3>
					Nintendo 3DS<br/>
					$439.00
					<ul >
						<li id="carrito"><a href=""><span>A&ntilde;adir al carrito</span></a></li>
					</ul>
				</td></tr>

				<tr><td><img src="ima/one.jpg"></td><td>
					<h3>Consola Xbox One 500 GB HDD "Elige tu juego" - Bundle EditionXbox One<br/>
					de Microsoft Game Studios</h3>
					Xbox One<br/>
					$640.00
					<ul >
						<li id="carrito"><a href=""><span>A&ntilde;adir al carrito</span></a></li>
					</ul>
				</td></tr>

				<tr><td><img src="ima/wii.jpg"></td><td>
					<h3>Consola Nintendo Wii U 32GB + Mario Kart 8 Deluxe Set - Standard EditionNintendo Wii U<br/>
					de Nintendo<br/></h3>
					Nintendo Wii<br/>
					$674.00
					<ul >
						<li id="carrito"><a href=""><span>A&ntilde;adir al carrito</span></a></li>
					</ul>
				</td></tr>

				<tr><td><img src="ima/control.jpg"></td><td>
					<h3>Control Inalambrico para Xbox One, EdiciOn Limitada: Halo 5 Guardians - Spartan Lock, azul - Special Edition<br/>
					de Microsoft Game Studios<br/></h3>
					Xbox One<br/>
					$94.00
					<ul >
						<li id="carrito"><a href=""><span>A&ntilde;adir al carrito</span></a></li>
					</ul>
				</td></tr>
			</table>
    </body>
</html>
<style>
    @page {
        size: letter portrait;
        margin: 2cm;
    }
</style>
"""
 
outFilename = "/home/julio/Documents/Estacionamiento/Tickets/" +n+ ".pdf"
outFile = open(outFilename, "w+b")
pisaStatus = pisa.CreatePDF(sourceHTML, dest=outFile)
outFile.close()
print pisaStatus.err
