import discord
from discord.ext import commands

from config import GuildConfig
from utils import name_assign, update_member_status


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guildconfig = GuildConfig()

    @commands.Cog.listener()
    async def on_message(self, message):
        bot = self.bot
        temp_member_id = int(self.guildconfig.MEMBER_TEMP_ROLE_ID)
        member_id = int(self.guildconfig.MEMBER_ROLE_ID)
        verify_user = int(self.guildconfig.VERIFY_USER)

        if message.author == bot.user:
            return
        if message.content.startswith("!"):
            return
        if message.type != discord.MessageType.default:
            return
        else:
            await message.channel.send(
                f"{message.author.name} has sent {message.content}", delete_after=5
            )
        ALLOWED_USER_IDS = [1168170948088840212, 869471461545480212]
        if message.channel.id == verify_user:
            if (message.webhook_id is not None) or (
                message.author.id in ALLOWED_USER_IDS
            ):
                text = message.content
                try:
                    status = text.split("status: ")[1]
                    discordid = text.split("discord_id: ")[1]
                    discord_id_str = discordid.split(",")[0].strip()
                    discord_id = int(discord_id_str)
                    name_in = text.split("name: ")[1]
                    name = name_in.split(",")[0].strip()
                except:  # noqa: E722
                    return

                member = await message.guild.fetch_member(discord_id)

                if status == "not_referred":
                    await update_member_status(
                        member, name, role_id=temp_member_id, guild=message.guild
                    )
                    await name_assign(member, name)

                elif status == "active":
                    await update_member_status(
                        member, name, role_id=member_id, guild=message.guild
                    )
                    await name_assign(member, name)

                elif status == "pending":
                    await update_member_status(member, name)
                    await name_assign(member, name)


async def setup(bot):
    await bot.add_cog(Roles(bot))
