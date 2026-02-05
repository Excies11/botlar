import discord
from discord.ext import commands
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Streaming(
                name="SSD Discord 🤍",
                url="https://twitch.tv/ssd"
            )
        )
        print("🎵 MUSIC BOT READY")


class TicketView(discord.ui.View):
    def __init__(self, support_role_id):
        super().__init__(timeout=None)
        self.support_role_id = support_role_id

    @discord.ui.button(label="🎫 Ticket Aç", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        user = interaction.user
        role = guild.get_role(self.support_role_id)

        category = discord.utils.get(guild.categories, name="🎫 Tickets")
        if not category:
            category = await guild.create_category("🎫 Tickets")

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category
        )

        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(user, view_channel=True, send_messages=True)
        await channel.set_permissions(role, view_channel=True, send_messages=True)

        embed = discord.Embed(
            title="🎫 Ticket Açıldı",
            description=f"{role.mention}\nKullanıcı: {user.mention}",
            color=discord.Color.green()
        )

        await channel.send(embed=embed, view=CloseView())
        await interaction.response.send_message("✅ Ticket oluşturuldu!", ephemeral=True)

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Kapat", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticket_setup(self, ctx, channel: discord.TextChannel, support_role: discord.Role):
        embed = discord.Embed(
            title="🎫 Destek Sistemi",
            description="Ticket açmak için aşağıdaki butona bas.",
            color=discord.Color.blurple()
        )

        await channel.send(embed=embed, view=TicketView(support_role.id))
        await ctx.send("✅ Ticket paneli kuruldu")

async def setup(bot):
    await bot.add_cog(Ticket(bot))
