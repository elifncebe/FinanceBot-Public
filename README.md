# FinanceBot-Public
FinanceBot is a Discord bot built with Python, Discord.py, and Yahoo Finance (yfinance).
It delivers real-time stock market data, allows users to track prices, manage watchlists, and fetch detailed stock info with simple, intuitive commands.

FEATURES

Real-time stock prices using Yahoo Finance 1-minute interval data.

Auto-updating watchlists that post price updates every minute.

Detailed stock information (market cap, 52-week high/low, summaries, etc.).

Simple and clean command setup using the $ prefix.

TECH STACK

Python 3.10+

discord.py

yfinance

dotenv

pytz

INSTALLATION & SETUP

Clone the repository:
git clone https://github.com/YOUR_USERNAME/FinanceBot-Public.git

Install dependencies:
pip install -r requirements.txt

Create a .env file in the project folder with the following line:
DISCORD_TOKEN=your_bot_token_here

Run the bot:
python bot.py

COMMANDS

$price SYMBOL - Get the real-time or latest stock price.
$watch SYMBOL - Add a stock to the channel watchlist.
$unwatch SYMBOL - Remove a stock from the watchlist.
$watchlist - Show the list of stocks being monitored.
$info SYMBOL - Get detailed information about a stock.
$commands - Display all available commands.

EXAMPLE USAGE

$price AAPL
$watch TSLA
$unwatch GOOGL
$watchlist
$info MSFT

HOW IT WORKS

Real-Time Data:
The bot uses yfinance to pull 1-minute interval data. If real-time data is unavailable,
it falls back to regularMarketPrice or previousClose.

Auto Price Updates:
The bot automatically sends updated prices every 1 minute for all watched symbols
in each channel.

Stock Info:
$info returns embedded stock information including summary, market cap, and 52-week
high/low values.

FILE STRUCTURE

FinanceBot-Public/
bot.py
requirements.txt
.env (not included)
readme.txt
