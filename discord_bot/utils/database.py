import json
import os
from typing import Any, Tuple


class DatabaseFactory():

    @staticmethod
    def create(type: str = "json"):
        if type == "json":
            return DatabaseJson()


class DatabaseJson():

    def get_data(self, command_name: str, key: str) -> Any:
        print(f"getting data {key} for {command_name} ")
        file_path = self._create_file_path(command_name)
        if not os.path.exists(file_path):
            print(f"Could not find file {file_path}")
            return None

        if self._check_file_empty(file_path):
            return None

        with open(file_path, 'r') as file:
            json_data = json.load(file)
            data = json_data[key]

        print(f"Found {data}")
        return data

    def write_data(self, command_name: str, key: str, value: str):
        print(f"writing data {value} with {key} for {command_name}")
        file_path = self._create_file_path(command_name)
        if not os.path.exists(file_path):
            print(f"Could not find file for {command_name} so creating file")
            with open(file_path, "x") as file:
                pass

        with open(file_path, "r") as file:
            try:
                if self._check_file_empty(file_path) is False:
                    json_data = json.load(file)
            except Exception as e:
                json_data = {}
                print(f"Probleme loading json with message '{e}'")

        json_data[key] = value
        with open(file_path, "w") as file:
            json.dump(json_data, file, indent=4)

    def get_filtered_data(self, command_name: str, key: str, data_filter: Tuple[str, str]) -> Any:
        output = []
        data = self.get_data(command_name, key)
        if data is None:
            return None

        print(f"trying to filter data {data} with filter {data_filter}")
        if not isinstance(data, list):
            print(f"data is not a list format its {type(data)}")
            return data

        for item in data:
            if not isinstance(item, dict):
                print(f"item inside list is not dict its {type(item)}")
                continue

            if not data_filter[0] in item.keys():
                print(f"item has no attribute {data_filter[0]}")
                continue

            if item[data_filter[0]] == data_filter[1]:
                output.append(item)

        if output == []:
            return None
        print(f"Found {output}")
        return output

    def _check_file_empty(self, file_path: str):
        return os.stat(file_path).st_size == 0

    def _create_file_path(self, command_name: str):
        return f"data/{command_name}.json"
