import discord
import random
from discord.ext import commands
import asyncio

"""A cog to change the bots Discord game based on a provided predefined list."""

class RandomDiscordGame:
	"""RandomDiscordGame"""

	def __init__(self, bot):
		self.discordGames = open("data/randomdiscordgames.txt").read().splitlines()
		bot.loop.create_task(self.updateDiscordGame(bot))

	async def updateDiscordGame(self, bot):
		await bot.wait_until_ready()
		while not bot.is_closed():
			randIndex = random.randint(0, len(self.discordGames) - 1)
			await bot.change_presence(game=discord.Game(name=self.discordGames[randIndex]))
			await asyncio.sleep(60*10) #10 minutes
	
def setup(bot):
	bot.add_cog(RandomDiscordGame(bot))