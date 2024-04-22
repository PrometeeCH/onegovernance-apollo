Commitizen

poetry run pre-commit install --hook-type commit-msg

# Getting started

1. You need poetry installed on your machine
2. Clone the repo
3. In `src` change `your_package` to the name of your choice
4. In `pyproject.toml`, at line 7, change `your_package` to the name of your choice
4. Run `poetry install`
5. Run `poetry run doit install_precommit`
