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
		
		if message.startswith('?echo '):
			message = message[len('?echo '):]
			prefix_stripped = True
		
		if message.startswith('?e '):
			message = message[len('?e '):]
			prefix_stripped = True
			
		if not prefix_stripped:
			await ctx.send('`You cannot echo an empty message.`')
		else:
			await ctx.send('`Enter a channel id`')
			chanid = await self.bot.wait_for('message')
			channel = ctx.guild.get_channel(int(chanid.content))
			await channel.send(message)

	@commands.command(aliases = ['eh'])
	@checks.is_owner()
	async def echohere(self, ctx):
		message = ctx.message.content
		prefix_stripped = False
		
		if message.startswith('?echohere '):
			message = message[len('?echohere '):]
			prefix_stripped = True
		
		if message.startswith('?eh '):
			message = message[len('?eh '):]
			prefix_stripped = True
			
		if not prefix_stripped:
			await ctx.send('`You cannot echo an empty message.`')
		else:
			await ctx.message.channel.purge(limit=1)
			await ctx.send(message)

	

	@commands.command(hidden=True)
	@checks.is_owner()
	async def purge(self, ctx, number: int):
		'''Purge messages'''
		await ctx.message.channel.purge(limit=(number+1))
		await ctx.send(f'`{number} messages purged!`')

	@commands.command(hidden=True)
	@checks.is_owner()
	async def purgeuser(self, ctx, user : discord.Member, number: int):
		'''Purge messages'''
		def is_user(m):
			return m.author == user

		await ctx.message.channel.purge(limit=(number+1), check = is_user)
		await ctx.send(f'`{number} messages purged!`')
			
			
def setup(bot):
	bot.add_cog(echo(bot))