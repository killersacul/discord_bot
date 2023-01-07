from asyncio import sleep

import discord
from discord.ext import commands

HELP_TEXT = 'The bot will joing you vocal channel and play a powerhour'


class PowerHourCommands(commands.Cog):
    # @IDEA LULU have it so each user has the total powerhour done stored by the bot.
    # @TODO LULU Add more sounds and a system to be able to change them.

    def __init__(self, client):
        self.client = client
        self.counter = 0
        self.current_voice_channel = None

    @commands.command(name='powerhour', help=HELP_TEXT)
    async def powerhour(self, ctx, op_1: str = "start"):
        op_1 = op_1.lower()
        function_to_call = getattr(self, f"{op_1}_powerhour", None)
        if function_to_call is None:
            await ctx.send("I did not understand your command")

        await function_to_call(ctx)

    async def start_powerhour(self, ctx):
        # do we want to powerhour to restart when the bot joins a new channel???
        if not (ctx.author.voice):
            await ctx.send("I cannot join you as you are not in a voice channel")
            return

        if self.is_connected(ctx) and not ctx.author.guild_permissions.administrator:
            await ctx.send("I am already in a voice channel")
            return

        elif self.is_connected(ctx) and ctx.author.guild_permissions.administrator:
            vc = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            await vc.disconnect()

        channel = ctx.author.voice.channel
        print(channel)
        vc = await channel.connect()
        self.current_voice_channel = vc
        self.client.loop.create_task(self.check_if_channel_empty())
        await sleep(1)
        await self.update_bot_status(f"Powerhour counter: {self.counter}")
        await self.play_repeat_audio(vc)

    async def stop_powerhour(self, ctx):
        # @TODO LULU need to make sure the bot is connected to the same voice channels as the user asking to stop.
        if not self.is_connected(ctx):
            await ctx.send("I am not in a voice channel")
        else:
            vc = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            self.current_voice_channel = None
            await vc.disconnect()
            await self.update_bot_status("")

    async def reset_powerhour(self):
        self.counter = 0
        await self.update_bot_status(f"Powerhour counter: {self.counter}")

    async def count_powerhour(self, ctx):
        await ctx.send(f"You have drank {self.counter} swigs")

    async def play_repeat_audio(self, vc):
        # @TODO LULU find a way to get the sound duration for the timing
        # @TODO LULU add a way to have different beat for the power hour
        #            and have a command to list them and change ofc.
        while True:
            audio_path = 'static/audio/Powerhour_beat.mp3'
            if self.counter % 60 == 0 and self.counter != 0:
                audio_path = 'static/audio/Powerhour_oh_no.mp3'

            audio_source = discord.FFmpegPCMAudio(audio_path, options="-loglevel panic")
            if not vc.is_playing():
                vc.play(audio_source, after=None)
                self.counter += 1
                await self.update_bot_status(f"Powerhour counter: {self.counter}")
                await sleep(55)

    async def update_bot_status(self, msg):
        await self.client.change_presence(activity=discord.Game(name=msg))

    async def check_if_channel_empty(self):
        await self.client.wait_until_ready()
        while True:
            print(self.current_voice_channel.channel.members)
            if all([member.bot for member in self.current_voice_channel.channel.members]):
                await self.current_voice_channel.disconnect()
                self.current_voice_channel = None
                break
            await sleep(60)

    def is_connected(self, ctx):
        return discord.utils.get(self.client.voice_clients, guild=ctx.guild)

    def get_stored_data(self):
        raise NotImplementedError


def setup(client):
    client.add_cog(PowerHourCommands(client))
