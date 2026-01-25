import discord
from discord.ext import commands
import yt_dlp
import requests
from bs4 import BeautifulSoup

YDL_OPTS = {
    "format": "bestaudio",
    "quiet": True,
    "default_search": "ytsearch",
    "noplaylist": True,
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


def get_spotify_title(url: str):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.replace("| Spotify", "").strip()
        return title
    except:
        return None


class MusicView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="⏸️", style=discord.ButtonStyle.secondary)
    async def pause(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸️ Duraklatıldı", ephemeral=True)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.success)
    async def resume(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("▶️ Devam ediyor", ephemeral=True)

    @discord.ui.button(label="🔁 Loop", style=discord.ButtonStyle.primary)
    async def loop(self, interaction: discord.Interaction, _):
        self.cog.loop = not self.cog.loop
        durum = "AÇIK 🔁" if self.cog.loop else "KAPALI ❌"
        await interaction.response.send_message(f"Loop {durum}", ephemeral=True)

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc:
            self.cog.loop = False
            vc.stop()
            await vc.disconnect()
            await interaction.response.send_message("⏹️ Durduruldu", ephemeral=True)


VOICE_CHANNEL_ID = 1464939407139147890  # BURAYA SES KANALI ID

@bot.event
async def on_ready():
    print(f"🟢 {bot.user} AKTİF")

    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            await channel.connect()
            print("🔊 Ses kanalına girildi")
        except Exception as e:
            print("❌ Ses kanalına girilemedi:", e)





class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = False
        self.current_source = None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Streaming(
                name="SSD Discord 🤍",
                url="https://twitch.tv/ssd"
            )
        )
        print("🎵 MUSIC BOT READY")

    def play_next(self, vc):
        if self.loop and self.current_source:
            vc.play(
                discord.FFmpegPCMAudio(self.current_source, **FFMPEG_OPTS),
                after=lambda e: self.play_next(vc)
            )

    @commands.command()
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Ses kanalında değilsin")

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        vc = ctx.voice_client

        if "open.spotify.com" in query:
            title = get_spotify_title(query)
            if not title:
                return await ctx.send("❌ Spotify başlığı alınamadı")
            query = title

        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]

            self.current_source = info["url"]
            title = info["title"]

        source = discord.FFmpegPCMAudio(self.current_source, **FFMPEG_OPTS)

        if vc.is_playing() or vc.is_paused():
            vc.stop()

        vc.play(
            source,
            after=lambda e: self.play_next(vc)
        )

        await ctx.send(
            embed=discord.Embed(
                title="🎶 Şimdi Çalıyor",
                description=title,
                color=discord.Color.green()
            ),
            view=MusicView(self)
        )


async def setup(bot):
    await bot.add_cog(Music(bot))
