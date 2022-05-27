import os
from asyncio import sleep

import discord
from discord.ext import commands


class DrinkingGamesCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.counter = 0

    @commands.command(name='powerhour', help='The bot will joing you vocal channel and play a powerhour')
    async def powerhour(self, ctx, op_1: str = "start"):
        op_1 = op_1.lower()
        function_to_call = getattr(self, f"{op_1}_powerhour", None)
        if function_to_call is None:
            await ctx.send("I did not understand your command")

        await function_to_call(ctx)

    async def start_powerhour(self, ctx):
        if not (ctx.author.voice):
            await ctx.send("I cannot join you as you are not in a voice channel")
        else:
            if self.is_connected(ctx):
                await ctx.send("I am already in a voice channel")
            else:
                await self.update_bot_status(f"Powerhour counter: {self.counter}")
                channel = ctx.author.voice.channel
                vc = await channel.connect()
                await sleep(1)
                await self.play_repeat_audio(vc)

    async def stop_powerhour(self, ctx):
        if not self.is_connected(ctx):
            await ctx.send("I am not in a voice channel")
        else:
            vc = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            await vc.disconnect()
            await self.update_bot_status("")

    async def reset_powerhour(self):
        self.counter = 0
        await self.update_bot_status(f"Powerhour counter: {self.counter}")

    async def count_powerhour(self, ctx):
        await ctx.send(f"You have drank {self.counter} swigs")

    async def play_repeat_audio(self, vc):
        # @TODO LULU add a way to have different beat for the power hour
        while True:
            audio_path = 'static/audio/Powerhour_beat.mp3'
            if self.counter % 60 == 0 and self.counter != 0:
                audio_path = 'static/audio/Powerhour_oh_no.mp3'

            audio_source = discord.FFmpegPCMAudio(audio_path)
            if not vc.is_playing():
                vc.play(audio_source, after=None)
                self.counter += 1
                await self.update_bot_status(f"Powerhour counter: {self.counter}")
                await sleep(55)

    async def update_bot_status(self, msg):
        await self.client.change_presence(activity=discord.Game(name=msg))

    def is_connected(self, ctx):
        return discord.utils.get(self.client.voice_clients, guild=ctx.guild)


def setup(client):
    client.add_cog(DrinkingGamesCommands(client))
