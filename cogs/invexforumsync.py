import discord
from discord.ext import commands

import pymysql, asyncio

# Get Config
import config
config = config.GetConfig()

"""A cog to sync roles on the server based on verified Discord Tags stored in the Invex database"""

class InvexForumMember:
    """InvexForumMember"""
    def __init__(self, username, usergroups, discord_tag):
        self.username = username
        self.usergroups = usergroups
        self.discord_tag = discord_tag

class InvexForumSync:
    """InvexForumSync"""
    
    def __init__(self, bot):
        bot.loop.create_task(self.sync(bot))
        
    @commands.command(aliases = ['link'])
    async def verify(self, ctx):
        '''Print information about how to link Discord to Invex Forum Accounts'''
        await ctx.send("**Want to receive your role/rank?**\nYou have to link your forum account and Discord account to receive your role.\nOur Bot will automatically update roles every 15 minutes.\n**Visit:** https://www.invexgaming.com.au/showthread.php?tid=8384")

    async def sync(self, bot):
        await bot.wait_until_ready()
        while not bot.is_closed():
            # Connect to Invex DB
            conn = pymysql.connect(host=config['DB']['HOST'], port=int(config['DB']['PORT']), user=config['DB']['USER'], passwd=config['DB']['PASSWORD'], db=config['DB']['DATABASE'])
            cur = conn.cursor()
            
            # Fetch username, usergroups, additionalgroups and fid7 (discord tag in user#discrim format)
            cur.execute('''SELECT u.username, u.usergroup, u.additionalgroups, uf.fid7
                            FROM mybb_rmbj_users u
                            JOIN mybb_rmbj_userfields uf ON u.uid = uf.ufid
                            WHERE uf.fid7 IS NOT NULL AND uf.fid7 != '' ''')
            
            # Iterate through results accumulating InvexForumMember objects
            verified_forum_members = []
            for row in cur:
                usergroups = set()
                usergroups.add(int(row[1]))
                if len(row[2]) != 0:
                    usergroups.update(list(map(int, row[2].split(",")))) #split by comma and convert to int list
                
                verified_forum_members.append(InvexForumMember(row[0], usergroups, row[3]))
                
            cur.close()
            conn.close()
            
            # Iterate through all members in the Discord
            invex_guild = bot.get_guild(int(config['DEFAULT']['INVEXGUILD']))
            
            for discord_member in invex_guild.members:
                # Skip the guild owner as we will lack permissions to modify them
                if discord_member == invex_guild.owner:
                    continue
            
                # Skip other bots
                bot_role = discord.utils.get(invex_guild.roles, name='Bot')
                if bot_role in discord_member.roles:
                    continue
            
                # Try to find a verified forum user with matching tag
                forum_member = None
                for member in verified_forum_members:
                    if member.discord_tag == str(discord_member):
                        forum_member = member
                        break
                
                # If no match found, remove all roles from this Discord member
                if forum_member is None:
                    roles = discord_member.roles[1:] #exclude @everyone role
                    if len(roles) > 0:
                        await discord_member.remove_roles(*roles)
                else:
                    #Process this user
                    
                    # Enforce Username
                    await discord_member.edit(nick = forum_member.username)
                    
                    # Assign Roles/Permissions
                    await self._sync_role(invex_guild, forum_member, discord_member, 51, 'Staff')
                    await self._sync_role(invex_guild, forum_member, discord_member, 95, 'Head Administrator')
                    await self._sync_role(invex_guild, forum_member, discord_member, 31, 'Server Administrator')
                    await self._sync_role(invex_guild, forum_member, discord_member, 52, 'Surf Admin')
                    await self._sync_role(invex_guild, forum_member, discord_member, 66, 'Jailbreak Admin')
                    await self._sync_role(invex_guild, forum_member, discord_member, 72, '1v1 Admin')
                    await self._sync_role(invex_guild, forum_member, discord_member, 55, 'Veteran')
                    await self._sync_role(invex_guild, forum_member, discord_member, 11, 'Senior Member')
                    await self._sync_role(invex_guild, forum_member, discord_member, 41, 'VIP')
                    await self._sync_role(invex_guild, forum_member, discord_member, 21, 'Member')
        
            
            await asyncio.sleep(15*60) #15 minutes

    async def _sync_role(self, guild, forum_member, discord_member, forum_group_id, target_role_name):
        
        target_role = discord.utils.get(guild.roles, name=target_role_name)
        
        discord_member_roles = discord_member.roles[1:] #exclude @everyone role
        
        if (forum_group_id in forum_member.usergroups) and (target_role not in discord_member_roles):
            # Add missing role
            await discord_member.add_roles(target_role)
        elif (forum_group_id not in forum_member.usergroups) and (target_role in discord_member_roles):
            # Remove role they shouldn't have
            await discord_member.remove_roles(target_role)

def setup(bot):
    bot.add_cog(InvexForumSync(bot))