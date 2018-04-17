import discord
from discord.ext import commands

import asyncio
from random import choice

"""A cog to change the bots Discord game based on a provided predefined list."""

class RandomDiscordGame:
    """RandomDiscordGame"""

    def __init__(self, bot):
        self.discordGames = open("data/randomdiscordgames.txt").read().splitlines()
        bot.loop.create_task(self.update_discord_game(bot))

    async def update_discord_game(self, bot):
        await bot.wait_until_ready()
        while not bot.is_closed():
            await bot.change_presence(activity=discord.Game(name=choice(self.discordGames)))
            await asyncio.sleep(10*60) #10 minutes
    
def setup(bot):
    bot.add_cog(RandomDiscordGame(bot))