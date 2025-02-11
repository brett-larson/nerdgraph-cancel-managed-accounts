import time
from collections import deque
from datetime import datetime, timedelta
from cancel_managed_accounts.utils import setup_logger

# Create logger for the module
logger = setup_logger(__name__)

class RateLimiter:
    """
    Rate limiter to limit the number of calls per minute
    """
    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.calls = deque()

    def wait_if_needed(self):
        """
        Wait if the rate limit is reached
        :return: None
        """

        now = datetime.now()

        # Remove calls older than 1 minute
        logger.info(f"Checking calls: {self.calls}")
        while self.calls and (now - self.calls[0]) > timedelta(minutes=1):
            self.calls.popleft()

        # If at limit, wait until oldest call is more than 1 minute old
        if len(self.calls) >= self.calls_per_minute:
            wait_time = (self.calls[0] + timedelta(minutes=1) - now).total_seconds()
            if wait_time > 0:
                logger.info(f"Rate limit reached. Waiting for {wait_time} seconds.")
                time.sleep(wait_time)

        self.calls.append(now)
