from flask import Flask, request, send_file
from io import BytesIO
import qrcode
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)

# Ruta para generar código QR
@app.route('/qr_code', methods=['GET'])
def generate_qr():
    data = request.args.get('data')
    qr_img = qrcode.make(data)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

# Ruta para generar código de barras
@app.route('/barcode', methods=['GET'])
def generate_barcode():
    data = request.args.get('data')
     # Verificar si data está vacío o no válido
    if not data:
        return "Error: El parámetro 'data' está vacío o no es válido", 400

    barcode_img = barcode.get('code128', data, writer=ImageWriter())
    buffer = BytesIO()
    barcode_img.write(buffer)
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
