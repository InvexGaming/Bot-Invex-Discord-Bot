import discord
from discord.ext import commands

import os, sys, traceback

# Set CWD to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get Config
import config
config = config.GetConfig()

# Settings
INVITELINK = 'https://discordapp.com/oauth2/authorize?&client_id=' + str(config['DEFAULT']['CLIENTID']) + '&scope=bot&permissions=0'
description = '''Bot Invex is a Discord bot created by Byte#5322 and ev0ked#9780.'''

def get_prefix(bot, msg):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    
    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = [config['DEFAULT']['PREFIX']]
    
    # Check to see if we are outside of a guild. e.g DM's etc.
    if msg.guild.id is None:
        # Only allow ? to be used in DMs
        return '?'

    #allows bot mention as prefix
    return commands.when_mentioned_or(*prefixes)(bot, msg)

#inital Cog's Load
initial_extensions =('cogs.cogtools',
                     'cogs.admincommands',
                     'cogs.error_handler',
                     'cogs.channelUtilities', 
                     'cogs.members',
                     'cogs.remarks',
                     'cogs.randomdiscordgames',
                     'cogs.invexforumsync')
                      
bot = commands.Bot(command_prefix=get_prefix, description=description)


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
	
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    #Inital Extention Loading
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}. ', file=sys.stderr)
                traceback.print_exc() #uncomment for bug reports
    print(f'Successfully logged in and connected!')

    
bot.run(config['DEFAULT']['TOKEN'], bot=True, reconnect=True)