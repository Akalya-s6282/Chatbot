from discord.ext import commands

from config import ApiConfig
from utils import register


class VerifyWebhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_config = ApiConfig()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        api_url = self.api_config.URL

        discord_id = str(member.id)
        await register(member, api_url, discord_id)


async def setup(bot):
    await bot.add_cog(VerifyWebhooks(bot))
