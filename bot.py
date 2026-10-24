import os, json, urllib.request, urllib.parse

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL"]  # e.g. @yourchannel


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "btc-bot"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def get_price():
    try:
        d = get("https://api.coingecko.com/api/v3/simple/price"
                "?ids=bitcoin&vs_currencies=usd&include_24hr_change=true")["bitcoin"]
        return float(d["usd"]), float(d["usd_24h_change"])
    except Exception:
        d = get("https://data-api.binance.vision/api/v3/ticker/24hr?symbol=BTCUSDT")
        return float(d["lastPrice"]), float(d["priceChangePercent"])


price, change = get_price()
emoji = "🟢" if change > 0 else "🔴"
text = f"{emoji} <b>Bitcoin (BTC)</b>\nPrice: ${price:,.0f}\n24h: {change:+.2f}%"

data = urllib.parse.urlencode({
    "chat_id": CHANNEL,
    "text": text,
    "parse_mode": "HTML",
}).encode()
urllib.request.urlopen(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data, timeout=20
)
print("Posted:", text)
