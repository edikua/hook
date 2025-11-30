import logging
import os

from flask import Flask, request, jsonify
from pybit.unified_trading import HTTP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Read API keys from environment variables
API_KEY = os.environ.get("BYBIT_API_KEY")
API_SECRET = os.environ.get("BYBIT_API_SECRET")
USE_TESTNET = os.environ.get("BYBIT_TESTNET", "false").lower() == "true"


def get_client():
    """Create and return a Bybit HTTP client."""
    if not API_KEY or not API_SECRET:
        raise ValueError("BYBIT_API_KEY and BYBIT_API_SECRET must be set")

    return HTTP(
        testnet=USE_TESTNET,
        api_key=API_KEY,
        api_secret=API_SECRET,
    )


@app.route("/")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Webhook bot is running"})


@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming webhook requests from TradingView."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        action = data.get("action")
        symbol = data.get("symbol")
        qty = data.get("qty")
        price = data.get("price")

        if not action:
            return jsonify({"error": "Missing 'action' field"}), 400

        if not symbol:
            return jsonify({"error": "Missing 'symbol' field"}), 400

        # Clean symbol - remove .P suffix if present (TradingView Bybit Perpetual format)
        if symbol.endswith(".P"):
            symbol = symbol[:-2]

        # Validate qty if provided
        if qty is not None:
            try:
                qty_val = float(qty)
                if qty_val <= 0:
                    return jsonify({"error": "qty must be a positive number"}), 400
            except (ValueError, TypeError):
                return jsonify({"error": "qty must be a valid number"}), 400

        # Validate price if provided
        if price is not None:
            try:
                price_val = float(price)
                if price_val <= 0:
                    return jsonify({"error": "price must be a positive number"}), 400
            except (ValueError, TypeError):
                return jsonify({"error": "price must be a valid number"}), 400

        client = get_client()

        if action == "entry_long":
            # Place limit BUY order
            if not qty or not price:
                return jsonify({"error": "Missing 'qty' or 'price' for entry_long"}), 400

            response = client.place_order(
                category="linear",
                symbol=symbol,
                side="Buy",
                orderType="Limit",
                qty=str(qty),
                price=str(price),
            )
            return jsonify({"success": True, "action": action, "response": response})

        elif action == "entry_short":
            # Place limit SELL order
            if not qty or not price:
                return jsonify({"error": "Missing 'qty' or 'price' for entry_short"}), 400

            response = client.place_order(
                category="linear",
                symbol=symbol,
                side="Sell",
                orderType="Limit",
                qty=str(qty),
                price=str(price),
            )
            return jsonify({"success": True, "action": action, "response": response})

        elif action == "cancel":
            # Cancel all pending orders for the symbol
            response = client.cancel_all_orders(
                category="linear",
                symbol=symbol,
            )
            return jsonify({"success": True, "action": action, "response": response})

        elif action == "exit_long":
            # Close long position (market order)
            if not qty:
                return jsonify({"error": "Missing 'qty' for exit_long"}), 400

            response = client.place_order(
                category="linear",
                symbol=symbol,
                side="Sell",
                orderType="Market",
                qty=str(qty),
                reduceOnly=True,
            )
            return jsonify({"success": True, "action": action, "response": response})

        elif action == "exit_short":
            # Close short position (market order)
            if not qty:
                return jsonify({"error": "Missing 'qty' for exit_short"}), 400

            response = client.place_order(
                category="linear",
                symbol=symbol,
                side="Buy",
                orderType="Market",
                qty=str(qty),
                reduceOnly=True,
            )
            return jsonify({"success": True, "action": action, "response": response})

        else:
            return jsonify({"error": f"Unknown action: {action}"}), 400

    except ValueError as e:
        logger.error("Validation error: %s", str(e))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error("Unexpected error processing webhook: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
