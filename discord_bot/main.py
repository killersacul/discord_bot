import logging
import os
import sys

from discord.ext import commands
from utils.database import DatabaseFactory


def start_client():
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix='!')
    setattr(bot, "database", DatabaseFactory.create("json"))
    cog_files = ['commands.basic', 'commands.movie_night']
    for cog_file in cog_files:
        bot.load_extension(cog_file)
        print(f"{cog_file} has loaded.")

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    bot.run(TOKEN)


if __name__ == "__main__":
    start_client()
