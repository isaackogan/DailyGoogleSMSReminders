import time

import schedule
from schedule import Job

from SMSReminders.client import SMSRemindersClient
from SMSReminders.schedule import create_job

client: SMSRemindersClient = SMSRemindersClient(
    app_credentials_fp="./resources/app_credentials.json",
    user_credentials_fp="./resources/user_credentials.json",
    sms_credentials_fp="./resources/sms_credentials.json",
    timezone="US/Eastern"
)


def daily_reminder_task():
    print("Sending daily reminder...")
    print("=" * 30)
    print(client.send_daily_reminder())


if __name__ == '__main__':

    print("Starting the SMS reminder service...")

    # Run at 8am every day
    job: Job = create_job(
        time_str="00:40:30",
        timezone=client.timezone,
        task=daily_reminder_task
    )

    # Run forever
    while True:
        schedule.run_pending()
        time.sleep(1)
