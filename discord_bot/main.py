import logging
import os

from discord.ext import commands


def start_client():
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix='!')

    cog_files = ['commands.basic']
    for cog_file in cog_files:
        bot.load_extension(cog_file)
        logging.warning(f"{cog_file} has loaded.")

    @bot.event
    async def on_ready():
        logging.warning(f'{bot.user.name} has connected to Discord!')

    bot.run(TOKEN)


if __name__ == "__main__":
    start_client()
