from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

BACKGROUND_PATH = "background.png"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SIZE = 48
TEXT_FILL = (255, 255, 255)
TEXT_POSITION = (50, 300)

@app.route("/")
def index():
    return "Flask app is running."

@app.route("/generate", methods=["POST"])
def generate_image():
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return {"error": "POST must include 'text'"}, 400

    text = data["text"]

    try:
        bg = Image.open(BACKGROUND_PATH).convert("RGB")
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        draw = ImageDraw.Draw(bg)
        draw.text(TEXT_POSITION, text, font=font, fill=TEXT_FILL)
    except Exception as e:
        return {"error": str(e)}, 500

    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    buf.seek(0)

    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
from flask import Response

@app.route("/")
def index():
    return Response("Flask app is running.", mimetype="text/html")

