from typing import TypedDict, Optional


class CreatorOrganizer(TypedDict, total=False):
    email: str
    self: bool
    displayName: Optional[str]


class DateTimeDetails(TypedDict, total=False):
    dateTime: str
    timeZone: str


class Reminders(TypedDict, total=False):
    useDefault: bool


class Event(TypedDict, total=False):
    kind: str
    etag: str
    id: str
    status: str
    htmlLink: str
    created: str
    updated: str
    summary: str
    creator: CreatorOrganizer
    organizer: CreatorOrganizer
    start: DateTimeDetails
    end: DateTimeDetails
    iCalUID: str
    sequence: int
    reminders: Reminders
    eventType: str

