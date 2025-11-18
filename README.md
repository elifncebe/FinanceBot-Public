# 📈 FinanceBot-Public

FinanceBot is a Discord bot built with **Python**, **Discord.py**, and **Yahoo Finance (yfinance)**.  
It delivers **real-time stock market data**, lets users **track prices**, manage **watchlists**, and retrieve **detailed stock info** with simple commands.

---

## 🚀 Features

- 🔹 **Real-Time Stock Prices** using Yahoo Finance 1-minute data  
- 🔹 **Auto-Updating Watchlists** (updates every minute per channel)  
- 🔹 **Detailed Stock Info** including market cap, 52-week range, summaries, etc.  
- 🔹 **Clean, simple command system** using `$` prefix  
- 🔹 **Error handling & helpful feedback**

---

## 📦 Tech Stack

- Python 3.10+
- discord.py
- yfinance
- python-dotenv
- pytz

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/FinanceBot-Public.git
cd FinanceBot-Public
```
2. Install dependencies
```
pip install -r requirements.txt
```
4. Add your Discord token
Create a .env file in the project directory:
```
DISCORD_TOKEN=your_bot_token_here
```
4. Run the bot
```
python bot.py
```
💬 Commands
Command	Description
$price SYMBOL	Get the real-time or latest available price of a stock.
$watch SYMBOL	Add a symbol to the channel’s watchlist for auto-updates.
$unwatch SYMBOL	Remove a symbol from the watchlist.
$watchlist	View all symbols currently being watched.
$info SYMBOL	Get detailed stock information including summary, market cap, and 52-week range.
$commands	Show the full list of commands.

📘 Example Usage
```
$price AAPL
$watch TSLA
$unwatch GOOGL
$watchlist
$info MSFT
```

🔧 How It Works
🔄 Real-Time Data Retrieval
FinanceBot uses yfinance.Ticker.history(period='1d', interval='1m') to get real-time data.
If real-time data is unavailable (market closed), it falls back to:

regularMarketPrice

previousClose

🕒 Automatic Watchlist Updates
Every 1 minute, the bot posts updated prices for all watched stocks in each channel.

📊 Rich Stock Info
$info sends a Discord embed containing:
Company full name
Summary/business description
Market cap
Current/latest price
52-week high & low

📂 Project Structure
```
FinanceBot-Public/
│
├── bot.py
├── requirements.txt
├── .env              # Holds your bot token (make sure to put your Discord Bot token)
└── README.md
```

