from flask import Flask, request, jsonify
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# Make sure a folder exists for saving mp3s
if not os.path.exists('static'):
    os.makedirs('static')

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

    # Generate unique filename to avoid conflicts
    filename = f"static/{uuid.uuid4()}.mp3"

    # Convert reply text to speech
    tts = gTTS(text=reply, lang='en')
    tts.save(filename)

    # Return both text and audio file path
    return jsonify({
        'reply': reply,
        'audio': filename
    })

if __name__ == '__main__':
    app.run()
