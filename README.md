# Patche

Modern patch, written in Python.

## Config

`patche` loads the configuration from a file named `.patche.env` in `$HOME`.

```shell
max_diff_lines = 3
```

## Development

`patche` uses `pdm` as package manager. To install the dependencies in your workspace, run:

```bash
pdm install --prod

# If you want to trace patche execution
pdm install
```

ref: [PDM Documentation](https://pdm-project.org/en/latest/usage/dependency/)
