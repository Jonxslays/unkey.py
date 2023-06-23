# Contributing

Thanks for your interest in unkey.py! Here are some tips for contributing.

## Guidelines

- Code should be [PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.
- Implementations should be well tested before opening a pull request.
- If you have an idea, but are unsure on the proper implementation - open an issue.
- Use informative commit messages.
- Code should be written in [black](https://github.com/psf/black)'s code style.
- Max code line length of 99, max docs line length of 80.

## Installing poetry

Yami uses [Poetry](https://python-poetry.org/) for dependency management.

Check out poetry's full
[installation guide](https://python-poetry.org/docs/master/#installing-with-the-official-installer)
for detailed instructions if you aren't familiar with it.

## Installing dependencies

1) Create a fork of unkey.py, and clone the fork to your local machine.
2) Change directory into the project dir `unkey`.
3) Run `poetry shell` to create a new virtual environment, and activate it.
4) Run `poetry install` to install dependencies (this includes dev deps).

## Writing code

- Check out a new branch to commit your work to, e.g. `git checkout -b bugfix/typing-errors`.
- Make your changes, then run `nox` and address any issues that arise.
- Commit your work, using an informative commit message
- Open a pull request into the master branch of this repository.

After submitting your PR, it will be reviewed (and hopefully merged!).
Thanks again for taking the time to read this contributing guide, and for your
interest in unkey.py. I look forward to working with you.
