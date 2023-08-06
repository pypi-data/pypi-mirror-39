from functools import wraps

import click
import github3

from github_cards.otp_cache import otp_cache


def inject_github_instance(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        gh = github3.GitHub()
        username = kwargs["username"]
        password = kwargs["password"]
        if username is not None:
            if password is None:
                password = click.prompt(
                    f"Please enter GitHub-Password for {username}", hide_input=True
                )
            gh.login(
                username=username,
                password=password,
                two_factor_callback=otp_cache.otp_callback,
                # does not use the otp here but only during further requests
            )
        kwargs["gh"] = gh
        return func(*args, **kwargs)

    return wrapped


def retry_on_2fa_failure(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
                break
            except github3.exceptions.AuthenticationFailed:
                otp_cache.invalidate()
        return func(*args, **kwargs)

    return wrapped
