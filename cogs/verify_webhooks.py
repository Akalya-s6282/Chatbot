import discord
import requests
from discord.ext import commands

from config import ApiConfig


class VerifyWebhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_config = ApiConfig()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        api_url = self.api_config.URL

        rules = (
            "https://discordapp.com/channels/1385239593355313192/1386584972726632578"
        )

        discord_id = str(member.id)

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


async def setup(bot):
    await bot.add_cog(VerifyWebhooks(bot))
