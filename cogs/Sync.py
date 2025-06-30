import discord
import requests
from discord import app_commands
from discord.ext import commands

from config import ApiConfig


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_config = ApiConfig()

    @app_commands.command(name="sync", description="To find the status.")
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Wait until you receive a dm from Rose", ephemeral=True
        )
        member = interaction.user
        api_url = self.api_config.URL

        discord_id = str(interaction.user.id)

        url = f"{api_url}/user/verify"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers, params={"discord_id": discord_id})

        if response.status_code == 200:
            data = response.json()
        else:
            print("error in sending requests")

        if data["status"]:
            status = data["status"]
        if status == "active":
            roles = [role for role in member.roles if role.name != "@everyone"]

            if roles:
                print(
                    f"Roles for {member.display_name}: {', '.join(role.name for role in roles)}is changed"
                )
                await member.remove_roles(*roles)
            role = discord.utils.get(interaction.guild.roles, id=1386299830762078309)

            if role:
                await member.add_roles(role)

        elif status == "pending":
            await member.send(
                "A Signup link will be already provided to you while joining kindly check and register"
            )
        elif status == "not_referred":
            roles = [role for role in member.roles if role.name != "@everyone"]

            if roles:
                print(
                    f"Roles for {member.display_name}: {', '.join(role.name for role in roles)} is changed"
                )
                await member.remove_roles(*roles)

            role = discord.utils.get(interaction.guild.roles, id=1386050010948309113)

            if role:
                await member.add_roles(role)

        elif status == "user_not_found":
            print("Hey")
            rules = "https://discordapp.com/channels/1385239593355313192/1386584972726632578"
            url = f"{api_url}/user/onboarding"
            headers = {"accept": "application/json", "Content-Type": "application/json"}
            data = {"discord_id": discord_id}

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                data = response.json()
            else:
                print(data["error in sending requests"])

            if data["signup_url"]:
                signup = data["signup_url"]
            else:
                print("no")
                signup = "https://discordapp.com/channels/1385239593355313192/1386584972726632578"

            embed = discord.Embed(
                title="Welcome to BuilderClan! 🛠️",
                description=f"\n\n👋 Hello **{member.name}**, welcome aboard!"
                "\n\n✨ You’ve been referred to join our amazing community of builders and innovators! 🏗️"
                "\n\n🔗 Use the following link to sign up and become a part of our journey:"
                f"\n👉[Sign Up Here]({signup})"
                f"\n👉[Find rules here]({rules})"
                "\n\n💡 Let's create something extraordinary together! 🚀",
                color=discord.Color.pink(),
            )
            embed.set_thumbnail(url=member.guild.icon.url)
            await member.send(embed=embed)

        else:
            return {
                "status": "unknown",
                "message": f"Unexpected account status: '{status}'",
            }


async def setup(bot: commands.bot):
    await bot.add_cog(Sync(bot))

