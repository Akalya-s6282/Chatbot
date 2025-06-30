import asyncio

import discord
import requests
from discord.ext import commands

from config import ApiConfig, Config

bot_config = Config()
api_config = ApiConfig()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Set the command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

api_url = api_config.URL


@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"❌ Sync failed: {e}")


@bot.command()
async def clear(ctx):
    await ctx.channel.purge(limit=None)
    await ctx.send("✅ All messages cleared.", delete_after=3)


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.name}! 👋")


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


@bot.command()
async def weather(ctx, *, city: str):
    try:
        response = requests.get("http://127.0.0.1:5000/weather", params={"city": city})
        data = response.json()

        if "error" in data:
            await ctx.send(f"❌ {data['error']}")
        else:
            await ctx.send(
                f"🌤️ Weather in **{data['city']}**:\n"
                f"🌡️ Temperature: **{data['temperature']}°C**\n"
                f"📄 Condition: **{data['description'].capitalize()}**"
            )
    except Exception as e:
        await ctx.send("⚠️ Failed to fetch weather.")
        print("Error:", e)


async def main():
    # ADD YOUR COGS HERE
    await bot.load_extension("cogs.verify_webhooks")
    await bot.load_extension("cogs.roles")
    await bot.load_extension("cogs.Sync")
    # Start the bot
    await bot.start(bot_config.TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
