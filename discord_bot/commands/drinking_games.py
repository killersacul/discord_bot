

import discord
from discord.ext import commands


class DrinkingGamesCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='powerhour', help='The bot will joing you vocal channel and play a powerhour')
    async def powerhour(self, ctx):
        if not (ctx.author.voice):
            await ctx.send("I cannot join you as you are not in a voice channel")
        else:
            channel = ctx.author.voice.channel
            vc = await channel.connect()


def setup(client):
    client.add_cog(DrinkingGamesCommands(client))
