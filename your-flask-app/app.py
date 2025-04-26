from flask import Flask, request, jsonify
import pyttsx3

app = Flask(__name__)

# Initialize Nova's voice engine
engine = pyttsx3.init()

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    text = data['text']
    print(f"User said: {text}")

    # Nova's logic
    if 'hello' in text.lower():
        reply = "Hello! How can I help you?"
    else:
        reply = "I'm not sure what you mean."

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run()
