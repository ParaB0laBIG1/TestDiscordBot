import disnake
import youtube_dl
from disnake.ext import commands
from disnake import VoiceChannel, FFmpegPCMAudio
from disnake.ext.commands import Bot
from config import SERVER_ID

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=[SERVER_ID],
        name="играть",
        description="Play music in a voice channel"
    )
    async def play(self, inter, url: str):
        try:
            voice_channel = inter.author.voice.channel
            await inter.response.send_message("Включаю музыку")
        
            if voice_channel:
                voice_channel: VoiceChannel = await voice_channel.connect()

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url2 = info['formats'][0]['url']

                voice_client = disnake.utils.get(self.bot.voice_clients, guild=inter.guild)

                if voice_client and not voice_client.is_playing():
                    voice_client.play(disnake.FFmpegPCMAudio(url2), after=lambda e: print('done', e))
                    await inter.send(f'Now playing: {url}')
        
                else:
                    await inter.response.send_message("Bot is already playing or you are not in a voice channel!")

        except Exception as e:
            print(f"Ошибка: {e}")

def setup(bot):
    bot.add_cog(Music(bot))
