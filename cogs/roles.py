import discord
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        bot = self.bot
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
        if message.channel.name == "verify-user":
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
                    roles = [role for role in member.roles if role.name != "@everyone"]

                    if roles:
                        print(
                            f"Roles for {member.display_name}: {', '.join(role.name for role in roles)} is changed"
                        )
                        await member.remove_roles(*roles)

                    role = discord.utils.get(
                        message.guild.roles, id=1386050010948309113
                    )

                    if role:
                        await member.add_roles(role)
                    try:
                        await member.edit(nick=name)
                        await member.send(f"✅ Nickname updated as {name} in server")
                    except:  # noqa: E722
                        print("❌ Failed to set nickname")

                elif status == "active":
                    roles = [role for role in member.roles if role.name != "@everyone"]

                    if roles:
                        print(
                            f"Roles for {member.display_name}: {', '.join(role.name for role in roles)}is changed"
                        )
                        await member.remove_roles(*roles)
                    role = discord.utils.get(
                        message.guild.roles, id=1386299830762078309
                    )

                    if role:
                        await member.add_roles(role)
                    try:
                        await member.edit(nick=name)
                        await member.send(f"✅ Nickname updated as {name} in server")
                    except:  # noqa: E722
                        print("❌ Failed to set nickname")

                elif status == "pending":
                    roles = [role for role in member.roles if role.name != "@everyone"]

                    if roles:
                        print(
                            f"Roles for {member.display_name}: {', '.join(role.name for role in roles)}is changed "
                        )
                        await member.remove_roles(*roles)
                    try:
                        await member.edit(nick=name)
                        await member.send(f"✅ Nickname updated as {name} in server")
                    except:  # noqa: E722
                        print("❌ Failed to set nickname")

                else:
                    print("")


async def setup(bot):
    await bot.add_cog(Roles(bot))
