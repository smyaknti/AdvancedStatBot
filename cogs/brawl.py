"""
Author: Soumyakanti (r.soumyakanti@outlook.com)

last edited on: 15th February, 2020
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

#lookup table
name_lookup = {
   'soloShowdown': 'Solo Showdown',
   'duoShowdown' : 'Duo Showdown',
   'brawlBall' : 'Brawl Ball',
   'gemGrab': 'Gem Grab',
   'heist': 'Heist',
   'seige': 'Seige',
   'bounty': 'Bounty',
   'bigGame': 'Big Game',
   'roboRumble':'Robo Rumble',
   'bossFight':'Boss Fight'
}
soloPP = {
   1:38,
   2:34,
   3:30,
   4:26,
   5:22,
   6:18,
   7:14,
   8:10,
   9:6,
   10:2
}

duoPP = {
   1:34,
   2:26,
   3:18,
   4:10,
   5:2
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
    return total_change

#function to check if a match is a powerplay game
def is_powerplay(battle):
   try:
      if battle.battle.mode == 'soloShowdown':
         if soloPP[battle.battle.rank] == battle.battle.trophyChange:
            return True
         else: return False
      elif battle.battle.mode == 'duoShowdown':
         if duoPP[battle.battle.rank] == battle.battle.trophyChange:
            return True
         else: return False
      else:
         if battle.battle.trophyChange > 8:
            return True
         else:
            if battle.battle.result == 'defeat' and battle.battle.trophyChange > 0:
               return True
            else: return False
   except box.exceptions.BoxKeyError:
      pass


#Function to get the brawler played in a match
def get_brawler_played(battle, player_tag): 
   player_tag = '#'+player_tag.upper()
   if battle.mode in set([ 'bigGame','roboRumble']):
      return None
   elif battle.mode == 'soloShowdown':
        for i in range (10):
           if battle.players[i].tag == player_tag:
              return battle.players[i].brawler
   elif battle.mode == 'duoShowdown':
      for i in range (5):
         for j in range(2):
           if battle.teams[i][j].tag == player_tag:
              return battle.teams[i][j].brawler
   else: 
      for i in range(2):
         for j in range(3):
            if battle.teams[i][j].tag == player_tag:
               return battle.teams[i][j].brawler


def sign(value): return ('-','+')[value >= 0]

class Brawl(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.bot_name = 'LA Advanced Stats Bot'

   @commands.command()
   async def blog(self, ctx, player_tag, num=25):
      """<Tag> <No. of Battles>"""
      await ctx.trigger_typing()
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Brawl Stars servers"))
      if num > 25:
         em = discord.Embed(colour = discord.Colour.gold())
         em.set_author(name=f'{self.bot_name}', icon_url="https://cdn.discordapp.com/emojis/664337403716173835.gif")
         em.add_field(name=f'Wrong Input!', value=f'Sir, there aren\'t {num} battles in your log. Choose a number upto 25.', inline=False)
         await ctx.send(embed=em)
      else:
         brawler_trophy_change = {}
         if player_tag[0] == '#':
            player_tag = player_tag[1:]
         client = brawlstats.BrawlAPI(token, is_async=True)
         player = await client.get_profile(player_tag)
         
         power_play_points = player.powerPlayPoints
         name = player.name
         
         em = discord.Embed(color=0x00ff80)
         em.set_author(name=f'{self.bot_name}',icon_url='https://cdn.discordapp.com/emojis/664337403716173835.gif' )
         em.title = f'Hey {name}!'
      
         battles = await client.get_battle_logs(player_tag)
         trophy_change = calculate_trophy_change(battles, num)
         log = ''
         
         for i in range(int(num)):
            brawler = get_brawler_played(battles[i].battle,player_tag)
            powerPlay = is_powerplay(battles[i])
            if battles[i].battle.mode in set([ 'bigGame','roboRumble']):
               em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= 'Ticketed Events aren\'t competetive',inline=False)
            elif battles[i].battle.mode in set([ 'soloShowdown','duoShowdown']):
               if battles[i].battle.type == 'ranked' and brawler != None:
                  if powerPlay:
                     brawler_details = f'{brawler.name}\nPower Play Game at {brawler.trophies} points.'
                  else:
                     brawler_details = f'{brawler.name} ({brawler.trophies})'
               elif brawler != None:
                  brawler_details = f'{brawler.name} (Friendly)'
               try:
                  em.add_field(name = f'{i+1}. **{name_lookup[battles[i].battle.mode]}**, {brawler_details}', value= f'Rank: {battles[i].battle.rank} ({sign(battles[i].battle.trophyChange)}{abs(battles[i].battle.trophyChange)})',inline=False)
                  if powerPlay:
                     if 'POWER-PLAY Points' in brawler_trophy_change:
                        brawler_trophy_change['POWER-PLAY Points']+=battles[i].battle.trophyChange
                     else:
                        brawler_trophy_change['POWER-PLAY Points']=battles[i].battle.trophyChange
                  else:
                     if brawler.name in brawler_trophy_change:
                        brawler_trophy_change[brawler.name]+=battles[i].battle.trophyChange
                     else:
                        brawler_trophy_change[brawler.name]=battles[i].battle.trophyChange
               except box.exceptions.BoxKeyError:
                  em.add_field(name = f'{i+1}. **{name_lookup[battles[i].battle.mode]}**, {brawler_details}', value= f'Rank: {battles[i].battle.rank} (+0)',inline=False)
            else :
               if battles[i].battle.type == 'ranked' and brawler != None:
                  if powerPlay:
                     brawler_details = f'{brawler.name}\nPower Play Game at {brawler.trophies} points.'
                  else:
                     brawler_details = f'{brawler.name} ({brawler.trophies})'
               elif brawler != None:
                  brawler_details = f'{brawler.name} (Friendly)' 
               try:
                  em.add_field(name = f'{i+1}. **{name_lookup[battles[i].battle.mode]}**, {brawler_details}', value= f'Result: {battles[i].battle.result} ({sign(battles[i].battle.trophyChange)}{abs(battles[i].battle.trophyChange)})',inline=False)
                  if powerPlay:
                     if 'POWER-PLAY Points' in brawler_trophy_change:
                        brawler_trophy_change['POWER-PLAY Points']+=battles[i].battle.trophyChange
                     else:
                        brawler_trophy_change['POWER-PLAY Points']=battles[i].battle.trophyChange
                  else:
                     if brawler.name in brawler_trophy_change:
                        brawler_trophy_change[brawler.name]+=battles[i].battle.trophyChange
                     else:
                        brawler_trophy_change[brawler.name]=battles[i].battle.trophyChange
               except box.exceptions.BoxKeyError:
                  em.add_field(name = f'{i+1}. **{name_lookup[battles[i].battle.mode]}**, {brawler_details}', value= f'Result: {battles[i].battle.result}',inline=False)
         if int(num) == 1:
            gamemode_grammar = 'played Gamemode is'
            em.description = f'Your last {gamemode_grammar}:'
            
         else:
            gamemode_grammar = 'played Gamemodes are'
            em.description = f'Your last {num} {gamemode_grammar}:'
         brawler_trophy_changes = ''
         for key, value in brawler_trophy_change.items():
            brawler_trophy_changes += f'{key} : {sign(value)}{abs(value)} \n'

         if 'POWER-PLAY Points' in brawler_trophy_change:
            deduct_from_total = brawler_trophy_change['POWER-PLAY Points']
         else: deduct_from_total = 0
         em.set_footer(text=f'Total Trophy change was {sign(trophy_change)}{abs(trophy_change-deduct_from_total)}\n{brawler_trophy_changes}', icon_url="https://icons8.com/vue-static/landings/animated-icons/icons/rhombus/rhombus.gif")
         await ctx.send(embed=em)
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="bot calls!"))
      


def setup(bot):
   bot.add_cog(Brawl(bot))  
