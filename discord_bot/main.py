import logging
import os
import sys

from discord.ext import commands


def start_client():
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot = commands.Bot(command_prefix='!')

    cog_files = ['commands.basic', 'commands.powerhour']
    for cog_file in cog_files:
        bot.load_extension(cog_file)
        print(f"{cog_file} has loaded.")

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    bot.run(TOKEN)


if __name__ == "__main__":
    start_client()
