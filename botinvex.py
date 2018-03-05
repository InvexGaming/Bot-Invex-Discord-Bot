import discord
from discord.ext import commands

import os
import sys
import traceback

# Set CWD to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Get Config
import config
config = config.GetConfig()

# Settings
INVITELINK = 'https://discordapp.com/oauth2/authorize?&client_id=' + str(config['DEFAULT']['CLIENTID']) + '&scope=bot&permissions=0'
description = """Bot Invex is a Discord bot created by Byte#0017 and ev0ked#9780."""

def get_prefix(bot, msg):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    
    prefixes = [config['DEFAULT']['PREFIX']]
    
    # Check to see if we are outside of a guild. e.g DM's etc.
    if msg.guild is None:
        # Only allow ? to be used in DMs
        return '?'

    # Allow bot mention as prefix.
    return commands.when_mentioned_or(*prefixes)(bot, msg)

# Inital Cog's to load.
initial_extensions = (
    'cogs.cogtools',
    'cogs.admincommands',
    'cogs.error_handler',
    'cogs.channelutilities', 
    'cogs.members',
    'cogs.remarks',
    'cogs.randomdiscordgames',
    'cogs.invexforumsync',
    'cogs.gametracker',
    'cogs.youtube',
)

bot = commands.Bot(command_prefix=get_prefix, description=description)


@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
	
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    
    # Inital Extention Loading.
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}. ', file=sys.stderr)
                traceback.print_exc() # Uncomment for bug reports.
    print(f'Successfully logged in and connected!')


# Welcome Message
@bot.event
async def on_member_join(member):
    invex_guild = bot.get_guild(int(config['DEFAULT']['INVEXGUILD']))
    
    if invex_guild != member.guild:
        return
    
    # Format Welcome Message
    welcome_message = config['DEFAULT']['WELCOME_MESSAGE'].format(
      name=member.display_name,
      verify_text=config['DEFAULT']['VERIFY_TEXT'],
    )
    
    await member.send(welcome_message)
    
bot.run(config['DEFAULT']['TOKEN'], bot=True, reconnect=True)