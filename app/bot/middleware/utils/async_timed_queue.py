import asyncio
from datetime import datetime, timedelta, timezone
from collections import deque


class AsyncTimedQueue[T: datetime]:
    def __init__(self, max_age: timedelta) -> None:
        self.max_age = max_age
        self.q = deque[T]()
        self._lock = asyncio.Lock()

    @classmethod
    def get_time_now(cls) -> datetime:
        return datetime.now(timezone.utc)


    @classmethod
    def get_age(cls, item: T) -> datetime:
        return item


    async def clear_old(self) -> None:
        async with self._lock:
            current_time = self.get_time_now()
            while self.q and (current_time - self.get_age(self.q[0])) > self.max_age:
                self.q.popleft()


    async def push(self, item: T) -> None:
        await self.clear_old()
        async with self._lock:
            self.q.append(item)


    async def peek(self) -> T | None:
        await self.clear_old()
        return self.q[0] if self.q else None


    async def get_len(self) -> int:
        await self.clear_old()
        return self.q.__len__()
