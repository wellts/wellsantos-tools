from asyncio import sleep
from datetime import datetime, timedelta, timezone

from pydantic.v1.datetime_parse import parse_datetime


class Clock:
    def current(self):
        return datetime.utcnow()

    def tick(self, use_case):
        """Abstract method."""

    async def sleep(self, delay: float, *, result=None, use_case):
        return await sleep(delay, result)

    def timestamp(self, value: float):
        return datetime.fromtimestamp(value)

    def parse(self, date) -> datetime:
        return parse_datetime(date)

    def difference(self, end: datetime, start: datetime):
        return self.ensure_timezone(end) - self.ensure_timezone(start)

    def is_equal(self, end: datetime, start: datetime):
        return self.ensure_timezone(end) == self.ensure_timezone(start)

    def is_bigger_than(self, end: datetime, start: datetime):
        return self.ensure_timezone(end) > self.ensure_timezone(start)

    def is_past(self, deadline: datetime, delta: timedelta = timedelta(seconds=0)):
        return self.ensure_timezone(deadline) <= self.ensure_timezone(self.current() + delta)

    def ensure_timezone(self, date: datetime) -> datetime:
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        return date
