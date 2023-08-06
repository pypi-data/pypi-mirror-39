from functools import wraps

import click
import github3

from github_cards.otp_cache import OTPCache


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
                two_factor_callback=OTPCache().otp_callback,
            )
        kwargs["gh"] = gh
        return func(*args, **kwargs)

    return wrapped
