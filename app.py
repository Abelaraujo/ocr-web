from flask import Flask, render_template, request
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import io

app = Flask(__name__)

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


@app.route("/", methods=["GET", "POST"])
def index():

    texto = ""
    mensagem = ""

    if request.method == "POST":

        arquivo = request.files["imagem"]

        if arquivo:

            imagem = Image.open(
                io.BytesIO(arquivo.read())
            )

            imagem = imagem.convert("L")

            imagem = ImageEnhance.Contrast(
                imagem
            ).enhance(2)

            imagem = imagem.filter(
                ImageFilter.SHARPEN
            )

            texto = pytesseract.image_to_string(
                imagem,
                lang="por"
            )

            linhas = [
                l.strip()
                for l in texto.split("\n")
                if l.strip()
            ]

            texto = "\n".join(linhas)

            # Se não conseguir ler
            if not texto.strip():

                mensagem = (
                    "Não foi possível "
                    "ler o texto da imagem."
                )

    return render_template(
        "index.html",
        texto=texto,
        mensagem=mensagem
    )


if __name__ == "__main__":
    app.run()
