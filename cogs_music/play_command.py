import disnake
import youtube_dl
import asyncio
from disnake.ext import commands
from config import SERVER_ID


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        self.voice_clients = {}
        
        self.ydl_options = {"format": 'bestaudio/best'}
        self.ytdl = youtube_dl.YoutubeDL(self.ydl_options)
        self.ffmpeg_options = { 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', }


    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="играть",
        description="Play music in a voice channel"
    )
    async def play(self, inter, url: str):
        try:

            voice_client = await inter.author.voice.channel.connect()
            self.voice_clients[voice_client.guild.id] = voice_client

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))

            song = data["url"]
            player = disnake.FFmpegPCMAudio(song, **self.ffmpeg_options)

            voice_client.play(player)

        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(Music(bot))
