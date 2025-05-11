
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("✅ Webhook received:", data)
    return jsonify({"status": "success", "message": "Webhook accepted"}), 200

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
