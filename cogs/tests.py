"""
Author: Soumyakanti (r.soumyakanti@outlook.com)

Last edited: 16th February, 2020
"""

import discord
from discord.ext import commands


class Tests(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.bot_name = 'LA Advanced Stats Bot'

   @commands.command()
   async def test(self,ctx):
      """Sends a reply!"""
      await ctx.trigger_typing()
      em = discord.Embed(color=discord.Colour.dark_green())
      em.set_author(name=f'{self.bot_name}', icon_url="https://cdn.discordapp.com/emojis/664337403716173835.gif")
      em.set_footer(text = 'Testing succesful!',icon_url="https://icons8.com/vue-static/landings/animated-icons/icons/checkmark-ok/checkmark-ok.gif")
      await ctx.send(embed=em)


   @commands.command()
   async def ping(self, ctx):
      """Pings you back!"""
      await ctx.trigger_typing()
      em = discord.Embed(color=discord.Colour.dark_green())
      em.set_author(name=f'{self.bot_name}', icon_url="https://cdn.discordapp.com/emojis/664337403716173835.gif")
      em.set_footer(text =f'Pong!\nYou are {round(self.bot.latency*1000)}ms away from me!', icon_url="https://icons8.com/vue-static/landings/animated-icons/icons/hourglass/hourglass.gif")
      await ctx.send(embed=em)
      
def setup(bot):
   bot.add_cog(Tests(bot))