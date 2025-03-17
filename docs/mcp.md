# Patche MCP Example

In `src/Patche/mcp/server` we create a simple MCP server that offers patch utility for LLMs.

## Installation

You can install the MCP server using `pdm` or `pipx`. Make sure you have either of them installed.
```bash
pdm install -G mcp

# or

pipx install patche[mcp]
```

## Usage

To start the MCP server, run the following command in the terminal:
```bash
patche-mcp -r .

# or

python3 -m Patche.mcp -r .
```

## Tools

| Tool | Description | Input | Output | Usage |
|------|-------------|-------|--------|-------|
| **patche_config** | 显示 Patche 的配置信息 | 无需额外参数 | 返回 Patche 配置的 JSON 字符串表示 | 获取当前 Patche 实例的所有配置参数，包括路径、设置和首选项等 |
| **patche_list** | 列出指定目录中所有可用的补丁文件 | `patche_dir` (字符串): 包含补丁文件的目录路径 | 返回一个包含所有补丁文件名的字符串列表，每个文件名占一行 | 快速查看特定目录中有哪些补丁可供使用 |
| **patche_show** | 显示指定补丁文件的详细内容和元数据 | `patch_path` (字符串): 补丁文件的完整路径 | 返回补丁的详细信息，包括: <br>- 补丁文件路径<br>- SHA 哈希值<br>- 作者信息<br>- 创建日期<br>- 提交主题<br>- 所有差异文件的路径信息 | 在应用补丁前检查其内容和影响范围 |
| **patche_apply** | 将指定补丁应用到目标目录 | - `patch_path` (字符串): 补丁文件的完整路径<br>- `target_dir` (字符串): 要应用补丁的目标目录<br>- `reverse` (布尔值, 可选): 是否反向应用补丁，默认为 False | 返回应用补丁的结果信息，成功或失败的详细原因 | 执行补丁应用操作，可以创建新文件、修改现有文件或删除文件 |
