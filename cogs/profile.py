import discord
from discord import app_commands
from discord.ext import commands


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="To get profile info")
    async def profile(self, interaction: discord.Interaction):
        print("hey")
        await interaction.response.send_message(
            "Wait until you receive a dm from Rose", ephemeral=True
        )
        user = interaction.user
        avatar_url = user.avatar.url

        embed = discord.Embed(title="User Info", color=discord.Color.pink())
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Display Name", value=user.display_name, inline=False)
        embed.add_field(name="Bot?", value=user.bot, inline=False)
        embed.add_field(
            name="Account Created",
            value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            inline=False,
        )

        # Only in servers/guilds
        if isinstance(user, discord.Member) and user.joined_at:
            embed.add_field(
                name="Joined Server",
                value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"),
                inline=False,
            )

        await user.send(embed=embed)


async def setup(bot: commands.bot):
    await bot.add_cog(Profile(bot))
