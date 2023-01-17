from typing import List

from discord.ext import commands
from models import Movie

HELP_TEXT = 'A simple app to keep track of movie night ideas and what was watched'

'''
a simple app to help keep track of what films the movie crew has seen and what we would like to watch,
Can add movies to the watch list
'''


class BlindTestCommands(commands.Cog):

    command_name = "movie_night"

    def __init__(self, client):
        self.name = self.command_name
        self.client = client

    @commands.command(name='movie_night', help=HELP_TEXT)
    async def movie_night(self, ctx, op_1: str = "list", op_2: str = None):
        op_1 = op_1.lower()
        function_to_call = getattr(self, f"{op_1}_{self.command_name}", None)
        if function_to_call is None:
            await ctx.send("I did not understand your command")
            return

        if op_2 is not None:
            await function_to_call(ctx, op_2)
        else:
            await function_to_call(ctx)

    async def list_movie_night(self, ctx):
        to_watch_list = self.get_to_watch()
        message = "The movies in the list are:\n"
        for movie in to_watch_list:
            message += f"{movie.name} added by {movie.get_username(self.client, ctx)}\n"

        if to_watch_list is not None:
            await ctx.send(message)
        else:
            await ctx.send("Sorry you do not have a list yet")

    async def add_movie_night(self, ctx, movie: str):
        to_watch_list = self.get_to_watch()
        movie = Movie(movie, ctx.author.id)
        if to_watch_list is None:
            to_watch_list = [movie]
        else:
            if movie.name in [movie.name for movie in to_watch_list]:
                await ctx.send(f"The movie {movie.name} is already in the list and was added by"
                               f"{movie.get_username(self.client)} on the {movie.added_on}")
                return

            to_watch_list.append(movie)
        self.write_to_watch(to_watch_list)
        await ctx.send(f"I have added the movie {movie.name} to the list!")

    async def remove_movie_night(self, ctx, movie: str):
        to_watch_list = self.get_to_watch()
        pos = None
        for idx, movie_object in enumerate(to_watch_list):
            if movie_object.name == movie:
                pos = idx
        if pos is None:
            await ctx.send(f"The movie {movie} is not in the list so I can't remove it")
            return
        del to_watch_list[pos]
        self.write_to_watch(to_watch_list)
        await ctx.send(f"The movie {movie} has successfully been remove from the list")

    async def help_movie_night(self, ctx):
        raise NotImplementedError

    async def seen_movie_night(self, ctx, movie):
        raise NotImplementedError

    def get_to_watch(self) -> List["Movie"]:
        to_watch_list = self.client.database.get_data(self.name, "to_watch")
        if to_watch_list is None:
            return []
        return [Movie.from_dict(movie) for movie in to_watch_list]

    def write_to_watch(self, to_watch_list: List[Movie]) -> List[dict]:
        self.client.database.write_data(self.name, "to_watch", [movie.to_dict() for movie in to_watch_list])


def setup(client):
    client.add_cog(BlindTestCommands(client))
