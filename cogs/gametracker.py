import discord
from discord.ext import commands

import requests
from lxml import html
from random import choice as randchoice
from .utils import checks

class GameTracker:
    '''GameTracker cog to keep track of server status'''
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def servers(self,ctx):
        '''List Invex Gaming Servers status'''
        page = requests.get('https://www.invexgaming.com.au/serverlist.php')
        tree = html.fromstring(page.content)
        
        for i in range(1,4):
            servername = tree.xpath(f'//*[@id="serversboard_e"]/tr[{i}]/td[4]/span/a/text()')
            serverip = tree.xpath(f'//*[@id="serversboard_e"]/tr[{i}]/td[5]/span/text()')
            players = tree.xpath(f'//*[@id="serversboard_e"]/tr[{i}]/td[6]/span/div/div/div[2]/center/text()')
            servermap = tree.xpath(f'//*[@id="serversboard_e"]/tr[{i}]/td[7]/span/text()')

            player = players[0]

            embed = discord.Embed(colour=discord.Colour(0xa31e13), description=f"**IP:** {serverip[0]}\n**Players:** {player[4:9]}\n**Map:** {servermap[0]}\n\n[**Connect**](steam://connect/{serverip[0]})")
            embed.set_author(name=servername[0], icon_url="https://www.invexgaming.com.au/images/logo/logo_outline_small.png")
            embed.set_footer(text="Invex Gaming Australia")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GameTracker(bot))


