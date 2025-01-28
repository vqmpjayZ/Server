from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Image Converter API!", "status": "deployed"}), 200

@app.route('/convert-image', methods=['GET', 'POST'])
def convert_image():
    image_url = None

    if request.method == 'GET':
        image_url = request.args.get('url')
        if not image_url:
            return jsonify({'error': 'No URL provided in query parameters'}), 400

    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided in request body'}), 400
        image_url = data['url']

    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        image = image.resize((32, 32))

        pixels = []
        for y in range(image.height):
            for x in range(image.width):
                r, g, b = image.getpixel((x, y))[:3]
                pixels.append({'R': r, 'G': g, 'B': b})

        return jsonify({'pixels': pixels})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
