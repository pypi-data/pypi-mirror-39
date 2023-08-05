import sys
from functools import wraps

import click


class GitHubCardsException(RuntimeError):
    pass


def catch_github_cards_exception(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GitHubCardsException as exc:
            click.echo(str(exc), err=True)
            sys.exit(1)

    return wrapped
