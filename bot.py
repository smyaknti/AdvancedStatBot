"""
Author: Soumyakanti (r.soumyakanti@outlook.com)

last edited on: 16th February, 2020
"""

import discord
from discord.ext import commands
import os
import time
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("DISCORD")
command_prefix = ','
bot = commands.Bot(command_prefix=command_prefix)
bot.remove_command('help')
bot_name = 'LA Advanced Stats Bot'

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

@bot.command()
async def help(ctx):
   author = ctx.author
   em = discord.Embed(colour = discord.Colour.gold())
   em.set_author(name=f'{bot_name}', icon_url="https://cdn.discordapp.com/emojis/664337403716173835.gif")
   em.add_field(name=f'1. **{command_prefix}ping**', value="Pings you back with latency!", inline=False)
   em.add_field(name=f'2. **{command_prefix}blog** <Player Tag> <Number of Battles(max 25)>', value="Sends your comprehensive battle logs.", inline=False)
   em.add_field(name=f'3. **{command_prefix}3v3** <Player Tag> <Number of battles to consider>', value="Sends the detailed analysis of friendly 3v3 matches played.", inline=False)
   await ctx.send(embed=em)

#load all py files as a cog
for filename in os.listdir('./cogs'):
   if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(discord_token)