import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Grabs the bot's token from the .env file
load_dotenv()
Discord_Bot_Token = os.getenv("Petal")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)
logging.getLogger("asyncio_redis").setLevel(logging.WARNING)

# Loads in all extensions
initial_extensions = [
    "Cogs.kumikoinfo",
    "Cogs.kumikoping",
    "Cogs.kumikohelp",
    "Cogs.reddit",
    "Cogs.mcsrvstats",
    "Cogs.waifu",
    "Cogs.hypixel",
    "Cogs.advice",
    "Cogs.qrcode-maker",
    "Cogs.spiget",
    "Cogs.jikan",
    "Cogs.top-gg",
    "Cogs.global-error-handling",
    "Cogs.kumikoinvite",
    "Cogs.mangadex",
    "Cogs.version",
    "Cogs.twitter",
    "Cogs.youtube",
    "Cogs.bonk",
    "Cogs.tenor",
    "Cogs.uptime",
    "Cogs.jisho",
    "Cogs.bot-info",
    "Cogs.help",
    "Cogs.modrinth",
    "Cogs.discord-bots",
    "Cogs.economy.marketplace",
    "Cogs.economy.users",
    "Cogs.economy.petals",
    "Cogs.platform",
    "Cogs.pages",
    "Cogs.first-frc-events",
    "Cogs.blue-alliance",
    "Cogs.legacy-help",
    "Cogs.github",
    "Cogs.anilist",
    "Cogs.rabbitmq-consumer",
    "Cogs.economy.auction_house",
    "Cogs.gws",
    "Cogs.avatar",
    "Cogs.uwu",
    "Cogs.ah-checker",
    "Cogs.economy.quests",
]
for extension in initial_extensions:
    bot.load_extension(extension)


# Adds in the bot presence
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="/kumikohelp"
        )
    )


# Run the bot
bot.run(Discord_Bot_Token)
