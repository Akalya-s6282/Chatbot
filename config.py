import os

from dotenv import load_dotenv

load_dotenv()


# Discord bot configuration
class Config:
    TOKEN = os.getenv("DISCORD_TOKEN")


# API configuration
class ApiConfig:
    URL = os.getenv("API_URL")


# Discord guild configuration
class GuildConfig:
    MEMBER_ROLE_ID = os.getenv("MEMBER_ROLE_ID")
    MEMBER_TEMP_ROLE_ID = os.getenv("MEMBER_TEMP_ROLE_ID")
