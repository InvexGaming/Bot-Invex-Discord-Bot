import discord
from discord.ext import commands

import asyncio
from .utils import checks

# Get Config
import config
config = config.GetConfig()

"""A cog which allows owners echo text via the bot"""

class admincommands:
    """Administrator commands (not for Forgotten)"""
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='echo', aliases=['e'], hidden=True)
    @checks.is_owner()
    async def echo(self, ctx, *, input : str):
        await ctx.send(input)
        await ctx.message.delete()

    @echo.error
    async def echo_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param == 'input':
                await ctx.send("`You cannot echo an empty message.`")

    @commands.command(hidden=True)
    @checks.is_owner()
    async def purge(self, ctx, number: int):
        """Purge messages"""
        def is_pinned(m):
            return m.pinned == False

        await ctx.message.channel.purge(limit=(number+1), check=is_pinned)
        await ctx.send(f'`{number} messages purged!`')

    @commands.command(hidden=True)
    @checks.is_owner()
    async def purgeuser(self, ctx, user : discord.Member, number: int):
        """Purge specific user messages"""
        def is_user(m):
            return m.author == user

        await ctx.message.channel.purge(limit=(number+1), check=is_user)
        await ctx.send(f'`{number} messages purged!`')

    
    @commands.command(hidden=True)
    @checks.is_owner()
    async def root(self, ctx):
        invex_guild = self.bot.get_guild(int(config['DEFAULT']['INVEXGUILD']))
        root_role = discord.utils.get(invex_guild.roles, name='Root Permissions')
        
        if root_role in ctx.author.roles:
            await ctx.send(ctx.author.mention + " `You already have root permissions.`")
        else:
            await ctx.author.add_roles(root_role)
            await ctx.send(ctx.author.mention + " `Root permissions added and will be automatically removed in 15 minutes.`")
            await asyncio.sleep(15*60) #15 minutes
            if root_role in ctx.author.roles:
                await ctx.author.remove_roles(root_role)
                await ctx.send(ctx.author.mention + " `Your root permissions were removed.`")
    
    @commands.command(hidden=True)
    @checks.is_owner()
    async def unroot(self, ctx):
        invex_guild = self.bot.get_guild(int(config['DEFAULT']['INVEXGUILD']))
        root_role = discord.utils.get(invex_guild.roles, name='Root Permissions')
        
        if root_role in ctx.author.roles:
            await ctx.author.remove_roles(root_role)
            await ctx.send(ctx.author.mention + " `Your root permissions were removed.`")
        else:
            await ctx.send(ctx.author.mention + " `You do not currently have root permissions.`")
    
    @purge.error
    @purgeuser.error
    async def generic_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("`You did not provide the '" + error.param + "' parameter.`")
        
def setup(bot):
    bot.add_cog(admincommands(bot))