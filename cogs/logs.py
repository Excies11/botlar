import discord
from discord.ext import commands

LOG_CHANNEL_ID = 1409915479438393425
OTOROL_ID = 1409896783743549512
await mod_bot.change_presence(
    status=discord.Status.online,
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="SSD Private | SSD Login"
    )
)
class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.get_channel(LOG_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="🟢 Üye Katıldı",
                description=f"{member.mention}",
                color=discord.Color.green()
            )
            await channel.send(embed=embed)

        role = member.guild.get_role(OTOROL_ID)
        if role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.get_channel(LOG_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="🔴 Üye Ayrıldı",
                description=f"{member}",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
