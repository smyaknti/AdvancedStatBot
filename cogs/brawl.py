"""
Author: Soumyakanti (r.soumyakanti@outlook.com)

last edited on: 13th February, 2020
"""

import discord
from discord.ext import commands
import brawlstats
from dotenv import load_dotenv
import os
import box

#loading the tokens from environment variables
load_dotenv(dotenv_path='../.env')
token = os.getenv("TOKEN")

#lookup table for names
name_lookup = {
   'soloShowdown': 'Solo Showdown',
   'duoShowdown' : 'Duo Showdown',
   'brawlBall' : 'Brawl Ball',
   'gemGrab': 'Gem Grab',
   'heist': 'Heist',
   'seige': 'Seige',
   'bounty': 'Bounty'
}

#calculating trophy changes for the number of battles requested
def calculate_trophy_change(battles, num):
    total_change = 0
    for i in range(num):
      try:
         total_change += battles[i].battle.trophyChange
      except box.exceptions.BoxKeyError:
         pass
      except:
         print("You screwed something up son!")
    print("You overall trophy turnover:", total_change)
    return total_change

def sign(value): return ('-','+')[value >= 0]

class Brawl(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.bot_name = 'LA Advanced Stats Bot'
      self.client = brawlstats.OfficialAPI(token, is_async=True)

   @commands.command()
   async def blog(self, ctx, player_tag, num=25):
      """<Tag> <No. of Battles>"""
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('with BrawlAPI!'))
      
      if player_tag[0] == '#':
         player_tag = player_tag[1:]
      player = await self.client.get_profile(player_tag)
      name = player.name
      em = discord.Embed(color=0x00ff80)
      em.set_author(name=f'{self.bot_name}')
      em.title = f'Hey {name}!'
      battles = await self.client.get_battle_logs(player_tag)
      trophy_change = calculate_trophy_change(battles, num)
      em.set_footer(text=f'Total Trophy change was {sign(trophy_change)}{trophy_change}')
      log = ''
      for i in range(int(num)):
         if battles[i].battle.mode in set([ 'soloShowdown','duoShowdown']):
            em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= f'Rank: {battles[i].battle.rank}',inline=False)
         else :
            em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= f'Result: {battles[i].battle.result}',inline=False)
      if int(num) == 1:
         gamemode_grammar = 'played Gamemode is'
         em.description = f'Your last {gamemode_grammar}:'
         await ctx.send(embed=em)
      else:
         gamemode_grammar = 'played Gamemodes are'
         em.description = f'Your last {num} {gamemode_grammar}:'
         await ctx.send(embed=em)
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('with Statistics!'))


def setup(bot):
   bot.add_cog(Brawl(bot))  