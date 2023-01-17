from datetime import date, datetime


class Movie():

    def __init__(self, name: str, added_by: int, added_on: datetime = date.today()):
        self.name = name
        self.added_on = added_on
        self.added_by = added_by

    def __str__(self) -> str:
        return f"Movie({self.name})"

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def from_dict(cls, data_dict) -> "Movie":
        return cls(
            name=data_dict.get("name"),
            added_on=date.fromisoformat(data_dict.get("added_on")),
            added_by=data_dict.get("added_by"),
        )

    def get_username(self, client, ctx):
        user = ctx.guild.get_member(user_id=self.added_by)
        if user is not None:
            return user.display_name
        return "User could not be found"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "added_on": self.added_on.isoformat(),
            "added_by": self.added_by,
        }
