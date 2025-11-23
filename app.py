from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_meme():
    data = request.json
    meme_url = f"https://picsum.photos/400/300?random={random.randint(1,1000)}"
    return jsonify({"meme_url": meme_url})

if __name__ == '__main__':
    app.run(debug=True)
