# ppatch

A tool to analyze and patches between different Linux Kernel versions.

## Config

`ppatch` loads the configuration from a file named `.ppatch.env` in `$HOME`.

```shell
base_dir = "/home/laboratory/workspace/exps/ppatch" # The base directory to store the patches
patch_store_dir = "_patches" # The directory to store the patches
max_diff_lines = 3
```

By default, base_dir is the base directory where `ppatch` is installed.

## Development

`ppatch` uses `pdm` as package manager. To install the dependencies in your workspace, run:

```bash
pdm install
```

ref: [PDM Documentation](https://pdm-project.org/en/latest/usage/dependency/)
