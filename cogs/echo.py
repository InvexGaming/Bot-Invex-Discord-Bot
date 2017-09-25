import asyncio
import discord
from discord.ext import commands

from .utils import checks

"""A cog which allows owners echo text via the bot"""

class echo:
	"""Echo Cog"""
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(name='echo', aliases=['e'], hidden=True)
	@checks.is_owner()
	async def echo(self, ctx):
		message = ctx.message.content
		prefix_stripped = False
		
		if message.startswith('!echo '):
			message = message[len('!echo '):]
			prefix_stripped = True
		
		if message.startswith('!e '):
			message = message[len('!e '):]
			prefix_stripped = True
			
		if not prefix_stripped:
			await ctx.send('`You cannot echo an empty message.`')
		else:
			await ctx.send(message)
			
			
def setup(bot):
	bot.add_cog(echo(bot))