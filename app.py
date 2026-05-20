from flask import Flask, render_template, request
from PIL import Image
import pytesseract

app = Flask(__name__)

# Caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/", methods=["GET", "POST"])
def index():
    texto = ""

    if request.method == "POST":
        arquivo = request.files["imagem"]

        if arquivo:
            imagem = Image.open(arquivo)
            texto = pytesseract.image_to_string(imagem, lang="por")

    return render_template("index.html", texto=texto)

app.run(debug=True)