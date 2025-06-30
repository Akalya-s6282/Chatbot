import asyncio

import discord
from discord.ext import commands

from config import Config

bot_config = Config()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Set the command prefix
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Sync failed: {e}")


@bot.command()
async def profile(ctx):
    user = ctx.author
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

    await ctx.send(embed=embed)

async def main():
    # ADD YOUR COGS HERE
    await bot.load_extension("cogs.verify_webhooks")
    await bot.load_extension("cogs.roles")
    await bot.load_extension("cogs.Sync")
    # Start the bot
    await bot.start(bot_config.TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
