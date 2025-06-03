from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from pyzbar.pyzbar import decode
import requests
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    product = None
    barcode_result = None

    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            imagem = Image.open(filepath).convert("L")
            codigos_barras = decode(imagem)

            if len(codigos_barras) > 0:
                barcode_result = codigos_barras[0].data.decode("utf-8")
                url = f"https://world.openfoodfacts.org/api/v0/product/{barcode_result}.json"
                response = requests.get(url)
                data = response.json()
                product = data["product"]
            else:
                barcode_result = "Nenhum código de barras identificado."
                product = {'teste': 'Teste'}

    return render_template("index.html", resultado=product)
