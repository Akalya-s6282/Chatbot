import discord
import requests
from discord import app_commands
from discord.ext import commands

from config import ApiConfig, GuildConfig
from utils import register, update_member_status


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_config = ApiConfig()
        self.guildconfig = GuildConfig()

    @app_commands.command(name="sync", description="To find the status.")
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Wait until you receive a dm from Rose", ephemeral=True
        )
        member = interaction.user
        api_url = self.api_config.URL

        discord_id = str(interaction.user.id)
        temp_member_id = int(self.guildconfig.MEMBER_TEMP_ROLE_ID)
        member_id = int(self.guildconfig.MEMBER_ROLE_ID)

        url = f"{api_url}/user/verify"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers, params={"discord_id": discord_id})

        if response.status_code == 200:
            data = response.json()
        else:
            print("error in sending requests")

        if data["status"]:
            # status = data["status"]
            status = "user_not_found"
        if status == "active":
            await update_member_status(
                member, role_id=member_id, guild=interaction.guild
            )

        elif status == "pending":
            await member.send(
                "A Signup link will be already provided to you while joining kindly check and register"
            )
        elif status == "not_referred":
            await update_member_status(
                member, role_id=temp_member_id, guild=interaction.guild
            )

        elif status == "user_not_found":
            await register(member, api_url, discord_id)

        else:
            return {
                "status": "unknown",
                "message": f"Unexpected account status: '{status}'",
            }


async def setup(bot: commands.bot):
    await bot.add_cog(Sync(bot))
