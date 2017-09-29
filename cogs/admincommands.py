import asyncio
import discord
from discord.ext import commands

from .utils import checks

"""A cog which allows owners echo text via the bot"""

class admincommands:
	"""Administrator commands (not for Forgotten)"""
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(name='echo', aliases=['e'], hidden=True)
	@checks.is_owner()
	async def echo(self, ctx):
		'''Echos input to channel from Bot'''
		message = ctx.message.content
		prefix_stripped = False
		
		if message.startswith('!echo '):
			message = message[len('!echo '):]
			prefix_stripped = True
		
		if message.startswith('?e '):
			message = message[len('?e '):]
			prefix_stripped = True
			
		if not prefix_stripped:
			await ctx.send('`You cannot echo an empty message.`')
		else:
			await ctx.message.channel.purge(limit=1)
			await ctx.send(message)

	@commands.command(hidden=True)
	#@checks.owner_or_permissions(manage_messages=True)
	@checks.is_owner()
	async def purge(self, ctx, number: int):
		'''Purge messages'''
		def is_pinned(m):
			return m.pinned == False

		await ctx.message.channel.purge(limit=(number+1), check = is_pinned)
		await ctx.send(f'`{number} messages purged!`')

	@commands.command(hidden=True)
	#@checks.owner_or_permissions(manage_messages=True)
	@checks.is_owner()
	async def purgeuser(self, ctx, user : discord.Member, number: int):
		'''Purge specific user messages'''
		def is_user(m):
			return m.author == user

		await ctx.message.channel.purge(limit=(number+1), check = is_user)
		await ctx.send(f'`{number} messages purged!`')
			
			
def setup(bot):
	bot.add_cog(admincommands(bot))