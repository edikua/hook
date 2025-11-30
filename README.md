# TradingView → Bybit Webhook Bot

A Flask webhook bot that receives alerts from TradingView and executes trades on Bybit using limit and market orders.

## Features

- **entry_long** - Place limit BUY order
- **entry_short** - Place limit SELL order
- **cancel** - Cancel all pending orders for a symbol
- **exit_long** - Close long position (market order)
- **exit_short** - Close short position (market order)

## Deploy on Railway

1. Fork this repository
2. Go to [Railway](https://railway.app/) and create a new project
3. Select "Deploy from GitHub repo" and choose your forked repository
4. Add the following environment variables in Railway:
   - `BYBIT_API_KEY` - Your Bybit API key
   - `BYBIT_API_SECRET` - Your Bybit API secret
5. Railway will automatically deploy your bot and provide a public URL

## Configure TradingView Alerts

1. In TradingView, create a new alert
2. Set the webhook URL to your Railway deployment URL + `/webhook`
   - Example: `https://your-app.railway.app/webhook`
3. Set the alert message to one of the JSON payloads below

## Webhook JSON Payloads

### Entry Long (Limit Buy Order)
```json
{"action":"entry_long","symbol":"SQDUSDT","qty":500,"price":0.058}
```

### Entry Short (Limit Sell Order)
```json
{"action":"entry_short","symbol":"SQDUSDT","qty":500,"price":0.062}
```

### Cancel All Orders
```json
{"action":"cancel","symbol":"SQDUSDT"}
```

### Exit Long (Market Sell to Close)
```json
{"action":"exit_long","symbol":"SQDUSDT","qty":500}
```

### Exit Short (Market Buy to Close)
```json
{"action":"exit_short","symbol":"SQDUSDT","qty":500}
```

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hook.git
   cd hook
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export BYBIT_API_KEY="your_api_key"
   export BYBIT_API_SECRET="your_api_secret"
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

5. The bot will be available at `http://localhost:5000`

## Endpoints

- `GET /` - Health check endpoint
- `POST /webhook` - Webhook endpoint for TradingView alerts

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BYBIT_API_KEY` | Your Bybit API key |
| `BYBIT_API_SECRET` | Your Bybit API secret |
| `BYBIT_TESTNET` | Set to `true` to use Bybit testnet (default: `false`) |
| `PORT` | Port to run the server (default: 5000) |

## License

MIT