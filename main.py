import discord
from discord.ext import commands
import random
import os
from database_access import Student,wallStreet,coin

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)



description = '''Welcome to your virtual brokerage account!'''

intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='$', description=description, intents=intents, help_command=help_command)

bot.help_command = MyNewHelp()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping(ctx):
    """Pong"""
    await ctx.send(":ping_pong: ")
    print ("user has pinged")

class WallStreet(commands.Cog):
    """Commands for the stonks bot!"""
    
    @commands.command()
    async def port(self,ctx):
        """See your portfolio."""
        trader = Student(ctx.message.author.id, ctx.message.author.name)
        file = discord.File(trader.getImage()) 
        await ctx.send(file = file)

    @commands.command()
    async def screener(self,ctx):
        """Show online resources for stocks available"""
        if ctx.invoked_subcommand is None:
            await ctx.send("https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/")
    
    @commands.command()
    async def market(self,ctx, ticker:str):# added command for $market <ticker> to see current price
        """Shows current price of stock\n For Crypto use \"-USD\" after ticker"""
        if "-" in ticker:
            stock = coin(ticker.split("-")[0]+"-USD",1)
            if stock.getVerify():
                if ctx.invoked_subcommand is None:
                    embedVar = discord.Embed(title=stock.getInfo()['shortName'], color=0x0000ff, description="Price: $"+ 
                                            str(stock.getInfo()['regularMarketPrice']))
                    await ctx.send(embed = embedVar)
            else:
                if ctx.invoked_subcommand is None:
                    await ctx.send("Yahoo does not recognize that coin symbol. \n For stocks use \"$market {0}\" instead".format(ticker.split("-")[0]))
        else:
            stock = wallStreet(ticker, 1)
            if stock.getVerify():
                if('BUY' not in stock.getInfo()['recommendationKey'].upper()):
                    color = 0xff0000
                else:
                    color = 0x00ff00
                if ctx.invoked_subcommand is None:
                    embedVar = discord.Embed(title=stock.getInfo()['shortName'], color=color, description="Price: $"+ 
                                            str(stock.getInfo()['currentPrice'])+"\nRecommendation: " +stock.getInfo()['recommendationKey'].upper())
                    await ctx.send(embed = embedVar)
            else:
                if ctx.invoked_subcommand is None:
                    await ctx.send("Yahoo does not recognize that ticker symbol. \n For Coins use \"$market {0}-USD\" instead".format(ticker))

    @commands.command()
    async def buy(self,ctx, ticker:str, shares:int):
        """Buy shares in a stock.
            insert amount of shares and ticker symbol\nEx: $buy 10 TSLA
        """
        ticker = ticker.upper()
        trader = Student(ctx.message.author.id, ctx.message.author.name)
        if "-" in ticker:
            stock = coin(ticker.split("-")[0]+"-USD", shares)
        else:
            stock = wallStreet(ticker, shares)
        
        if(stock.getVerify()):
            if(stock.getTotal() > trader.getBalance()):
                if ctx.invoked_subcommand is None:
                    await ctx.send(ctx.message.author.name+" you only have a balance of "+str(trader.getBalance())+ " you need "+ 
                                    str(stock.getTotal() - trader.getBalance()))
            else:
                trader.buy(stock)
                if ctx.invoked_subcommand is None:
                    await ctx.send(ctx.message.author.name+" bought "+str(shares)+" shares of "+ticker+" at $"+str(stock.getPrice())+
                                    " for $" + str(stock.getTotal()))
        else:
            if ctx.invoked_subcommand is None:
                embedVar = discord.Embed(title="Try entering a real stock symbol buddy...", color=0xff0000)
                embedVar.set_image(url="https://media1.tenor.com/images/e74f1e9fbe531e208fd18b8ff6170dd3/tenor.gif")
                await ctx.send(embed = embedVar)
    @commands.command()
    async def sellAll(self, ctx):# command for selling everything in portfolio
        """Sell all shares in your portfolio.
            \nEx: $sellAll
        """
        trader = Student(ctx.message.author.id, ctx.message.author.name)
        trader.sellAll()
        if ctx.invoked_subcommand is None:
            await ctx.send(ctx.message.author.name+" sold all their shares!")

        
    @commands.command()
    async def sell(self, ctx, ticker:str, shares:int):
        """Sell shares in your portfolio.
            insert amount of shares and ticker symbol\nEx: $buy 10 TSLA
        """
        ticker = ticker.upper()
        trader = Student(ctx.message.author.id, ctx.message.author.name)
        if "-USD" in ticker:
            stock = coin(ticker.split("-")[0]+"-USD", shares)
        else:
            stock = wallStreet(ticker, shares)
        if(ticker in trader.getPort()):
            if(trader.getPort()[ticker] < shares):
                if ctx.invoked_subcommand is None:
                    await ctx.send(ctx.message.author.name+" you only have "+str(trader.getPort()[ticker])+ " shares of "+
                    ticker + ". BUY MORE!")
            else:
                trader.sell(stock)
                if ctx.invoked_subcommand is None:
                    await ctx.send(ctx.message.author.name+" sold "+str(shares)+" shares of "+ticker+" at $"+str(stock.getPrice())+
                                    " for $" + str(stock.getTotal()))
        else:
            if ctx.invoked_subcommand is None:
                embedVar = discord.Embed(title="Yahoo does not recognize that ticker symbol", color=0xff0000)
                await ctx.send(embed = embedVar)



bot.add_cog(WallStreet())

bot.run('WEBHOOK_GOES_IN_THIS_SECTION')



