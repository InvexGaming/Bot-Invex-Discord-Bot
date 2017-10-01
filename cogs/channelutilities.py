import asyncio
import discord
from discord.ext import commands

from .utils import checks

# Get Config
import config
config = config.GetConfig()

class ChannelUtilities:

    def __init__(self, bot):
        self.bot = bot
        self.current_users = dict()
        self.current_channels = dict()

        #Initialises a Dictionary of lists for each guild#
        for guild in self.bot.guilds:
            self.current_users[guild] = list()
            self.current_channels[guild] = list()

    @commands.group(aliases = ['ch'])
    @checks.no_pm()
    async def channel(self, ctx):
        #For help on channel commands, use: help channel#
        if ctx.invoked_subcommand is None:
            ctx.message.content = config['DEFAULT']['PREFIX'] + "help channel"
            await self.bot.process_commands(ctx.message)

    @checks.chcreate_or_permissions(manage_channels = True)
    @channel.command(aliases = ['cr'])
    @checks.no_pm()
    async def create(self, ctx, time : str, limit : int, *, name : str):
        '''Creates a temp channel; Usage channel create {time} {maxusers} {name}
        Parameters:
        {time} = Time channel will exist for;
        {limit} = amount of players able to join the channel
        {name} = name of the channel '''

        if ctx.guild not in self.current_users:
            self.current_users[ctx.guild] = list()
            self.current_channels[ctx.guild] = list()

        #Time input Verification#
        if len(time) > 4:
            await ctx.send("Temporary channels can last at MOST a day! (1440 minutes)")
            return
        else:
            time = int(time)
            if time > 1440:
                await ctx.send("Temporary channels can last at MOST a day! (1440 minutes)")
                return

        if limit > 99:
            await ctx.send("`User limit must be in between 0 - 99 users!`")
            return

        #Channel Creation#
        try:
            guild = ctx.guild
            author = ctx.author

            if author.id not in self.current_users[guild]:
                if not name:
                    name = author.name
                
                # Move to specific category
                temp_category = guild.get_channel(360990997716402177)
                
                if temp_category:
                    # Text Channel Creation
                    channel = await guild.create_voice_channel(name)
                    
                    # Little Hacky but needed to avoid position out of bounds exception occuring
                    # Sets the position relative to the category prior to setting channels category
                    await channel.edit(position = len(temp_category.channels))
                    
                    await channel.edit(category = temp_category)
                    
                    if limit:
                        await channel.edit(user_limit = limit)

                    await ctx.send(f'`Channel {name} created, it will expire in {time} minute(s)!`')
                    await author.move_to(channel)
                    #Sets permissions for author#
                    await channel.set_permissions(author, connect = True)

                    await channel.set_permissions(ctx.message.guild.default_role, connect = False)

                    #Adds Author's ID and Channel to Lists#
                    self.current_users[guild].append(author.id)
                    info = (author, channel, guild)
                    self.current_channels[guild].append(info)                    
                    
                    # Timing and Deletion Loop#
                    while True:

                        ch = None
                        remaining = time*60
                        checkRate = 30

                        # Timing Loop #
                        while remaining != 0:
                            try:
                                #Check for Manual Channel Deletion#
                                ch = await self.bot.wait_for("guild_channel_delete", check = lambda x: x.id == channel.id, timeout = checkRate)
                                break

                            except asyncio.TimeoutError:
                                remaining -= checkRate
                                if not channel.members:
                                    #Check if channel has users#
                                    ch = None
                                    break

                        if ch is not None:
                            #Deletes stored info if manually deleted#
                            self.current_channels[guild].remove(info)
                            self.current_users[guild].remove(author.id)

                        else:
                            if channel.members:
                                #If channel has users, waits till they are gone#
                                continue

                            if author.id in self.current_users[guild]:
                                #Channel Deletion and notifying the author#
                                try:
                                    await channel.delete()
                                    self.current_channels[guild].remove(info)
                                    self.current_users[guild].remove(author.id)
                                    await ctx.send(author.mention + " your channel has expired")

                                except discord.NotFound:
                                    #Deletes information if Discord 404's#
                                    self.current_channels[guild].remove(info)
                                    self.current_users[guild].remove(author.id)

                        if not self.current_channels[guild]:
                            del self.current_channels[guild]

                        if not self.current_users[guild]:
                            del self.current_users[guild]

                        break
                else:
                    await ctx.send('`Failed to find Temporary Category`')
            else:
                await ctx.send('`You already have a active channel`')
        except discord.errors.Forbidden:
            await ctx.send('`This command is disabled in this server!`')

    @channel.command()
    @checks.no_pm()
    async def delete(self, ctx):
        #Delete your temp channel; usage channel delete#
        if ctx.author.id in self.current_users[ctx.guild]:
            for channel in self.current_channels[ctx.guild]:
                if channel[0] == ctx.author:
                    await channel[1].delete()
                    await ctx.send('`Your channel has been deleted`')
        else:
            await ctx.send("`You don't currently have a channel!`")

    @channel.command(aliases = ['su'])
    @checks.no_pm()
    async def setusers(self, ctx, *users: discord.Member):
        #Set allowed users in channel; usage ch setusers {@user} {@user} ...#
        if ctx.author.id in self.current_users[ctx.guild]:
            for channel in self.current_channels[ctx.guild]:
                if channel[0] == ctx.author:
                    for user in users:
                        await channel[1].set_permissions(user, connect=True)
                    await ctx.send("` Permissions added for " + ", ".join([mention.name for mention in ctx.message.mentions]) + "`")
        else:
            await ctx.send("`You don't currently have a channel!`")

def setup(bot):
    bot.add_cog(ChannelUtilities(bot))