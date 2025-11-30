import json
import unittest
from unittest.mock import patch, MagicMock

from bot import app


class TestSymbolCleaning(unittest.TestCase):
    """Test symbol cleaning logic for .P suffix removal."""

    def setUp(self):
        """Set up test client."""
        self.client = app.test_client()
        app.config["TESTING"] = True

    @patch("bot.get_client")
    def test_symbol_with_p_suffix_is_cleaned(self, mock_get_client):
        """Test that .P suffix is removed from symbol."""
        mock_client = MagicMock()
        mock_client.cancel_all_orders.return_value = {"retCode": 0}
        mock_get_client.return_value = mock_client

        response = self.client.post(
            "/webhook",
            data=json.dumps({"action": "cancel", "symbol": "KGENUSDT.P"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        # Verify the API was called with cleaned symbol (without .P)
        mock_client.cancel_all_orders.assert_called_once_with(
            category="linear", symbol="KGENUSDT"
        )

    @patch("bot.get_client")
    def test_symbol_without_p_suffix_unchanged(self, mock_get_client):
        """Test that symbol without .P suffix remains unchanged."""
        mock_client = MagicMock()
        mock_client.cancel_all_orders.return_value = {"retCode": 0}
        mock_get_client.return_value = mock_client

        response = self.client.post(
            "/webhook",
            data=json.dumps({"action": "cancel", "symbol": "BTCUSDT"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        mock_client.cancel_all_orders.assert_called_once_with(
            category="linear", symbol="BTCUSDT"
        )

    @patch("bot.get_client")
    def test_entry_long_with_p_suffix(self, mock_get_client):
        """Test entry_long action with .P suffix symbol."""
        mock_client = MagicMock()
        mock_client.place_order.return_value = {"retCode": 0}
        mock_get_client.return_value = mock_client

        response = self.client.post(
            "/webhook",
            data=json.dumps(
                {
                    "action": "entry_long",
                    "symbol": "ETHUSDT.P",
                    "qty": 1,
                    "price": 2000,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        mock_client.place_order.assert_called_once_with(
            category="linear",
            symbol="ETHUSDT",
            side="Buy",
            orderType="Limit",
            qty="1",
            price="2000",
        )

    @patch("bot.get_client")
    def test_entry_short_with_p_suffix(self, mock_get_client):
        """Test entry_short action with .P suffix symbol."""
        mock_client = MagicMock()
        mock_client.place_order.return_value = {"retCode": 0}
        mock_get_client.return_value = mock_client

        response = self.client.post(
            "/webhook",
            data=json.dumps(
                {
                    "action": "entry_short",
                    "symbol": "BTCUSDT.P",
                    "qty": 0.01,
                    "price": 50000,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        mock_client.place_order.assert_called_once_with(
            category="linear",
            symbol="BTCUSDT",
            side="Sell",
            orderType="Limit",
            qty="0.01",
            price="50000",
        )

    @patch("bot.get_client")
    def test_exit_long_with_p_suffix(self, mock_get_client):
        """Test exit_long action with .P suffix symbol."""
        mock_client = MagicMock()
        mock_client.place_order.return_value = {"retCode": 0}
        mock_get_client.return_value = mock_client

        response = self.client.post(
            "/webhook",
            data=json.dumps(
                {"action": "exit_long", "symbol": "SOLUSDT.P", "qty": 10}
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        mock_client.place_order.assert_called_once_with(
            category="linear",
            symbol="SOLUSDT",
            side="Sell",
            orderType="Market",
            qty="10",
            reduceOnly=True,
        )

    @patch("bot.get_client")
    def test_exit_short_with_p_suffix(self, mock_get_client):
        """Test exit_short action with .P suffix symbol."""
        mock_client = MagicMock()
        mock_client.place_order.return_value = {"retCode": 0}
        mock_get_client.return_value = mock_client

        response = self.client.post(
            "/webhook",
            data=json.dumps(
                {"action": "exit_short", "symbol": "XRPUSDT.P", "qty": 100}
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        mock_client.place_order.assert_called_once_with(
            category="linear",
            symbol="XRPUSDT",
            side="Buy",
            orderType="Market",
            qty="100",
            reduceOnly=True,
        )


if __name__ == "__main__":
    unittest.main()
