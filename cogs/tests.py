"""
Author: Soumyakanti (r.soumyakanti@outlook.com)

Last edited: 13th February, 2020
"""


import discord
from discord.ext import commands


class Tests(commands.Cog):

   def __init__(self, bot):
      self.bot = bot

   @commands.command()
   async def test(self,ctx):
      """Sends a reply!"""
      await ctx.send('Testing succesful!')

   @commands.command()
   async def ping(self, ctx):
      """Pings you back!"""
      await ctx.send(f'Pong!\nYou are {round(self.bot.latency*1000)}ms away from me!')

def setup(bot):
   bot.add_cog(Tests(bot))