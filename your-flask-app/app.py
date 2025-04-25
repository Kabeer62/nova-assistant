from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# Home route - serves the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

# Route to start the Nova assistant when button is clicked
@app.route('/start-nova', methods=['POST'])
def start_nova():
    try:
        subprocess.Popen(['python', 'main.py'])  # Make sure main.py runs Nova
        return jsonify({"status": "success", "message": "Nova assistant started."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Use host='0.0.0.0' if Safari still blocks localhost (or use 'localhost')
    app.run(debug=True, host='localhost', port=5000)