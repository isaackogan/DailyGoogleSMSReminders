from typing import List

from pydantic import BaseModel

from SMSReminders.calendar.client import CalendarClient
from SMSReminders.calendar.models import Event


class Calendar(BaseModel):
    calendar_id: str
    client: CalendarClient

    def fetch_events_today(self, timezone: str) -> List[Event]:
        """
        Fetches the events for today.

        :return: The list of events fetched

        """

        start_time, end_time = self.client.today_iso_range(timezone=timezone)

        return self.client.fetch_calendar_events(
            calendar_id=self.calendar_id,
            start_time=start_time,
            end_time=end_time
        )
