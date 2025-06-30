import discord
import requests


async def update_member_status(
    member: discord.Member, name: str, role_id: int = None, guild=None
):
    # Remove all roles except @everyone
    roles = [role for role in member.roles if role.name != "@everyone"]
    if roles:
        print(
            f"Roles for {member.display_name}: {', '.join(role.name for role in roles)} are changed"
        )
        await member.remove_roles(*roles)

    # Add new role if provided
    if role_id and guild:
        role = discord.utils.get(guild.roles, id=role_id)
        if role:
            await member.add_roles(role)


async def name_assign(member: discord.Member, name: str):
    try:
        await member.edit(nick=name)
        await member.send(f"✅ Nickname updated as {name} in server")
    except:
        print("❌ Failed to set nickname")


async def register(member: discord.member, api_url: str, discord_id: int):
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
        signup = (
            "https://discordapp.com/channels/1385239593355313192/1386584972726632578"
        )

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
