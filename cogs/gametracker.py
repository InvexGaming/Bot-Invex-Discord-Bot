import discord
from discord.ext import commands

import asyncio
import requests
from datetime import datetime, timezone
from lxml import html
from .utils import checks

# Get Config
import config
config = config.GetConfig()

class GameTracker:
    """GameTracker cog to keep track of server status"""
    
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.update_servers(bot))

    async def update_servers(self, bot):
        await bot.wait_until_ready()
        
        # Get Invex Guild and server status channel
        invex_guild = bot.get_guild(int(config['DEFAULT']['INVEXGUILD']))
        serverstatus_channel = invex_guild.get_channel(int(config['GAMETRACKER']['SERVERSTATUS_CHANNEL_ID']))
        
        while not bot.is_closed():
            # Delete all current messages
            await serverstatus_channel.purge(limit=100)
            
            # Output embed
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
                embed.set_footer(text="Invex Gaming")
                await serverstatus_channel.send(embed=embed)
            
            # Print out empty line (acts as separator)
            await serverstatus_channel.send('\uFEFF')
            
            # Print out time of update
            post_time = datetime.utcnow()
            post_time = post_time.replace(tzinfo=timezone.utc).astimezone(tz=None) # convert from UTC to local
            post_time_str = post_time.strftime('%A %d %B %Y at %I:%M:%S %p')
            await serverstatus_channel.send(f'Last Updated: `{post_time_str}`')
            
            await asyncio.sleep(5*60) #5 minutes

def setup(bot):
    bot.add_cog(GameTracker(bot))
