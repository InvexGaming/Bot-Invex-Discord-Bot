import discord
from discord.ext import commands
from random import choice as randchoice
import os
from .utils import checks

class Remarks:

	'''ev0ked's Remarks Cog'''

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

	@commands.command(name='quote', pass_context = True, no_pm = True)
	async def quote(self, ctx):
		'''List a Quote!'''
		quotes = open("data/quotes.txt").read().splitlines()
		await ctx.send(randchoice(quotes))
	
	@commands.command(aliases =['addquote'])
	@checks.is_owner()
	async def addQuote(self, ctx):
		
		message = ctx.message.content
		prefix_stripped = False
		
		if message.startswith('?addquote '):
			message = message[len('?addquote '):]
			prefix_stripped = True

		if not prefix_stripped:
			await ctx.send('`You cannot quote an empty message.`')
		else:
			with open("data/quotes.txt", "a") as text_file:
				text_file.write(f"'{message}'\n")
			await ctx.send('`Quote added!`')

	'''GENERIC SHITTY CHAT MEMES/COMMANDS'''

	@commands.command()
	async def dotheroar(self,ctx):
		await ctx.send('https://giphy.com/gifs/shrek-qFsHUsuBMQemQ')

	@commands.command()
	async def panic(self,ctx):
		await ctx.send(':rotating_light: EVERYTHING IS BROKEN :rotating_light:')
		await ctx.send(':rotating_light: CALL THE COPS :rotating_light:')
		await ctx.send(':rotating_light: SHUT DOWN EVERYTHING :rotating_light:')
		await ctx.send(':rotating_light: I NEED AN ADULT :rotating_light:')

def setup(bot):
	bot.add_cog(Remarks(bot))