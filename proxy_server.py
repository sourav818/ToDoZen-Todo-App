from flask import Flask, request, jsonify, send_from_directory
import requests
from ai_module import suggest_priority  # Ensure this is correctly defined
import os

app = Flask(__name__)

# Define the URL of the original app
ORIGINAL_APP_URL = "http://192.168.29.102:8080"

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Proxy Server!"})

@app.route('/favicon.ico')
def favicon():
    # Return a placeholder favicon or an empty response to avoid 500 error
    return send_from_directory(os.getcwd(), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/add-task', methods=['POST'])
def ai_add_task():
    """
    Intercepts the /add-task endpoint to inject AI logic.
    """
    try:
        data = request.json
        title = data.get('title')
        priority = data.get('priority')

        # Use AI to suggest priority if not provided
        if not priority:
            try:
                priority = suggest_priority(title)  # AI logic
            except Exception as e:
                return jsonify({"error": f"AI suggestion failed: {str(e)}"}), 500

        data['priority'] = priority

        # Forward the request to the original app
        response = requests.post(f"{ORIGINAL_APP_URL}/add-task", json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Request handling failed: {str(e)}"}), 500

@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    """
    Pass-through proxy for all other endpoints.
    """
    try:
        if request.method == "GET":
            response = requests.get(f"{ORIGINAL_APP_URL}/{path}", params=request.args)
        elif request.method == "POST":
            response = requests.post(f"{ORIGINAL_APP_URL}/{path}", json=request.json)
        elif request.method == "PUT":
            response = requests.put(f"{ORIGINAL_APP_URL}/{path}", json=request.json)
        elif request.method == "DELETE":
            response = requests.delete(f"{ORIGINAL_APP_URL}/{path}")

        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error connecting to the original app: {str(e)}"}), 500

if __name__ == "__main__":
    try:
        # Start the Flask app with reloader disabled to avoid automatic restarts
        app.run(port=8082, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
