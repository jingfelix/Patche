<div align="center">
    <h1>Patche</h1>
    <h3>Python 编写的现代补丁工具</h3>
    <div><a href="README.md">English</a> | 简体中文</div>
    <br>
    <a href="https://pypi.org/project/Patche/"><img src="https://img.shields.io/pypi/v/Patche" alt="PyPI"></a>
    <a href="https://github.com/jingfelix/Patche/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/Patche" alt="PyPI - License"></a>
    <a href="https://pdm-project.org"><img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed"></a>
</div>

## 🔨 使用方法

支持以下命令：

### ➡️ patche apply

将补丁应用到目标文件。

```shell
patche apply <patch-file>
```

选项：
- `-R, --reverse`: 假设补丁文件在创建时新旧文件被交换
- `-F, --fuzz LINES`: 为不精确匹配设置模糊行数 LINES

### ↕️ patche show

显示补丁文件的详细信息。

```shell
patche show <patch-file>
```

### ⚙️ patche settings

显示当前配置。

```shell
patche settings
```

## 🧰 配置

`patche` 从 `$HOME` 目录下的 `.patche.env` 文件加载配置。

```shell
max_diff_lines = 3
```

## 💻 开发

`patche` 使用 `pdm` 作为包管理器。要在工作空间中安装依赖项，请运行：

```bash
pdm install --prod

# 如果你想追踪 patche 的执行过程
pdm install
```

参考：[PDM 文档](https://pdm-project.org/en/latest/usage/dependency/)
