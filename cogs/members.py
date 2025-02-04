import discord
from discord.ext import commands

from datetime import datetime, timezone

class MembersCog(commands.Cog):

    """Useful functions to use on guild members."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member=None):
        """Says when a member joined."""
        
        if not member:
            member = ctx.author
        
        join_time = member.joined_at
        join_time = join_time.replace(tzinfo=timezone.utc).astimezone(tz=None) # convert from UTC to local
        
        join_time_str = join_time.strftime('%A %d %B %Y at %I:%M:%S %p')
        await ctx.send(f'{member.display_name} joined on `{join_time_str}`')
    
    @commands.command(name='bot', aliases=['ping'])
    async def _bot(self, ctx):
        """Ping bot to see if it is alive."""
        await ctx.send('Yes, I\'m alive.')

    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        top_role_name =  member.top_role.name if member.top_role.name != '@everyone' else 'Default Role'
        
        await ctx.send(f'The top role for {member.display_name} is {top_role_name}')
    
    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *, member: discord.Member=None):
        """Displays a users avatar link."""
        
        if not member:
            member = ctx.author
        
        await ctx.send(f"**{member.display_name}'s avatar URL:**\n{member.avatar_url}")
  
        
# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MembersCog(bot))