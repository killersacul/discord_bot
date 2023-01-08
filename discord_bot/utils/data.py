import json
import os
from typing import Any


'''
For now since this bot is only meant to run on one discord there is no need to split data by discord.
'''


def get_data(command_name: str, key: str) -> Any:
    print(f"getting data {key} for {command_name} ")
    file_path = create_file_path(command_name)
    if not os.path.exists(file_path):
        print(f"Could not find file {file_path}")
        return None

    with open(file_path, 'r') as file:
        json_data = json.load(file)
        data = json_data[key]
    print(f"Found {data}")
    return data


def write_data(command_name: str, key: str, value: str):
    print(f"writing data {value} with {key} for {command_name}")
    file_path = create_file_path(command_name)
    if not os.path.exists(file_path):
        print(f"Could not find file for {command_name} so creating file")
        with open(file_path, "x") as file:
            pass

    with open(file_path, "r") as file:
        json_data = json.load(file)

    json_data[key] = value
    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)


# /***** private *****/


def create_file_path(command_name: str):
    return f"data/{command_name}.json"
