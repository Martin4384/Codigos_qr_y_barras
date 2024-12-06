import os
import qrcode
from barcode import Code128
from barcode.writer import ImageWriter
from flask import Flask, request, send_file
from io import BytesIO

app = Flask(__name__)

# Ruta para generar código QR
@app.route('/qr_code', methods=['GET'])
def generate_qr():
    data = request.args.get('data')

    if not data:
        return "Error: El parámetro 'data' está vacío o no es válido", 400
    
    # Configurar el tamaño del QR
    qr = qrcode.QRCode(
        version=1,  # Controla el tamaño del QR (puedes aumentar si necesitas más datos)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,  # Tamaño de cada cuadro del QR (reduce para hacer el QR más pequeño)
        border=2    # Borde alrededor del QR (reduce para un borde más pequeño)
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')
# Ruta para generar código de barras
@app.route('/barcode', methods=['GET'])
def generate_barcode():
    data = request.args.get('data')
    if not data:
        return "Error: El parámetro 'data' está vacío o no es válido", 400
    
    barcode_img = Code128(data, writer=ImageWriter())
    options = {
        'module_width': 0.2,  # Ajusta el ancho del módulo (reduce para imágenes más pequeñas)
        'module_height': 10.0,  # Ajusta la altura del módulo
        'font_size': 10,       # Tamaño de la fuente
        'text_distance': 1.0   # Distancia del texto al código de barras
    }
    
    buffer = BytesIO()
    barcode_img.write(buffer, options)
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    # Render asigna dinámicamente el puerto, por lo que lo obtenemos desde la variable de entorno PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    #app.run(debug=True)
