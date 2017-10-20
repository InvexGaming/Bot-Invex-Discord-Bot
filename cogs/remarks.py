import discord
from discord.ext import commands
from random import choice as randchoice
import os, re
from .utils import checks

class Remarks:

    '''ev0ked's Remarks Cog'''

    def __init__(self,bot):
        self.bot = bot
        self.insults = open("data/insults.txt").read().splitlines()
        self.addquote_regex = re.compile("^'.+ - .+'$", re.UNICODE)

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
        quote_list = open("data/quotes.txt").read().splitlines()
        selected_quote = randchoice(quote_list)
        selected_quote = selected_quote[1:-1]
        quote, quote_author = selected_quote.split(' - ')
        
        embed = discord.Embed(colour=discord.Colour(0xc0c0c0), title=f'"{quote}"')
        embed.set_author(name="Quotes", icon_url="https://www.invexgaming.com.au/images/discord/quote_icon_v2.png")
        embed.set_footer(text = f"-{quote_author}")
        await ctx.send(embed=embed)
    
    @commands.command(hidden=True)
    @checks.is_owner()
    async def addquote(self, ctx, *, quote : str):
        '''Add Quote to list of quotes'''
        if not self.addquote_regex.match(quote):
            await ctx.send("`Quote must be in this format (including surrounding single quotes):\n'some quote here - quote author'`")
        else:
            with open("data/quotes.txt", "a") as text_file:
                text_file.write(f"{quote}\n")
            await ctx.send('`Quote added!`')

    @addquote.error
    async def create_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("`You did not provide the '" + error.param + "' parameter.`")
            
    # GENERIC SHITTY CHAT MEMES/COMMANDS

    @commands.command()
    async def dotheroar(self,ctx):
        '''Roooooar!'''
        await ctx.send('https://giphy.com/gifs/shrek-qFsHUsuBMQemQ')

    @commands.command()
    async def panic(self,ctx):
        '''SOUND THE ALARMS!@!'''
        await ctx.send(':rotating_light: EVERYTHING IS BROKEN :rotating_light:')
        await ctx.send(':rotating_light: CALL THE COPS :rotating_light:')
        await ctx.send(':rotating_light: SHUT DOWN EVERYTHING :rotating_light:')
        await ctx.send(':rotating_light: I NEED AN ADULT :rotating_light:')

    @commands.command()
    async def n8egirl(self,ctx):
        '''Approved by n8'''
        await ctx.send(":man_in_tuxedo: n8's e-girl? What one?")
        await ctx.send(':raising_hand: Elaina?')
        await ctx.send(':raising_hand: Darcye?')
        await ctx.send(':raising_hand: Sarah?')

    @commands.command(aliases=['ree'])
    async def reeeeee(self,ctx):
        '''reeeeee!'''
        await ctx.send(file = discord.File(open("data/images/ree.gif", "rb")))

    @addquote.error
    async def generic_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("`You did not provide the '" + error.param + "' parameter.`")
def setup(bot):
    bot.add_cog(Remarks(bot))