from typing import Callable

import schedule


def create_job(
        time_str: str,
        timezone: str,
        task: Callable[[], None]
) -> schedule.Job:

    # Schedule the task
    return schedule.every().day.at(time_str, timezone).do(task)
