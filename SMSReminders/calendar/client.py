import datetime
import os
from typing import Tuple, List

import pytz
from googleapiclient import discovery
from pydantic import BaseModel

from SMSReminders.calendar.credentials import CredentialsProvider
from SMSReminders.calendar.models import Event


class CalendarClient(BaseModel):
    provider: CredentialsProvider

    def get_calendar_ids(self) -> List[str]:
        calendar_list = self._service.calendarList().list().execute()
        return [calendar['id'] for calendar in calendar_list.get('items', [])]

    def fetch_calendar_events(
            self,
            calendar_id: str,
            start_time: str,
            end_time: str,
    ) -> List[Event]:
        """
        Fetches calendar events within the specified time range.

        :param calendar_id: ID of the calendar to fetch events from
        :param start_time: The start time of the range to fetch events from (ISO Format)
        :param end_time: The end time of the range to fetch events from (ISO Format)
        :return: The list of events fetched

        """

        # Build the service

        events_result = self._service.events().list(
            calendarId=calendar_id,
            timeMin=start_time,
            timeMax=end_time,
            maxResults=int(os.environ.get('MAX_RESULTS', '25')),
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    @property
    def _service(self):
        return discovery.build(
            'calendar',
            'v3',
            credentials=self.provider.credentials
        )

    @staticmethod
    def today_iso_range(
            timezone: str
    ) -> Tuple[str, str]:
        """
        Get today's date range in ISO format.

        :param timezone: The timezone to localize the date range to
        :return: A tuple containing the start and end of today in ISO format

        """

        now = datetime.datetime.now(tz=pytz.timezone(timezone))

        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        day_end = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()

        return day_start, day_end
