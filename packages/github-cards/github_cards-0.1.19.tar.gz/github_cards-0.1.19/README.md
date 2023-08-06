# GitHub Cards

[![PyPI](https://img.shields.io/pypi/v/github_cards.svg)](https://pypi.python.org/pypi/github_cards)
[![Travis](https://img.shields.io/travis/larsrinn/github_cards.svg)](https://travis-ci.org/larsrinn/github_cards)
[![Documentation Status](https://readthedocs.org/projects/github-cards/badge/?version=latest)](https://github-cards.readthedocs.io/en/latest/?badge=latest)

Convert your GitHub issues into printable cards for your physical Scrum board.

* Free software: MIT license
* Documentation: https://github-cards.readthedocs.io.


## Features

This tool creates a printable HTML-file containing the issues of a GitHub repository.
You can print the file, cut the cards and attach them to your physical Scrum/Kanban board.

To use it, run

```bash
# github_cards REPOSITORY_OWNER REPOSITORY_NAME
>> github_cards pallets click
```

There are some options available, e.g. to access private repositories or only select a certain milestone.

```
>> github_cards --help

Usage: github_cards [OPTIONS] OWNER REPOSITORY

  Console script for github_cards.

Options:
  -u, --username TEXT            Username to perform authenticated requests
                                 with. If provided, the script will request
                                 the password.
  -p, --password TEXT            Password for the username provided. If the
                                 username is set but the password is not
                                 provided, script will request it.
  -m, --milestone-title TEXT     Limit selected issues to a milestone by the
                                 milestone's title. It will search the
                                 repository for that milestone and error if
                                 it's not available.
  -m#, --milestone-number TEXT   Limit selected issue to a milestone by the
                                 milestone's number (similarly to issue
                                 numbers). Will be overwritten by the
                                 milestone title if set.
  -s, --state [all|open|closed]  Limit to all, open or closed issues. Defaults
                                 to open
  -pr, --per-row INTEGER         Number of cards per row
  -pc, --per-column INTEGER      Number of cards per column
  -o, --output PATH              HTML filename to output to. Defaults to a
                                 value containing the repository title and the
                                 current time.
  --help                         Show this message and exit.                     Show this message and exit.

```

### ToDo
* [x] Unspaghettify
* [x] Error handling
* [ ] Add some tests
* [ ] Add documentation
* [ ] Caching of already covered cards
* [ ] User provided templates
* [ ] Authentication
* [ ] List milestones

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.


## History

### 0.1.0 (2018-11-25)

* First release on PyPI.
