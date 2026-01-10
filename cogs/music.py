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


def get_spotify_title(url: str) -> str | None:
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string

        # Spotify başlık formatı: "Yıldızlar - Çakal | Spotify"
        title = title.replace("| Spotify", "").strip()
        return title
    except:
        return None


class MusicView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="⏸️", style=discord.ButtonStyle.secondary)
    async def pause(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("Duraklatıldı", ephemeral=True)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.success)
    async def resume(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("Devam ediyor", ephemeral=True)

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            await interaction.response.send_message("Durduruldu", ephemeral=True)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Streaming(
                name="SSD Discord 🤍",
                url="https://twitch.tv/ssd"
            )
        )
        print("🎵 MUSIC BOT READY")

    @commands.command()
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Ses kanalında değilsin")

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        vc = ctx.voice_client

        # 🔥 SPOTIFY LINK → BAŞLIK → YOUTUBE SEARCH
        if "open.spotify.com" in query:
            title = get_spotify_title(query)
            if not title:
                return await ctx.send("❌ Spotify başlığı alınamadı")
            query = title  # ARTIK NORMAL YAZI

        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]

            url = info["url"]
            title = info["title"]

        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTS)

        if vc.is_playing() or vc.is_paused():
            vc.stop()

        vc.play(source)

        await ctx.send(
            embed=discord.Embed(
                title="🎶 Şimdi Çalıyor",
                description=title,
                color=discord.Color.green()
            ),
            view=MusicView()
        )


async def setup(bot):
    await bot.add_cog(Music(bot))
