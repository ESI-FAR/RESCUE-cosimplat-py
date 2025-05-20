# Web application for the RESCUE cosim platform

## Install

```shell
pip install -e .
```

## Configuration

The dashboard is configured using [config.toml](config.toml).

## Usage

Make sure the MySQL database is running.

```shell
flask --app rescue_dashboard run
```

## Development

Format Python code using [ruff](https://docs.astral.sh/ruff/):
```shell
uvx ruff format
# Sort imports with
ruff check --select I --fix
```
Lint Python code:
```shell
uvx ruff check
```

Format Jinja2 templates in `src/rescue_dashboard/templates/**.html.j2` using [djlint](https://djlint.com/):
```shell
uvx djlint --reformat -
```
Lint templates:
```shell
uvx djlint -
```