import pytest

from github_cards.exceptions import GitHubCardsException, catch_github_cards_exception

NORMAL_RETURN_VALUE = "NORMAL RETURN VALUE"
EXCEPTION_MESSAGE = "ERROR"


@catch_github_cards_exception
def method_that_can_error(exception=None):
    if exception is not None:
        raise exception(EXCEPTION_MESSAGE)
    return NORMAL_RETURN_VALUE


class TestExceptionCatchingDecorator:
    def test_returns_functions_return_value_when_not_erroring(self):
        assert method_that_can_error() == NORMAL_RETURN_VALUE

    def test_lets_other_exceptions_propagate(self):
        with pytest.raises(ValueError):
            method_that_can_error(ValueError)

    def test_echos_error_message_and_exits_with_code_1_on_own_exception(self, mocker):
        sys_exit_mock = mocker.patch("sys.exit")
        click_echo_mock = mocker.patch("click.echo")

        method_that_can_error(GitHubCardsException)

        sys_exit_mock.assert_called_with(1)
        click_echo_mock.assert_called_with(EXCEPTION_MESSAGE, err=True)
