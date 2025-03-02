from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum


class TimeEntryType(Enum):
    REGULAR = "REGULAR"
    BREAK = "BREAK"


@dataclass
class TimeEntry:
    billiable: bool | None = None
    description: str | None = None
    id: str | None = None
    is_locked: bool | None = None
    kiosk_id: str | None = None
    project_id: str | None = None
    tag_ids: list[str] | None = None
    end: datetime | None = None
    start: datetime | None = None
    task_id: str | None = None
    type_: TimeEntryType | None = None

    def _transform_datetime_to_str(self, datetime_obj: datetime) -> str:
        return datetime_obj.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_json(self) -> dict:
        return {
            "billiable": self.billiable,
            "description": self.description,
            "id": self.id,
            "is_locked": self.is_locked,
            "kiosk_id": self.kiosk_id,
            "project_id": self.project_id,
            "tag_ids": self.tag_ids,
            "end": self._transform_datetime_to_str(self.end),
            "start": self.start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "task_id": self.task_id,
            "type": self.type_,
        }


@dataclass
class Workspace:
    id: str
    name: str
