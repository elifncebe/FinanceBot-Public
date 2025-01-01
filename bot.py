import discord
from discord.ext import commands, tasks
import yfinance as yf
from datetime import datetime
import os
from dotenv import load_dotenv
import pytz

#Load enviroment from .env file which has the Discord bot token. 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Set up for the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

#Dictionary for storing watched symbols, mapped by channel IDs
watched_symbols = {}

class FinanceBot(commands.Cog):
    '''Class for Bot functionality'''
    def __init__(self, bot):
        ''' Initialize the FinanceBot and start the update loop'''
        self.bot = bot
        self.price_update_loop.start()

    def cog_unload(self):
        ''' If cog is unloaded, loop is cancelled'''
        self.price_update_loop.cancel()

    def get_price_data(self, symbol):
        '''Get Price Data'''
        try:
            stock = yf.Ticker(symbol)
            
            #Get real time data
            real_time_data = stock.history(period='1d', interval='1m')
            #When stock market is closed
            if not real_time_data.empty:
                latest_price = real_time_data['Close'].iloc[-1]
                return {
                    'price': latest_price,
                    'time': real_time_data.index[-1],
                    'source': 'real-time'
                }
            
            #Get info for the entered stock
            info = stock.info
            if info.get('regularMarketPrice'):
                return {
                    'price': info['regularMarketPrice'],
                    'time': datetime.now(pytz.UTC),
                    'source': 'regular'
                }
            
            #If the market is closed, then the price will be previous close
            return {
                'price': info.get('previousClose'),
                'time': datetime.now(pytz.UTC),
                'source': 'previous'
            }
        except Exception as e:
            raise Exception(f"Error fetching data: {str(e)}")

    #For watched stock prices, will update every (1) minute.
    @tasks.loop(minutes=1)
    async def price_update_loop(self):
        '''Update prices for watched symbols every minute'''
        for channel_id, symbols in watched_symbols.items():
            if symbols:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    for symbol in symbols:
                        try:
                            data = self.get_price_data(symbol)
                            if data['price']:
                                await channel.send(f"{symbol}: ${data['price']:.2f}")
                            else:
                                await channel.send(f"Could not get price for {symbol}")
                        except Exception as e:
                            await channel.send(f"Error fetching data for {symbol}: {str(e)}")
                            
    #Price command, use $price and enter the stock symbol. Will return the current or latest price as well as a timestamp to when it was last updated. 
    @commands.command(name='price')
    async def price(self, ctx, symbol: str):
        '''Get current/latest price for a symbol'''
        try:
            data = self.get_price_data(symbol.upper())
            
            if data['price']:
                if data['source'] == 'real-time':
                    message = f"Current price of {symbol}: ${data['price']:.2f}"
                elif data['source'] == 'regular':
                    message = f"Regular market price of {symbol}: ${data['price']:.2f}"
                else:
                    message = f"Latest available price for {symbol}: ${data['price']:.2f} (Previous close)"
                
                #Add timestamp. 
                timestamp = data['time'].astimezone(pytz.timezone('US/Eastern'))
                message += f"\nLast updated: {timestamp.strftime('%I:%M:%S %p ET')}"
            else:
                message = f"Could not get price data for {symbol}"
            
            await ctx.send(message)
        except Exception as e:
            await ctx.send(f"Error fetching price for {symbol}: {str(e)}")

    #Watch command, use $watch to add stock(s) to watchlist. Using this would make it so that the bot returns the price of stocks in watchlist every minute
    @commands.command(name='watch')
    async def watch(self, ctx, symbol: str):
        '''Add a symbol to watch list'''
        channel_id = ctx.channel.id
        if channel_id not in watched_symbols:
            watched_symbols[channel_id] = set()
        watched_symbols[channel_id].add(symbol.upper())
        await ctx.send(f"Added {symbol} to watch list")

    #Unwatch command, use $unwatch to remove stock(s) from watchlist. 
    @commands.command(name='unwatch')
    async def unwatch(self, ctx, symbol: str):
        '''Remove a symbol from watch list'''
        channel_id = ctx.channel.id
        if channel_id in watched_symbols:
            watched_symbols[channel_id].discard(symbol.upper())
            await ctx.send(f"Removed {symbol} from watch list")

    #Watchlist command, to use $watchlist which returns the symbols of stocks that are currently being watched. Uses a dictionary.
    @commands.command(name='watchlist')
    async def watchlist(self, ctx):
        '''Show all watched symbols'''
        channel_id = ctx.channel.id
        if channel_id in watched_symbols and watched_symbols[channel_id]:
            symbols = ', '.join(watched_symbols[channel_id])
            await ctx.send(f"Currently watching: {symbols}")
        else:
            await ctx.send("No symbols in watch list")

    #Info command. Use $info along with a stock's symbol. This is used to get detailed information on a stock, including the full name of stock, summary description, current/latest price, market cap, 52 week high, and 52 week low. 
    @commands.command(name='info')
    async def info(self, ctx, symbol: str):
        '''Get detailed information about a symbol'''
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            embed = discord.Embed(
                title=f"{info.get('longName', symbol)} ({symbol})",
                description=info.get('longBusinessSummary', 'No description available')[:2048],
                color=discord.Color.blue()
            )
            
            current_price = info.get('regularMarketPrice') or info.get('previousClose')
            embed.add_field(name="Current/Latest Price", value=f"${current_price}" if current_price else "N/A")
            embed.add_field(name="Market Cap", value=f"${info.get('marketCap', 'N/A'):,}")
            embed.add_field(name="52 Week High", value=f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
            embed.add_field(name="52 Week Low", value=f"${info.get('fiftyTwoWeekLow', 'N/A')}")
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error fetching info for {symbol}: {str(e)}")

    #Commands command. Use $commands to see the list of all available commands and their description. Helps users understand what commands the bot offers and how to use them, as well as what it is helpful for. 
    @commands.command(name='commands')
    async def show_commands(self, ctx):
        '''Show all available commands'''
        embed = discord.Embed(
            title="📈 Finance Bot Commands",
            description="Here are all available commands you can use:",
            color=discord.Color.green()
        )
    
        commands_list = {
            "$price SYMBOL": "Get current/latest price for a stock (e.g., $price AAPL)",
            "$watch SYMBOL": "Add a stock to your watchlist for price updates",
            "$unwatch SYMBOL": "Remove a stock from your watchlist",
            "$watchlist": "Show all stocks you're currently watching",
            "$info SYMBOL": "Get detailed information about a stock",
            "$commands": "Show this commands list"
        }
    
        for command, description in commands_list.items():
            embed.add_field(name=command, value=description, inline=False)
    
        await ctx.send(embed=embed)
        
@bot.event
async def on_ready():
    '''Log when the bot connects to discord when it is run. Also adds the finance cog'''
    print(f'{bot.user} has connected to Discord!')
    await bot.add_cog(FinanceBot(bot))

@bot.event
async def on_command_error(ctx, error):
    '''When a command is not found'''
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found! Use `$commands` to see all available commands.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

# Run the bot!
def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()