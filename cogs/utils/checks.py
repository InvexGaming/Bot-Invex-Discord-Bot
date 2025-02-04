from discord.ext import commands
import discord.utils

# Get Config
import config
config = config.GetConfig()

def is_owner_check(message):
    return message.author.id in [365795952767795201, 356003102169759755, 101786275568164864, 361542628015079426]

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))

# The permission system of the bot is based on a "just works" basis
# You have permissions and the bot has permissions. If you meet the permissions
# required to execute the command (and the bot does as well) then it goes through
# and you can execute the command.
# If these checks fail, then there are two fallbacks.
# A role with the name of Bot Mod and a role with the name of Bot Admin.
# Having these roles provides you access to certain commands without actually having
# the permissions required for them.
# Of course, the owner will always be able to execute commands.

def check_permissions(ctx, perms):
    msg = ctx.message
    if is_owner_check(msg):
        return True

    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())

def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if isinstance(ch, (discord.DMChannel, discord.GroupChannel)):
        return False  # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None

def mod_or_inv():
    def predicate(ctx):
        if check_permissions(ctx, dict(manage_server=True)):
            return True

        check = lambda r: r.name in ('Bot Mod', 'Bot Admin', 'Bot Inventory')
        ch = ctx.message.channel
        author = ctx.message.author
        if isinstance(ch, (discord.DMChannel, discord.GroupChannel)):
            return False  # can't have roles in PMs

        role = discord.utils.find(check, author.roles)
        return role is not None

    return commands.check(predicate)

def mod_or_permissions():
    def predicate(ctx):
        if check_permissions(ctx, dict(manage_server=True)):
            return True
        check = lambda r: r.name in ('Bot Mod', 'Bot Admin')
        ch = ctx.message.channel
        author = ctx.message.author
        if isinstance(ch, (discord.DMChannel, discord.GroupChannel)):
            return False  # can't have roles in PMs

        role = discord.utils.find(check, author.roles)
        return role is not None
    return commands.check(predicate)

def admin_or_permissions(**perms):
    def predicate(ctx):
        if check_permissions(ctx, dict(manage_server=True)):
            return True

        check = lambda r: r.name == 'Bot Admin'
        ch = ctx.message.channel
        author = ctx.message.author
        if isinstance(ch, (discord.DMChannel, discord.GroupChannel)):
            return False  # can't have roles in PMs

        role = discord.utils.find(check, author.roles)
        return role is not None

    return commands.check(predicate)

def is_in_servers(*server_ids):
    def predicate(ctx):
        server = ctx.message.server
        if server is None:
            return False
        return server.id in server_ids
    return commands.check(predicate)

def chcreate_or_permissions(**perms):
        def predicate(ctx):
            return role_or_permissions(ctx, lambda r: r.name == 'VIP', **perms)

        return commands.check(predicate)

def owner_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda ctx: is_owner_check(ctx.message))
    return commands.check(predicate)

def nsfw_channel():
    def predicate(ctx):
        if not (isinstance(ctx.channel, (discord.DMChannel, discord.GroupChannel)) or "nsfw" in ctx.channel.name.lower()):
            raise ChannelError("This command can only be used in `nsfw` channels!")
        return True
    return commands.check(predicate)

def no_pm():
    def predicate(ctx):
        if ctx.command.name == "help":
            return True
        if ctx.guild is None:
            raise commands.NoPrivateMessage('This command cannot be used in private messages.')
        return True
    return commands.check(predicate)

def commandschat_channel():
    def predicate(ctx):
        commandschat_channel = ctx.guild.get_channel(int(config['DEFAULT']['COMMANDSCHAT_CHANNEL_ID']))
        if ctx.channel.id != commandschat_channel.id:
            raise ChannelError(f"`You can only use this command in the` {commandschat_channel.mention} `text channel.`")
        return True
    return commands.check(predicate)    
    
class ChannelError(commands.CommandError):
    def __init__(self, message):
        self.__message__ = message
        super().__init__(message)

