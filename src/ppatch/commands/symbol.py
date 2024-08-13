from cscopy.cli import CscopeCLI
from cscopy.workspace import CscopeWorkspace

from ppatch.app import app, logger

# 一个新的设计思路：不直接调用作为 command 的函数，将 command 和具体功能区分开
# 写这个临时的 command 的时候可以简单试一下


@app.command("symbol")
def getsymbol_command(
    files: list[str] = [],
    symbols: list[str] = [],
):
    getsymbol(files, symbols)


def getsymbol(files: list[str], symbols: list[str]):
    logger.debug(f"Getting symbols from {files} with {symbols}")

    cli = CscopeCLI("/usr/bin/cscope")

    # 之后还是要按 patch/file/hunk 划分的，这里只是一个临时的 command
    # 解析的思路：先按文件划分，再按每个 hunk 划分
    # DONE 现在需要做的：增强 ppatch 的补丁解析功能，使其能够解析出 diff-hunk-change 三层结构

    with CscopeWorkspace(files, cli) as workspace:
        for symbol in symbols:
            result = workspace.search_c_symbol(symbol)

            for res in result:
                logger.info(f"{res.file}:{res.line} {res.content}")
