import discord
from discord.ext import commands

class TicketView(discord.ui.View):
    def __init__(self, category_id: int, staff_role_id: int):
        super().__init__(timeout=None)
        self.category_id = category_id
        self.staff_role_id = staff_role_id

    @discord.ui.button(label="🎟️ Ticket Aç", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, _):
        guild = interaction.guild
        user = interaction.user

        category = guild.get_channel(self.category_id)
        if not category:
            return await interaction.response.send_message(
                "❌ Ticket kategorisi bulunamadı", ephemeral=True
            )

        # Aynı kullanıcıdan 1 ticket
        for ch in category.channels:
            if ch.topic == str(user.id):
                return await interaction.response.send_message(
                    "❌ Zaten açık bir ticketin var", ephemeral=True
                )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.get_role(self.staff_role_id): discord.PermissionOverwrite(
                view_channel=True, send_messages=True
            ),
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category,
            overwrites=overwrites,
            topic=str(user.id)
        )

        await channel.send(
            f"🎟️ {user.mention} ticket oluşturdu.\n"
            f"Yetkililer sizinle ilgilenecek.\n\n"
            f"`!close` yazarak ticketi kapatabilirsiniz."
        )

        await interaction.response.send_message(
            f"✅ Ticket oluşturuldu: {channel.mention}",
            ephemeral=True
        )


class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.category_id = None
        self.staff_role_id = None

    # ===== SETUP =====
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticket_setup(self, ctx, category: discord.CategoryChannel, staff_role: discord.Role):
        self.category_id = category.id
        self.staff_role_id = staff_role.id

        embed = discord.Embed(
            title="🎟️ Destek Sistemi",
            description="Aşağıdaki butona basarak ticket oluşturabilirsiniz.",
            color=discord.Color.green()
        )

        await ctx.send(
            embed=embed,
            view=TicketView(self.category_id, self.staff_role_id)
        )

    # ===== CLOSE =====
    @commands.command()
    async def close(self, ctx):
        if not ctx.channel.topic:
            return await ctx.send("❌ Bu kanal bir ticket değil")

        await ctx.send("⏳ Ticket 5 saniye içinde kapanıyor...")
        await ctx.channel.delete(delay=5)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
