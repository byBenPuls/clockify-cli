from datetime import datetime

from src.clockify import ClockifyHttpClient, ClockifyMethod
from src.lib_types import TimeEntry, Workspace


def serialize_time_entry(time_entry: dict) -> TimeEntry:
    return TimeEntry(
        billiable=time_entry.get("billiable"),
        id=time_entry.get("id"),
        description=time_entry.get("description"),
        tag_ids=time_entry.get("tagIds"),
        is_locked=time_entry.get("isLocked"),
        start=datetime.strptime(
            time_entry.get("timeInterval").get("start"), "%Y-%m-%dT%H:%M:%SZ"
        ),
        end=datetime.strptime(
            time_entry.get("timeInterval").get("end"), "%Y-%m-%dT%H:%M:%SZ"
        )
        if time_entry.get("timeInterval").get("end")
        else None,
    )


class AllWorkspaces(ClockifyMethod):
    def __init__(self, http_client):
        super().__init__(http_client)

    def serialize_response(self, response: dict) -> list[Workspace]:
        return [Workspace(i.get("id"), i.get("name")) for i in response]

    def execute(self) -> list[Workspace]:
        response = self._client.get("workspaces")
        response.raise_for_status()
        response = response.json()

        return self.serialize_response(response)


class StartEntryTime(ClockifyMethod):
    def __init__(self, http_client: ClockifyHttpClient):
        super().__init__(http_client)

    def serialize_response(self, response: dict) -> TimeEntry:
        return serialize_time_entry(response)

    def execute(
        self,
        workspace_id: str,
        entry_time_name: str | None = None,
    ) -> TimeEntry:
        body = {"description": entry_time_name}

        response = self._client.post(
            f"workspaces/{workspace_id}/time-entries", json=body
        ).json()

        return self.serialize_response(response)


class SpecificTimeEntry(ClockifyMethod):
    def __init__(self, http_client):
        super().__init__(http_client)

    def serialize_response(self, response: dict) -> TimeEntry:
        return serialize_time_entry(response)

    def execute(self, workspace_id: str, time_entry_id: str) -> TimeEntry:
        response = self._client.get(
            f"workspaces/{workspace_id}/time-entries/{time_entry_id}"
        )

        return self.serialize_response(response.json())


class StopTimeEntry(ClockifyMethod):
    def __init__(self, http_client):
        super().__init__(http_client)

    def serialize_response(self, response: dict) -> TimeEntry:
        return serialize_time_entry(response)

    def execute(self, workspace_id: str, time_entry_id: str) -> TimeEntry:
        time_entry = SpecificTimeEntry(self._client).execute(
            workspace_id, time_entry_id
        )

        time_entry.end = datetime.now()
        response = self._client.put(
            f"workspaces/{workspace_id}/time-entries/{time_entry_id}",
            json=time_entry.to_json(),
        ).json()
        return self.serialize_response(response)
