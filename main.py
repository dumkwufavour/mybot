import discord
from discord.ext import commands
from command import setup_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')
    


# Load custom commands
setup_commands(bot)


# Error handler for command not found
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Type !help to see available commands.')
   


bot.run()
