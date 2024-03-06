import disnake
import asyncio
from disnake.ext import commands
from config import SERVER_ID
from cogs_music.music_utilits import MusicUtilits

class PlayCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.music_u = MusicUtilits()

        self.voice_clients = {}

        self.loop = asyncio.get_event_loop()
        self.data = None

        self.repeat = False

    async def play(self, inter, url: str):
        try:
            self.server_id = inter.guild.id

            if self.server_id not in self.voice_clients:
                
                if await self.connect_to_voice(inter):
                    await self.music_u.save_to_queue(url, self.server_id)
                    
                    await self.play_music(inter, self.server_id)
            else:        
                await inter.response.send_message("Загрузка песни..", delete_after=20)

                await self.music_u.save_to_queue(url, self.server_id)
                await self.music_u.edit_original_message(inter, self.server_id, self.song_info)

        except Exception as e:
            print(f"Ошибка: {e}")
            await inter.send("Произошла ошибка, пожалуйста, свяжитесь с администрацией для получения дополнительной информации!!!", ephemeral=True)

    async def connect_to_voice(self, inter):
        author_voice = inter.author.voice
        if author_voice:
            self.voice_client = await author_voice.channel.connect()
            self.voice_clients[self.voice_client.guild.id] = self.voice_client
            await inter.send(content="Запускаю музыку...")
            return self.voice_client
            
        else:
            await inter.response.send_message("Чтобы использовать эту команду, необходимо находиться в голосовом канале", ephemeral=True)
            return False

    async def play_music(self, inter, server_id):
        """
        Запускаем музыку
        """
        
        if server_id in self.music_u.queue and self.music_u.queue[server_id]:
            
            self.song_info = self.music_u.queue[server_id].pop(0)  # Получаем информацию о текущей песне
            song_url = self.song_info["info_url"]

            await self.music_u.edit_original_message(server_id=server_id, inter=inter, song_info=self.song_info)

            player = disnake.FFmpegOpusAudio(song_url, **self.music_u.ffmpeg_options)

            def after_playing(e):
                self.loop.create_task(self.play_music(inter, server_id))

            self.voice_client.play(player, after=after_playing)
        else:
            await asyncio.sleep(5)
            await self.voice_clients[server_id].disconnect()
            del self.voice_clients[server_id]

