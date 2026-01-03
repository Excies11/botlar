import discord
from discord.ext import commands

MLLOG_CHANNEL_ID = 1409914069317718017
await mod_bot.change_presence(
    status=discord.Status.online,
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="SSD Private | SSD Log"
    )
)

class MLLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_channel(self, guild):
        return guild.get_channel(MLLOG_CHANNEL_ID)

    # ================= MEMBER JOIN =================
    @commands.Cog.listener()
    async def on_member_join(self, member):
        ch = self.get_channel(member.guild)
        if not ch:
            return

        embed = discord.Embed(
            title="🟢 Üye Katıldı",
            color=discord.Color.green()
        )
        embed.add_field(name="Kullanıcı", value=f"{member} ({member.id})")
        embed.set_thumbnail(url=member.display_avatar.url)

        await ch.send(embed=embed)

    # ================= MEMBER LEAVE =================
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        ch = self.get_channel(member.guild)
        if not ch:
            return

        embed = discord.Embed(
            title="🔴 Üye Ayrıldı",
            color=discord.Color.red()
        )
        embed.add_field(name="Kullanıcı", value=f"{member} ({member.id})")

        await ch.send(embed=embed)

    # ================= MESSAGE DELETE =================
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.author.bot:
            return

        ch = self.get_channel(message.guild)
        if not ch:
            return

        embed = discord.Embed(
            title="🗑️ Mesaj Silindi",
            color=discord.Color.orange()
        )
        embed.add_field(name="Kullanıcı", value=message.author.mention)
        embed.add_field(name="Kanal", value=message.channel.mention)
        embed.add_field(
            name="Mesaj",
            value=message.content[:1000] if message.content else "İçerik yok",
            inline=False
        )

        await ch.send(embed=embed)

    # ================= MESSAGE EDIT =================
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild or before.author.bot:
            return
        if before.content == after.content:
            return

        ch = self.get_channel(before.guild)
        if not ch:
            return

        embed = discord.Embed(
            title="✏️ Mesaj Düzenlendi",
            color=discord.Color.blue()
        )
        embed.add_field(name="Kullanıcı", value=before.author.mention)
        embed.add_field(name="Kanal", value=before.channel.mention)
        embed.add_field(
            name="Önce",
            value=before.content[:500] or "Yok",
            inline=False
        )
        embed.add_field(
            name="Sonra",
            value=after.content[:500] or "Yok",
            inline=False
        )

        await ch.send(embed=embed)

    # ================= BAN =================
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        ch = self.get_channel(guild)
        if not ch:
            return

        embed = discord.Embed(
            title="🔨 Ban Atıldı",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Kullanıcı", value=f"{user} ({user.id})")

        await ch.send(embed=embed)

    # ================= UNBAN =================
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        ch = self.get_channel(guild)
        if not ch:
            return

        embed = discord.Embed(
            title="♻️ Ban Kaldırıldı",
            color=discord.Color.green()
        )
        embed.add_field(name="Kullanıcı", value=f"{user} ({user.id})")

        await ch.send(embed=embed)

    # ================= TIMEOUT =================
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.communication_disabled_until != after.communication_disabled_until:
            ch = self.get_channel(after.guild)
            if not ch:
                return

            if after.communication_disabled_until:
                title = "🔇 Timeout Verildi"
                color = discord.Color.orange()
            else:
                title = "🔊 Timeout Kaldırıldı"
                color = discord.Color.green()

            embed = discord.Embed(title=title, color=color)
            embed.add_field(name="Kullanıcı", value=after.mention)

            await ch.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MLLog(bot))
