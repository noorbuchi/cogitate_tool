
![Cogitate Logo](/images/logo.png)
[![Build Status](https://travis-ci.com/GatorCogitate/cogitate_tool.svg?branch=master)](https://travis-ci.com/GatorCogitate/cogitate_tool)
[![codecov](https://codecov.io/gh/GatorCogitate/cogitate_tool/branch/master/graph/badge.svg)](https://codecov.io/gh/GatorCogitate/cogitate_tool)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-orange.svg)](https://www.python.org/)

# About GatorCogitate

Cogitate is a free and open source tool written in Python. It is designed to
evaluate the level of contributions for members of a GitHub repository. GatorCogitate
generates a score for members based on a variety of metrics including:

- Lines added
- Lines removed
- Lines Deleted
- Pull Requests
- Issue Tracker
- Teamwork Performance

These metrics are combined into an overall score for the user.

*Note: This tool is alpha software. Please contact us if you intend to run it in
production.*

## Installing GatorCogitate

**1. Clone the GatorCogitate source code onto your machine.**

With HTTPS:

```
git clone https://github.com/GatorCogitate/cogitate_tool.git
```

Or with SSH:

```
git clone git@github.com:GatorCogitate/cogitate_tool.git
```

**2. Install Pipenv (Recommended)**
Documentation for installing pipenv can be found [Here.](https://pipenv.kennethreitz.org/en/latest/#install-pipenv-today)
After pulling the repo, use `pipenv shell` in `cogitate_tool/` to enter the virtual
environment. Use `exit` to exit. Under the virtual environment, use
`pipenv install <package_name> --dev` to install new packages for development.

Here is a good [tutorial](https://realpython.com/pipenv-guide/) on how to use `pipenv`.

Otherwise, all dependencies will need to be installed locally with the commands:

```
python3 -m pip install --upgrade pip
python3 -m pip install -e
```

## Running GatorCogitate

Run the command `pipenv python run src/cogitate.py` in the root directory.
When prompted, press `Enter` to leave the repository path as default.

*Note: Any users that do not wish to develop the tool can stop reading here.*

### Development Info

#### 2.1 How To Install Packages

When under development, always install the virtual environment first by using
`pipenv install --dev`, then run the developing program by using
`pipenv run python program_name`.

#### 2.2 How to setup scripts

The purpose of script is to automate the running or testing process. To make the
scripts take effect, add the following code to the `Pipfile`:

```
[scripts]
command_name = "./scripts/script_name.sh"
```

Here the `command_name` is the command you want to use when running the project.
For example, if the `command_name` is `cogitate`, the we can use `pipenv run cogitate`.

### 3. CLI

The [homepage](https://docs.python.org/3/howto/argparse.html) for `argparse`.

- `-l` or `--link` Cogitate a repo by the url of the repo.
- `-t` or `--token` Github user token.
- `-r` or `--repo` User's repository.
- `-s` or `--state` State of the issue.

### 4. PyDriller

The [homepage](https://github.com/ishepard/pydriller) and [documentation](https://pydriller.readthedocs.io/en/latest/intro.html)
for `PyDriller`.

The available attributes can be found at their homepage.

## Steps to print out table

- Must be in the `cogitate_tool` folder.
- Before you run the program make sure you have installed the dev packages.
- Run the following command `pipenv run python src/data_collection.py`
- Enter your user token to collect PyGitHub data.
- Enter repo name in this format: org/repo_name.
- After table prints: Enter username to be merged then deleted.
- (This is if you have two usernames within the table and want to combine them.)
- Select yes or no if you would like to continue working with the graph.
