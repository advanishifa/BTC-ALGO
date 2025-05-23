from flask import Flask, request
import requests
import hmac
import hashlib
import time
import os

app = Flask(__name__)

# Load BingX API credentials from environment variables
BINGX_API_KEY = os.getenv("BINGX_API_KEY")
BINGX_SECRET_KEY = os.getenv("BINGX_SECRET_KEY")

# Verify API keys are loaded
if not BINGX_API_KEY or not BINGX_SECRET_KEY:
    raise ValueError("BingX API key or secret key not found in environment variables")

@app.route('/webhook', methods=['POST'])
def webhook():
    # Receive TradingView webhook payload
    data = request.json
    print("Received webhook:", data)

    # Parse the alert (expecting "buy" for long, "sell" for short)
    action = data.get('action')
    symbol = "ETHUSDT"  # From your setup
    quantity = 0.01  # Adjust based on your risk management and capital

    if action not in ["buy", "sell"]:
        print("Invalid action received:", action)
        return "Invalid action", 400

    # Map TradingView action to BingX side
    side = "BUY" if action == "buy" else "SELL"

    # Prepare BingX API request
    timestamp = int(time.time() * 1000)
    params = f"symbol={symbol}&side={side}&type=MARKET&quantity={quantity}×tamp={timestamp}"
    signature = hmac.new(BINGX_SECRET_KEY.encode(), params.encode(), hashlib.sha256).hexdigest()

    url = "https://api.bingx.com/openApi/swap/v2/trade/order"
    headers = {"X-BX-APIKEY": BINGX_API_KEY}
    payload = {
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity,
        "timestamp": timestamp,
        "signature": signature
    }

    # Place trade on BingX
    try:
        response = requests.post(url, headers=headers, params=payload)
        response_data = response.json()
        print("BingX response:", response_data)
        return "Trade placed successfully", 200
    except Exception as e:
        print("Error placing trade:", str(e))
        return f"Error placing trade: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
