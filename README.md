<div align="center">
    <h1>Patche</h1>
    <h3>Modern patch, written in Python.</h3>
    <div>English | <a href="README.zh-CN.md">简体中文</a></div>
    <br>
    <a href="https://pypi.org/project/Patche/"><img src="https://img.shields.io/pypi/v/Patche" alt="PyPI"></a>
    <!-- <a href="https://pypi.org/project/Patche/"><img src="https://img.shields.io/pypi/pyversions/Patche" alt="PyPI - Python Version"></a> -->
    <a href="https://github.com/jingfelix/Patche/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/Patche" alt="PyPI - License"></a>
    <a href="https://pdm-project.org"><img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed"></a>
</div>

## 🔨 Usage

The following commands are supported:

### ➡️ patche apply

Apply a patch to target files.

```shell
patche apply <patch-file>
```

Options:
- `-R, --reverse`: Assume patches were created with old and new files swapped
- `-F, --fuzz LINES`: Set the fuzz factor to LINES for inexact matching

### ↕️ patche show

Show details of a patch file.

```shell
patche show <patch-file>
```

### ⚙️ patche settings

Display current configuration.

```shell
patche settings
```

## 🧰 Config

`patche` loads the configuration from a file named `.patche.env` in `$HOME`.

```shell
max_diff_lines = 3
```

## 💻 Development

`patche` uses `pdm` as package manager. To install the dependencies in your workspace, run:

```bash
pdm install --prod

# If you want to trace patche execution
pdm install
```

ref: [PDM Documentation](https://pdm-project.org/en/latest/usage/dependency/)
