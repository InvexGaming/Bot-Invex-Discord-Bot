import asyncio
import discord
from discord.ext import commands

import re, datetime
from collections import namedtuple

from .utils import checks

# Get Config
import config
config = config.GetConfig()

class ChannelUtilities:

    def __init__(self, bot):
        self.bot = bot
        
        self.voice_users = dict()
        self.voice_channels = dict()
        self.text_users = dict()
        self.text_channels = dict()
        
        self.non_alphanumeric_pattern = re.compile('[^a-zA-Z0-9_ ]+', re.UNICODE)
        self.alphanumeric_pattern = re.compile('[a-zA-Z0-9_ ]+', re.UNICODE)
        
        self.Info = namedtuple('Info', 'ctx author channel expiry')
        
        #Initialises a Dictionary of lists for each guild
        for guild in self.bot.guilds:
            self.voice_users[guild] = list()
            self.voice_channels[guild] = list()
            self.text_users[guild] = list()
            self.text_channels[guild] = list()

        bot.loop.create_task(self._timing_deletion_loop())
            
    @commands.group(aliases = ['ch'])
    @checks.no_pm()
    async def channel(self, ctx):
        '''Used to manage temporary channels'''
        #For help on channel commands, use: help channel
        if ctx.invoked_subcommand is None:
            ctx.message.content = config['DEFAULT']['PREFIX'] + "help channel"
            await self.bot.process_commands(ctx.message)

    @checks.chcreate_or_permissions(manage_channels = True)
    @channel.command(aliases = ['cr'])
    @checks.no_pm()
    async def create(self, ctx, type : str, time : str, limit : str, *, name : str):
        '''Creates temporary voice/text channels
        Parameters:
        {type} = Type of channel (either [voice|v], [text|t], or [both|b])
        {time} = Time channel will exist for in minutes (between 0 and 1440)
        {limit} = amount of players able to join the channel (between 0 and 99). 0 indicating there is no limit.
        {name} = name of the channel (max 32 characters) '''
        
        guild = ctx.guild
        author = ctx.author
        
        if guild not in self.voice_users:
            self.voice_users[guild] = list()
            self.voice_channels[guild] = list()
            
        if guild not in self.text_users:
            self.text_users[guild] = list()
            self.text_channels[guild] = list()
            
            
        #Input Verification
        errors = []
        
        if type not in ('voice', 'v', 'text', 't', 'both', 'b'):
            errors.append("`Type must be either 'voice', 'text', or 'both'.`")
        
        try:
            time = int(time)
            if time < 0 or time > 1440:
                errors.append("`Time must be a number between 0 and 1440 minutes.`")
        except ValueError:
            errors.append("`Time must be a number between 0 and 1440 minutes.`")

        try:
            limit = int(limit)
            
            if limit < 0 or limit > 99:
                errors.append("`Limit must be a number between 0 and 99 users.`")
        except ValueError:
            errors.append("`Limit must be a number between 0 and 99 users.`")

        if len(name) > 32:
            errors.append("`Channel name must be at most 32 characters long.`")
            
        if len(errors) > 0: # Handle any errors
            await ctx.send("\n".join(errors))
            ctx.message.content = config['DEFAULT']['PREFIX'] + "help channel create"
            await self.bot.process_commands(ctx.message)
            return
            
        #Channel Creation
        try:
            # Handle Voice Channel
            if type in ('voice', 'v', 'both', 'b'):
                if author.id in self.voice_users[guild]:
                    await ctx.send('`You already have an active voice channel`')
                    return
            
                # Add authors ID to list
                self.voice_users[guild].append(author.id)
               
                # Create voice channel
                
                # Get relevant categories
                voice_category = guild.get_channel(int(config['CHANNELUTILITIES']['VOICE_CHANNEL_CATEGORY_ID']))
                
                if not voice_category:
                    await ctx.send("`Error finding temporary voice category.`")
                    return
                
                # Create Voice Channel
                
                # Voice Overwrite Permissions
                voice_overwrites = {
                    guild.default_role: discord.PermissionOverwrite(connect = False),
                    author: discord.PermissionOverwrite(connect = True)
                }
                
                alphanumeric_name = self.non_alphanumeric_pattern.sub('', name) #remove all non-alphanumeric chars
                
                # Confirm Final name is alphanumeric, otherwise use placeholder name
                if not self.alphanumeric_pattern.match(alphanumeric_name):
                    await ctx.send("`Provided temporary voice channel name contained invalid characters, using default name instead.`")
                    alphanumeric_name = f'temp_voice_{len(voice_category.channels) + 1}'
                    
                voice_channel = await guild.create_voice_channel(name = alphanumeric_name, category = voice_category, overwrites = voice_overwrites)
                
                # Pause after creating channels
                await asyncio.sleep(1)
               
                # Set Voice channel limit
                if limit:
                    await voice_channel.edit(user_limit = limit)
                
                await ctx.send(f'`Voice channel \'{alphanumeric_name}\' created, it will expire in {time} minute(s)!`')    
                
                # Move author to voice channel if they are connected to voice
                if author.voice is not None:
                    await author.move_to(voice_channel)
                
                #Adds channel to list
                expiry = datetime.datetime.utcnow() + datetime.timedelta(0, time * 60)
                voice_info = self.Info(ctx, author, voice_channel, expiry)
                self.voice_channels[guild].append(voice_info)
            
            # Handle Text Channel
            if type in ('text', 't', 'both', 'b'):
                if author.id in self.text_users[guild]:
                    await ctx.send('`You already have an active text channel`')
                    return
                
                # Add authors ID to list
                self.text_users[guild].append(author.id)
               
                # Create text channel
                
                # Get relevant categories
                text_category = guild.get_channel(int(config['CHANNELUTILITIES']['TEXT_CHANNEL_CATEGORY_ID']))

                if not text_category:
                    await ctx.send("`Error finding temporary text category.`")
                    return
                    
                # Text Overwrite Permissions
                text_overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages = False),
                    author: discord.PermissionOverwrite(read_messages = True)
                }

                alphanumeric_name = name.replace(' ', '_') #turn spaces into underscores
                alphanumeric_name = self.non_alphanumeric_pattern.sub('', alphanumeric_name) #remove all non-alphanumeric chars
                
                # Confirm Final name is alphanumeric, otherwise use placeholder name
                if not self.alphanumeric_pattern.match(alphanumeric_name):
                    await ctx.send("`Provided temporary text channel name contained invalid characters, using default name instead.`")
                    alphanumeric_name = f'temp_text_{len(text_category.channels) + 1}'
                
                text_channel = await guild.create_text_channel(name = alphanumeric_name, category = text_category, overwrites = text_overwrites)

                # Pause after creating channels
                await asyncio.sleep(1)
                
                # Set Text channel description
                await text_channel.edit(topic = f'{author.name}\'s temporary text channel.')
                
                await ctx.send(f'`Text channel \'{alphanumeric_name}\' created, it will expire in {time} minute(s)!`')
                
                #Adds channel to list
                expiry = datetime.datetime.utcnow() + datetime.timedelta(0, time * 60)
                text_info = self.Info(ctx, author, text_channel, expiry)
                self.text_channels[guild].append(text_info)
                
        except discord.errors.Forbidden:
            await ctx.send('`This command is disabled in this server!`')
    
    async def _timing_deletion_loop(self):
        check_rate = 30
        text_channel_recently_active_timeout = 300
        
        while True:
            for guild in self.bot.guilds:
                # Check all voice channels
                for info in self.voice_channels[guild]:
                    now = datetime.datetime.utcnow()
                    
                    # Handle manually deleted channels
                    if info.channel is None or info.channel not in guild.channels:
                        self.voice_channels[guild].remove(info)
                        self.voice_users[guild].remove(info.author.id)
                    
                    elif info.expiry < now: # channel expired
                        # Ignore if voice channel if it has members
                        if info.channel.members:
                            continue
                            
                        # Delete info and channel
                        self.voice_channels[guild].remove(info)
                        self.voice_users[guild].remove(info.author.id)
                        await info.channel.delete()
                        await info.ctx.send(info.author.mention + " your temporary voice channel has expired.")
                        
                # Check all text channels
                for info in self.text_channels[guild]:
                    now = datetime.datetime.utcnow()
                    
                    # Handle manually deleted channels
                    if info.channel is None or info.channel not in guild.channels:
                        self.text_channels[guild].remove(info)
                        self.text_users[guild].remove(info.author.id)
                    
                    elif info.expiry < now: # channel expired
                        # Ignore if text channel recently active
                        last_message = await info.channel.history(limit=1).flatten()
                         
                        if len(last_message) > 0:
                            seconds_since = (now - last_message[0].created_at).total_seconds()
                            if seconds_since <= text_channel_recently_active_timeout:
                                continue
                        
                        # Delete info and channel
                        self.text_channels[guild].remove(info)
                        self.text_users[guild].remove(info.author.id)
                        await info.channel.delete()
                        await info.ctx.send(info.author.mention + " your temporary text channel has expired.")
                
                # Sleep
                await asyncio.sleep(check_rate)
    
    @channel.command(aliases = ['del'])
    @checks.no_pm()
    async def delete(self, ctx, type : str):
        if type not in ('voice', 'v', 'text', 't', 'both', 'b'):
            await ctx.send("`Type must be either 'voice', 'text', or 'both'.`")
            return
    
        if type in ('voice', 'v', 'both', 'b'):
            #Delete your temp channel
            if ctx.author.id in self.voice_users[ctx.guild]:
                for info in self.voice_channels[ctx.guild]:
                    if info.author == ctx.author:
                        self.voice_channels[ctx.guild].remove(info)
                        self.voice_users[ctx.guild].remove(info.author.id)
                        await info.channel.delete() # delete channel
                        await ctx.send('`Your temporary voice channel has been deleted.`')
            else:
                await ctx.send("`You don't currently have a temporary voice channel!`")
        
        if type in ('text', 't', 'both', 'b'):
            #Delete your temp channel
            if ctx.author.id in self.text_users[ctx.guild]:
                for info in self.text_channels[ctx.guild]:
                    if info.author == ctx.author:
                        self.text_channels[ctx.guild].remove(info)
                        self.text_users[ctx.guild].remove(info.author.id)
                        await info.channel.delete() # delete channel
                        await ctx.send('`Your temporary text channel has been deleted.`')
            else:
                await ctx.send("`You don't currently have a temporary text channel!`")
    
    @channel.command(aliases = ['su'])
    @checks.no_pm()
    async def setusers(self, ctx, type : str, *users: discord.Member):
        if type not in ('voice', 'v', 'text', 't', 'both', 'b'):
            await ctx.send("`Type must be either 'voice', 'text', or 'both'.`")
            return
        
        if type in ('voice', 'v', 'both', 'b'):
            #Set allowed users in channel
            if ctx.author.id in self.voice_users[ctx.guild]:
                for info in self.voice_channels[ctx.guild]:
                    if info.author == ctx.author:
                        for user in users:
                            await info.channel.set_permissions(user, connect = True)
                        await ctx.send("`Voice channel permissions added for " + ", ".join([mention.name for mention in ctx.message.mentions]) + "`")
            else:
                await ctx.send("`You don't currently have a temporary voice channel!`")
        
        if type in ('text', 't', 'both', 'b'):
            #Set allowed users in channel
            if ctx.author.id in self.text_users[ctx.guild]:
                for info in self.text_channels[ctx.guild]:
                    if info.author == ctx.author:
                        for user in users:
                            await info.channel.set_permissions(user, read_messages = True)
                        await ctx.send("`Text channel permissions added for " + ", ".join([mention.name for mention in ctx.message.mentions]) + "`")
            else:
                await ctx.send("`You don't currently have a temporary text channel!`")

    @channel.command(aliases = ['ru'])
    @checks.no_pm()
    async def removeusers(self, ctx, type : str, *users: discord.Member):
        if type not in ('voice', 'v', 'text', 't', 'both', 'b'):
            await ctx.send("`Type must be either 'voice', 'text', or 'both'.`")
            return
        
        if type in ('voice', 'v', 'both', 'b'):
            #Set allowed users in channel
            if ctx.author.id in self.voice_users[ctx.guild]:
                for info in self.voice_channels[ctx.guild]:
                    if info.author == ctx.author:
                        for user in users:
                            await info.channel.set_permissions(user, connect = False)
                            # Move user out of voice channel to a default voice channel if they are currently connected
                            if user.voice is not None and user.voice.channel == info.channel:
                                default_voice_channel = ctx.guild.get_channel(int(config['CHANNELUTILITIES']['DEFAULT_VOICE_CHANNEL_ID']))
                                await user.move_to(default_voice_channel)
                        await ctx.send("`Voice channel permissions removed for " + ", ".join([mention.name for mention in ctx.message.mentions]) + "`")
            else:
                await ctx.send("`You don't currently have a temporary voice channel!`")
        
        if type in ('text', 't', 'both', 'b'):
            #Set allowed users in channel
            if ctx.author.id in self.text_users[ctx.guild]:
                for info in self.text_channels[ctx.guild]:
                    if info.author == ctx.author:
                        for user in users:
                            await info.channel.set_permissions(user, read_messages = False)
                        await ctx.send("`Text channel permissions removed for " + ", ".join([mention.name for mention in ctx.message.mentions]) + "`")
            else:
                await ctx.send("`You don't currently have a temporary text channel!`")

    @create.error
    @delete.error
    @setusers.error
    @removeusers.error
    async def generic_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("`You did not provide the '" + error.param + "' parameter.`")
def setup(bot):
    bot.add_cog(ChannelUtilities(bot))