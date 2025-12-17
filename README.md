# How Phasors Work

## Development

### Getting Started

Create the Python virtual environment using:

```sh
UV_PROJECT_ENVIRONMENT=.venv uv venv
```

Activate the environment using:

```sh
source .venv/bin/activate
```

The JupyterBook GitHub workflow (`deploy.yml`) requires a traditional `requirements.txt` file. After adding, modifying, or removing a package (using `uv add --active ...` or `uv remove --active ...`), run the following to have the changes reflected in `requirements.txt`:

```sh
uv export --format requirements.txt
```
