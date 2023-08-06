# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import time


class ExecuteWithRetry:
    def __init__(self, max_retries, max_back_off_seconds, should_retry_func, log_message, action):
        if not callable(should_retry_func):
            raise TypeError('should_retry_func: Argument is not callable')
        self.max_retries = max_retries
        self.max_back_off_seconds = max_back_off_seconds
        self.should_retry_func = should_retry_func
        self.log_message = log_message
        self.action = action
        # only for the testing purpose
        self._last_wait_time = 0

    def execute(self, func, *args, **kwargs):
        if not callable(func):
            raise TypeError('Argument is not callable')

        self._current_retry = 0
        while self._current_retry < self.max_retries:
            try:
                output = func(*args, **kwargs)
                (should_retry, back_off_factor) = self.should_retry_func(
                    output=output, exception=None, current_retry=self._current_retry + 1)
                if should_retry:
                    self._current_retry += 1
                    if self._current_retry < self.max_retries:
                        self._wait_for_retry(
                            back_off_factor, self._current_retry, self.max_retries)
                        continue
                return output
            except Exception as e:
                (should_retry, back_off_factor) = self.should_retry_func(
                    output=None, exception=e, current_retry=self._current_retry + 1)
                if should_retry:
                    self._current_retry += 1
                    if self._current_retry < self.max_retries:
                        self._wait_for_retry(
                            back_off_factor, self._current_retry, self.max_retries)
                        continue
                raise

    def _wait_for_retry(self, back_off, current_retry, total_retry):
        delay = 0
        if self._last_wait_time != self.max_back_off_seconds:
            delay = back_off ** current_retry
            if delay > self.max_back_off_seconds:
                delay = self.max_back_off_seconds
            self._last_wait_time = delay
        self.log_message("{}: Retry {} waiting for {} seconds before next retry".format(
            self.action, current_retry, self._last_wait_time))
        time.sleep(self._last_wait_time)
