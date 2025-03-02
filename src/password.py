import keyring
import keyring.errors


class TokenNotProvided(Exception):
    pass


class Password:
    def __init__(self, env) -> None:
        self._service_name = "system"
        self._username = "clockify-cli"

        self._env = env

    @property
    def value(self) -> str | None:
        try:
            return keyring.get_password(self._service_name, self._username)
        except Exception:
            return self._env.get("token")
            # raise TokenNotProvided(
            #     "Keyring is not available on your system. Token not provided"
            # ) from None

    @value.setter
    def value(self, new_password: str) -> None:
        try:
            keyring.set_password(self._service_name, self._username, new_password)
        except Exception:
            self._env["token"] = new_password

    def delete(self) -> None:
        try:
            return keyring.delete_password(self._service_name, self._username)
        except Exception:
            del self._env["token"]
