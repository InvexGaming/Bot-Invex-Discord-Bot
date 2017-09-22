import discord
from discord.ext import commands
from random import choice as randchoice
import os

class Insult:

	'''ev0ked's Insult Cog'''

	def __init__(self,bot):
		self.bot = bot
		self.insults = open("data/insults.txt").read().splitlines()

	@commands.command(name='insult', aliases=['roast'], pass_context = True, no_pm = True)
	async def insult(self, ctx, user : discord.Member = None):
		'''Insult another user!'''

		msg = ' '
		if user != None:
			if user.id == self.bot.user.id:
				msg = " How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
				await ctx.send(user.mention + msg)
			else:
				await ctx.send(user.mention + msg + randchoice(self.insults))
		else:
			await ctx.send(ctx.message.author.mention + msg + randchoice(self.insults))

def setup(bot):
	bot.add_cog(Insult(bot))