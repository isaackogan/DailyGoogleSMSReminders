import datetime
import json
from typing import List, Dict

import pytz
from twilio.rest import Client

from SMSReminders.calendar.calendar import Calendar
from SMSReminders.calendar.client import CalendarClient
from SMSReminders.calendar.credentials import CredentialsProvider
from SMSReminders.calendar.models import Event


class SMSRemindersClient:

    def __init__(
            self,
            app_credentials_fp: str,
            user_credentials_fp: str,
            sms_credentials_fp: str,
            timezone: str = "US/Eastern"
    ):
        self._provider: CredentialsProvider = CredentialsProvider(
            app_credentials_fp=app_credentials_fp,
            user_credentials_fp=user_credentials_fp
        )

        self._calendar_client: CalendarClient = CalendarClient(
            provider=self._provider
        )

        self._timezone: str = timezone

        # Load Twilio credentials
        with open(sms_credentials_fp) as f:
            credentials_json = json.load(f)
            self._sms_client = Client(credentials_json['account_sid'], credentials_json['auth_token'])
            self._from_number = credentials_json['from_number']
            self._to_number = credentials_json['to_number']

    @property
    def timezone(self) -> str:
        return self._timezone

    def get_all_events_today(self):
        calendar_ids: List[str] = self._calendar_client.get_calendar_ids()
        all_events_today = []

        for calendar_id in calendar_ids:
            calendar: Calendar = Calendar(
                calendar_id=calendar_id,
                client=self._calendar_client
            )

            all_events_today.extend(calendar.fetch_events_today(self._timezone))

        return all_events_today

    def get_sms_text(self) -> str:

        events: List[Event] = self.get_all_events_today()
        event_buckets: Dict[str, List[Event]] = {}

        for event in events:
            organizer = event['organizer'].get('displayName', "General")
            event_buckets[organizer] = event_buckets.get(organizer, [])
            event_buckets[organizer].append(event)

        # Date as "Friday, September 16th" format
        today_date = datetime.datetime.now(pytz.timezone(self._timezone)).strftime("%A, %B %d")

        if not events:
            return f"No events for {today_date}."

        sms_text = f"{len(events)} Event{'s' if len(events) == 1 else ''} for {today_date}:\n\n"

        # General should be the first
        items = sorted(event_buckets.items(), key=lambda x: x[0] != "General")

        for organizer, events in items:
            sms_text += f"{organizer}:"

            for event in events:
                date_time_iso_str = event['start'].get('dateTime')
                date_text: str = ""

                if date_time_iso_str:
                    date_time = datetime.datetime.fromisoformat(date_time_iso_str)

                    # Convert to 12:00 PM format
                    date_text += f" at {date_time.strftime('%I:%M %p')}"

                sms_text += f"\n• \"{event['summary']}\"{date_text}"

            sms_text += "\n\n"

        return sms_text.strip()

    def send_daily_reminder(self) -> str:
        """
        Sends the daily reminder to the user.

        :return: The SMS text sent

        """

        sms_text = self.get_sms_text()

        self._sms_client.messages.create(
            body=sms_text,
            from_=self._from_number,
            to=self._to_number
        )

        return sms_text
