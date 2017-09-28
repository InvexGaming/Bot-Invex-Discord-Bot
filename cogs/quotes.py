import discord
from discord.ext import commands
from random import choice as randchoice
import os

class Quotes:

	'''ev0ked's Quotes Cog'''

	def __init__(self,bot):
		self.bot = bot
		self.quotes = open("data/quotes.txt").read().splitlines()

	@commands.command(name='quote', pass_context = True, no_pm = True)
	async def quote(self, ctx):
		'''Insult another user!'''
		await ctx.send(ctx.message.author.mention + ' ' + randchoice(self.quotes))

def setup(bot):
	bot.add_cog(Quotes(bot))