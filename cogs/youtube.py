import discord
from discord.ext import commands

import asyncio
import aiohttp
import async_timeout
from datetime import datetime, timezone

# Get Config
import config
config = config.GetConfig()

"""A cog to post Youtube videos ."""

class Youtube:
    """Youtube"""
    
    def __init__(self, bot):
        bot.loop.create_task(self.check_youtube_channel(bot))
    
    async def check_youtube_channel(self, bot):
        await bot.wait_until_ready()
        
        invex_guild = bot.get_guild(int(config['DEFAULT']['INVEXGUILD']))
        youtube_webhook = discord.utils.get(await invex_guild.webhooks(), name='Youtube')
        
        while not bot.is_closed():
            # Make a session
            session = aiohttp.ClientSession()
            
            # Get uploaded videos playlist id
            uploads_id_query = f"https://www.googleapis.com/youtube/v3/channels?id={config['YOUTUBE']['CHANNEL_ID']}&key={config['YOUTUBE']['API_KEY']}&part=contentDetails"
            
            try:
                with async_timeout.timeout(30):
                    async with session.get(uploads_id_query) as response:
                        r = await response.json()
                        if response.status != 200:
                            await asyncio.sleep(5*60) # timeout 5 minutes
                            continue
            except asyncio.TimeoutError:
                await asyncio.sleep(5*60) # timeout 5 minutes
                continue
            
            uploads_id = r["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            # Query playlistitems to get list of videos (last 10 videos)
            playlistitems_query = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={uploads_id}&key={config['YOUTUBE']['API_KEY']}&part=snippet&maxResults=10"
            
            try:
                with async_timeout.timeout(30):
                    async with session.get(playlistitems_query) as response:
                        r = await response.json()
                        if response.status != 200:
                            await asyncio.sleep(5*60) # timeout 5 minutes
                            continue
            except asyncio.TimeoutError:
                await asyncio.sleep(5*60) # timeout 5 minutes
                continue
            
            session.close()
            
            videos = r["items"]
            
            # Get last processed time
            f = open("data/youtubelastupdate.txt", "r+")
            
            local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
            
            try:
                last_processed_datetime = datetime.fromtimestamp(float(f.readline())).replace(tzinfo=local_timezone)
            except:
                last_processed_datetime = datetime.fromtimestamp(0).replace(tzinfo=local_timezone) # if failed to read timestamp, assume first run
            
            for video in videos:
                published_at = video['snippet']['publishedAt']
                published_at_datetime = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.%fZ")
                published_at_datetime = published_at_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None) # convert from UTC to local
                published_at_str = published_at_datetime.strftime('%A %d %B %Y at %I:%M:%S %p')
                
                if published_at_datetime > last_processed_datetime:
                    # New video, post to web hook
                    await youtube_webhook.send(f"**{video['snippet']['channelTitle']}** uploaded **{video['snippet']['title']}** at {published_at_str}:\nhttps://youtu.be/{video['snippet']['resourceId']['videoId']}")
                    
            # Store current epoch to file so we don't reprocess same videos later
            epoch = datetime.now()
            
            f.seek(0)
            f.write(str(epoch.timestamp()))
            f.truncate()
            f.close()
            
            await asyncio.sleep(60*60) #60 minutes
    
def setup(bot):
    bot.add_cog(Youtube(bot))