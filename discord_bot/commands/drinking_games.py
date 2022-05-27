import os
from asyncio import sleep

import discord
from discord.ext import commands


class DrinkingGamesCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='powerhour', help='The bot will joing you vocal channel and play a powerhour')
    async def powerhour(self, ctx, op_1: str):
        if not (ctx.author.voice):
            await ctx.send("I cannot join you as you are not in a voice channel")
        else:
            if op_1 not in ["", "start", "stop"]:
                await ctx.send("I did not understand your command")
            channel = ctx.author.voice.channel
            vc = await channel.connect()
            await self.play_repeat_audio(vc)

    async def play_repeat_audio(self, vc):
        counter = 0
        while True:
            audio_source = discord.FFmpegPCMAudio('static/audio/Powerhour_beat.mp3')
            if not vc.is_playing():
                vc.play(audio_source, after=None)
                counter += 1
                await sleep(55)


def setup(client):
    client.add_cog(DrinkingGamesCommands(client))
