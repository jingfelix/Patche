# Patche

Modern patch, written in Python.

## Usage

The following commands are supported:

### apply

Apply a patch to target files.

```shell
patche apply <patch-file>
```

Options:
- `-R, --reverse`: Assume patches were created with old and new files swapped
- `-F, --fuzz LINES`: Set the fuzz factor to LINES for inexact matching

### show

Show details of a patch file.

```shell
patche show <patch-file>
```

### settings

Display current configuration.

```shell
patche settings
```

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
