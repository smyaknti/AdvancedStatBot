import discord
from discord.ext import commands
import brawlstats
from dotenv import load_dotenv
import os
import box

load_dotenv()
token = os.getenv("TOKEN")

name_lookup = {
   'soloShowdown': 'Solo Showdown',
   'duoShowdown' : 'Duo Showdown',
   'brawlBall' : 'Brawl Ball',
   'gemGrab': 'Gem Grab',
   'heist': 'Heist',
   'siege': 'Siege',
   'bounty': 'Bounty',
   'bigGame': 'Big Game',
   'roboRumble':'Robo Rumble',
   'bossFight':'Boss Fight'
}

#function to obtain all the players in a 3v3 match
def get_all_players(battle, player_tag):
   teams = ''
   for i in range(2):
      teams +=f'**Team {i+1}:**\n'
      for j in range(3):
         teams +=f'> **{battle.teams[i][j].name}**({battle.teams[i][j].tag})[{battle.teams[i][j].brawler.name}]\n'
   return teams


#function to obtain a team from the battle
def get_team(battle, player_tag, team_number):
   team = ''
   for j in range(3):
      team +=f'**{battle.teams[team_number][j].name}**'
      if j != 2:
         team += '|'
   return team

#function to obtain the team the player played on
def get_team_played(battle, player_tag): 
   player_tag = '#'+player_tag.upper()
   for i in range(2):
      for j in range(3):
         if battle.teams[i][j].tag == player_tag:
            return i

#function to obtain the showdown ranks (duo and solo) as a string formatted for discord
def get_showdown_ranks(battle):
   rank_list = ''
   if battle.mode == 'soloShowdown':
      rank_list += '**Ranks:**\n'
      for i in range (10):
         rank_list += f'> {i+1}:  **{battle.players[i].name}**({battle.players[i].tag}) [{battle.players[i].brawler.name}]\n'
      return rank_list
   elif battle.mode == 'duoShowdown':
      for i in range (5):
         rank_list += f'**Rank {i+1}**\n> **{battle.teams[i][0].name}**({battle.teams[i][0].tag}) [{battle.teams[i][0].brawler.name}]\n> **{battle.teams[i][1].name}**({battle.teams[i][1].tag}) [{battle.teams[i][1].brawler.name}]\n'
      return rank_list


class Tourney(commands.Cog):

   def __init__(self, bot):
      self.bot = bot
      self.bot_name = 'LA Advanced Stats Bot'

   @commands.command(aliases=['3v3'])
   async def threevthree(self, ctx, player_tag=None, num=25): #obtains 3v3 friendly logs
      """<Tag> <No. of Battles>"""
      await ctx.trigger_typing()
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Brawl Stars servers"))
      if player_tag == None:
         em = discord.Embed(colour = discord.Colour.gold())
         em.set_author(name=f'{self.bot_name}', icon_url="https://cdn.discordapp.com/emojis/664337403716173835.gif")
         em.add_field(name=f'Wrong Input!', value=f'Sir, enter at least one player\'s Tag!', inline=False)
         await ctx.send(embed=em)
      elif player_tag[0] == '#':
         player_tag = player_tag[1:]
      client = brawlstats.BrawlAPI(token, is_async=True)
      player = await client.get_profile(player_tag)
      name = player.name

      em = discord.Embed(color=0x00ff80)
      em.set_author(name=f'{self.bot_name}', icon_url="https://cdn.discordapp.com/emojis/664337403716173835.gif")
      em.title = f'Hey {name}(#{player_tag.upper()})!'
     
      battles = await client.get_battle_logs(player_tag)
      log,wins,losses,draws = '',0,0,0
      
      for i in range(int(num)):
         
         if battles[i].battle.mode in set([ 'bigGame','roboRumble']):
            em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= 'Ticketed Events aren\'t competetive',inline=False)
         elif battles[i].battle.type == 'ranked':
               team_details = f'This was a ranked match and won\'t be considered!'
               em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= f'{team_details}',inline=False)               
         elif battles[i].battle.mode in set([ 'soloShowdown','duoShowdown']):
               team_details = f'Use the showdown command instead of 3v3 for this!'  #use showdown
               em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= f'{team_details}',inline=False)   
         else :
            team = get_team_played(battles[i].battle,player_tag)
            teams = get_all_players(battles[i].battle,player_tag)

            if battles[i].battle.result == 'victory':
               wins += 1
               winning_team = f'Winners: {get_team(battles[i].battle,player_tag,team)}'
            elif battles[i].battle.result == 'defeat':
               losses += 1
               winning_team = f'Winners: {get_team(battles[i].battle,player_tag,not team)}'
            elif battles[i].battle.result == 'draw':
               draws += 1
               winning_team = f'**It was a Draw!**'

            
            em.add_field(name = f'**{i+1}. {name_lookup[battles[i].battle.mode]}**', value= f'{teams} {winning_team}',inline=False)
      if int(num) == 1:
         gamemode_grammar = 'Game'
         em.description = f'In the last {gamemode_grammar}:'
         
      else:
         gamemode_grammar = 'Games'
         em.description = f'In the last {num} {gamemode_grammar}:'

      em.set_footer(text=f'Statistics: {wins} wins, {losses} losses and {draws} draws!',icon_url='https://icons8.com/vue-static/landings/animated-icons/icons/rhombus/rhombus.gif')
      await ctx.send(embed=em)
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="bot calls!"))



   @commands.command(aliases=['sd'])
   async def showdown(self, ctx, player_tag=None, num=25): #obtains showdown ranks for friendlies
      """<Tag> <No. of Battles>"""
      await ctx.trigger_typing()
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Brawl Stars servers"))
      if player_tag == None:
         em = discord.Embed(colour = discord.Colour.gold())
         em.set_author(name=f'{self.bot_name}', icon_url="https://cdn.discordapp.com/emojis/664337403716173835.gif")
         em.add_field(name=f'Wrong Input!', value=f'Sir, enter at least one player\'s Tag!', inline=False)
         await ctx.send(embed=em)
      elif player_tag[0] == '#':
         player_tag = player_tag[1:]
      client = brawlstats.BrawlAPI(token, is_async=True)
      player = await client.get_profile(player_tag)
      name = player.name

      em = discord.Embed(color=0x00ff80)
      em.set_author(name=f'{self.bot_name}', icon_url="https://cdn.discordapp.com/emojis/664337403716173835.gif")
      em.title = f'Hey {name}(#{player_tag.upper()})!'
     
      battles = await client.get_battle_logs(player_tag)
      log = ''
      
      for i in range(int(num)):
         
         if battles[i].battle.mode in set([ 'bigGame','roboRumble']):
            em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= 'Ticketed Events aren\'t competetive',inline=False)
         elif battles[i].battle.type == 'ranked':
            team_details = f'This was a ranked match and won\'t be considered!'
            em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= f'{team_details}',inline=False)               
         elif battles[i].battle.mode in set([ 'soloShowdown','duoShowdown']):
            ranks = get_showdown_ranks(battles[i].battle)
            em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= f'{ranks}',inline=False)   
         else :
            team_details = f'Use the 3v3 command instead of sd for this!'  #use showdown
            em.add_field(name = f'{i+1}. {name_lookup[battles[i].battle.mode]}', value= f'{team_details}',inline=False)
      if int(num) == 1:
         gamemode_grammar = 'Game'
         em.description = f'In the last {gamemode_grammar}:'
         
      else:
         gamemode_grammar = 'Games'
         em.description = f'In the last {num} {gamemode_grammar}:'

      em.set_footer(text=f'The shodown ranks are given as above.',icon_url='https://icons8.com/vue-static/landings/animated-icons/icons/rhombus/rhombus.gif')
      await ctx.send(embed=em)
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="bot calls!"))

def setup(bot):
   bot.add_cog(Tourney(bot))