import discord
from discord.ext import commands
from datetime import datetime

LOG_CHANNEL_ID = 1409914069317718017


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ========== YARDIMCI ==========
    async def send_log(self, guild, embed):
        channel = guild.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)

    def base_embed(self, title, color=discord.Color.blurple()):
        embed = discord.Embed(
            title=title,
            color=color,
            timestamp=datetime.utcnow()
        )
        return embed

    # ========== SUNUCU GİRİŞ / ÇIKIŞ ==========
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = self.base_embed("🚪 Sunucuya Giriş", discord.Color.green())
        embed.add_field(name="Kullanıcı", value=f"{member} ({member.id})")
        await self.send_log(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = self.base_embed("🚪 Sunucudan Çıkış", discord.Color.red())
        embed.add_field(name="Kullanıcı", value=f"{member} ({member.id})")
        await self.send_log(member.guild, embed)

    # ========== PROFİL / İSİM ==========
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.avatar != after.avatar:
            embed = self.base_embed("🖼️ Profil Fotoğrafı Değişti")
            embed.add_field(name="Kullanıcı", value=f"{after} ({after.id})")
            embed.set_thumbnail(url=after.display_avatar.url)
            for guild in self.bot.guilds:
                await self.send_log(guild, embed)

        if before.name != after.name:
            embed = self.base_embed("✏️ Kullanıcı Adı Değişti")
            embed.add_field(
                name="Eski",
                value=before.name,
                inline=True
            )
            embed.add_field(
                name="Yeni",
                value=after.name,
                inline=True
            )
            for guild in self.bot.guilds:
                await self.send_log(guild, embed)

    # ========== ROL DEĞİŞİKLİK ==========
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            added = set(after.roles) - set(before.roles)
            removed = set(before.roles) - set(after.roles)

            embed = self.base_embed("🎭 Rol Güncellendi")

            if added:
                embed.add_field(
                    name="➕ Eklenen",
                    value=", ".join(r.name for r in added),
                    inline=False
                )

            if removed:
                embed.add_field(
                    name="➖ Kaldırılan",
                    value=", ".join(r.name for r in removed),
                    inline=False
                )

            embed.add_field(
                name="Kullanıcı",
                value=f"{after} ({after.id})",
                inline=False
            )

            await self.send_log(after.guild, embed)

    # ========== BAN / UNBAN ==========
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = self.base_embed("🔨 Ban Atıldı", discord.Color.dark_red())
        embed.add_field(name="Kullanıcı", value=f"{user} ({user.id})")
        await self.send_log(guild, embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = self.base_embed("♻️ Ban Kaldırıldı", discord.Color.green())
        embed.add_field(name="Kullanıcı", value=f"{user} ({user.id})")
        await self.send_log(guild, embed)

    # ========== TIMEOUT ==========
    @commands.Cog.listener()
    async def on_member_update_timeout(self, before, after):
        if before.communication_disabled_until != after.communication_disabled_until:
            embed = self.base_embed("⏱️ Timeout Güncellendi")
            embed.add_field(name="Kullanıcı", value=f"{after} ({after.id})")
            embed.add_field(
                name="Yeni Süre",
                value=str(after.communication_disabled_until),
                inline=False
            )
            await self.send_log(after.guild, embed)

    # ========== MESAJ SİLME ==========
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        embed = self.base_embed("🗑️ Mesaj Silindi", discord.Color.orange())
        embed.add_field(name="Kullanıcı", value=message.author.mention)
        embed.add_field(name="Kanal", value=message.channel.mention)
        embed.add_field(
            name="İçerik",
            value=message.content or "Boş",
            inline=False
        )
        await self.send_log(message.guild, embed)

    # ========== MESAJ DÜZENLEME ==========
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.content == after.content:
            return

        embed = self.base_embed("✏️ Mesaj Düzenlendi")
        embed.add_field(name="Kullanıcı", value=before.author.mention)
        embed.add_field(name="Kanal", value=before.channel.mention)
        embed.add_field(
            name="Eski",
            value=before.content[:1000],
            inline=False
        )
        embed.add_field(
            name="Yeni",
            value=after.content[:1000],
            inline=False
        )
        await self.send_log(before.guild, embed)

    # ========== READY ==========
    @commands.Cog.listener()
    async def on_ready(self):
        print("📑 LOG BOT READY")


async def setup(bot):
    await bot.add_cog(Logs(bot))
