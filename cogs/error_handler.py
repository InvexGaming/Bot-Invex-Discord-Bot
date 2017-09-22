import traceback
import sys
from discord.ext import commands
import discord


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                return await ctx.send('I could not find that member. Please try again.')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    @commands.command(name='repeat', aliases=['mimic', 'copy'])
    async def do_repeat(self, ctx, *, inp: str):
        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param == 'inp':
                await ctx.send("You forgot to give me input to repeat!")
                

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))