# yo

A powerful self customizable cli.

## Installation

```bash
pip install my-yo
```

## Get started

```
yo --help

Usage: yo [OPTIONS] COMMAND [ARGS]...

   __   __  _______
  |  | |  ||       |
  |  |_|  ||   _   |
  |       ||  | |  |
  |_     _||  |_|  |
    |   |  |       |
    |___|  |_______|  Make life easy.


Options:
  --version      Show the version and exit.
  -v, --verbose  Enables verbose mode.
  --help         Show this message and exit.

Commands:
  bb       commands to work with bitbucket.
```

## Setup development environment

```
python -m venv venv
.\venv\Scripts\activate
```

## Install dependencies

```
pip install -r requirements.txt
```

## Build your features and test it

```
pip install -e .
yo check now
```

## Contribution guide

1.	Must send PR to master branch for merge
2.	Update `CHANGELOG.md` for your change
3.	Add your ideas to `TODO.md`, remove it once done
4.	Should have meaningful commit message
5.	Following existed coding style, don’t worry about it, I will review
6.	Unit test your feature as much as possible