import time

import click


class _OTPCache:
    CACHING_SECONDS = 30

    def __init__(self):
        self._otp_password = None
        self._last_entered_time = None

    def otp_callback(self):
        if (
            self._otp_password is None
            or (time.time() - self._last_entered_time) >= self.CACHING_SECONDS
        ):
            self._request_otp_password()
        return self._otp_password

    def invalidate(self):
        self._otp_password = None

    def _request_otp_password(self):
        self._otp_password = click.prompt(
            "Please enter 2 Factor Authentication password: ", type=int
        )
        self._last_entered_time = time.time()
        return self._otp_password


otp_cache = _OTPCache()
