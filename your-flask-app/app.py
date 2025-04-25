from flask import Flask, render_template, request, jsonify
from nova_core import get_nova_response  # This is your new core logic handler

app = Flask(__name__)

# Home route - serves the chat HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat POST requests
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if user_input:
        response = get_nova_response(user_input)
        return jsonify({"response": response})
    return jsonify({"response": "No input received."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
