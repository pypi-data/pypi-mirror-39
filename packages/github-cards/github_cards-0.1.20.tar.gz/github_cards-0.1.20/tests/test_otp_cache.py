import time

import pytest

from github_cards.otp_cache import _OTPCache


class TestOTPCache:
    @pytest.fixture
    def cache(self):
        return _OTPCache()

    @pytest.fixture
    def otp_prompt_mock(self, mocker):
        return mocker.patch("click.prompt", return_value=123456)

    def test_returns_cached_value_if_set_and_not_expired(self, cache, otp_prompt_mock):
        cache._last_entered_time = time.time()
        cache._otp_password = "654321"

        assert cache.otp_callback() == "654321"
        otp_prompt_mock.assert_not_called()

    def test_requests_one_time_password_if_not_set(self, cache, otp_prompt_mock):
        cache.otp_callback()

        otp_prompt_mock.assert_called_once()

    def test_requests_one_time_password_if_expired(self, cache, otp_prompt_mock):
        cache._last_entered_time = time.time() - (_OTPCache.CACHING_SECONDS + 0.1)

        cache.otp_callback()

        otp_prompt_mock.assert_called_once()

    def tests_asks_again_after_invalidation(self, cache, otp_prompt_mock):
        cache.otp_callback()

        otp_prompt_mock.assert_called_once()

        otp_prompt_mock.reset_mock()
        cache.invalidate()
        cache.otp_callback()

        otp_prompt_mock.assert_called_once()
