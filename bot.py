"""
Author: Soumyakanti (r.soumyakanti@outlook.com)

last edited on: 15th February, 2020
"""

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import time

#loading tokens from environment variables
load_dotenv(dotenv_path='.env')
discord = os.getenv("DISCORD")

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
   await bot.change_presence(status=discord.Status.online, activity=discord.Game("with Statistics!"))
   print('Bot is alive!!!')

@bot.command()
async def load(ctx, extension):
   bot.load_extension(f'cogs.{extension}')
   await ctx.send(f'{extension} cog is loaded!')

@bot.command()
async def unload(ctx, extension):
   bot.unload_extension(f'cogs.{extension}')
   await ctx.send(f'{extension} cog was unloaded!')

@bot.command()
async def reload(ctx, extension):
   bot.unload_extension(f'cogs.{extension}')
   time.sleep(0.1)
   bot.load_extension(f'cogs.{extension}')
   await ctx.send(f'{extension} cog got reloaded!')


#load all py files as a cog
for filename in os.listdir('./cogs'):
   if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(discord)