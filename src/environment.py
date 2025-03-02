import json
from typing import Any

from src.password import Password


class Environment:
    def __init__(self) -> None:
        self._filename = "clockify.json"

        self._data: None | dict = None

        with open(self._filename, "r+") as file:
            file = file.read()
            if file == "":
                file = "{}"
            self._data = json.loads(file)

    @property
    def password(self) -> Password:
        return Password(self)

    def __getitem__(self, key: Any) -> Any:
        return self._data[key]

    def get(self, key: Any, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __setitem__(self, key: Any, value: Any) -> None:
        self._data[key] = value

        with open(self._filename, "w+") as file:
            file.write(json.dumps(self._data, indent=4))

    def __delitem__(self, key: Any) -> None:
        del self._data[key]

        with open(self._filename, "w+") as file:
            file.write(json.dumps(self._data, indent=4))
