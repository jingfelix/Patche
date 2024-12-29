import logging
import os
import time

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True)],
)

logger = logging.getLogger(__name__)


def bench_parse():

    # 创建表格
    table = Table(title="Benchmark Results")
    table.add_column("File Name", style="cyan")
    table.add_column("parse_patch Time", style="green")
    table.add_column("parse_patch_patche Time", style="green")
    table.add_column("parse_patch_pydantic Time", style="green")
    table.add_column("Time Difference patche", style="yellow")
    table.add_column("Percentage", style="red")
    table.add_column("Time Difference pydantic", style="yellow")
    table.add_column("Percentage", style="red")

    from whatthepatch import parse_patch
    from whatthepatch.patch import diffobj
    from whatthepatch_pydantic import parse_patch as parse_patch_pydantic
    from whatthepatch_pydantic.patch import Diff as Diff_pydantic

    from Patche.model import Diff
    from Patche.utils.parse import parse_patch as parse_patch_patche

    time_differences = []
    time_differences_pydantic = []

    time_diffes = []
    time_diffes_patche = []
    time_diffes_pydantic = []

    percentage_diffs_patche = []
    percentage_diffs_pydantic = []

    for patch_file in os.listdir("tests/cases/patches"):
        if not patch_file.split(".")[-1] == "patch":
            continue

        with open(f"tests/cases/patches/{patch_file}", "r") as f:
            patch = f.read()

        try:
            st = time.time()
            diffes: list[diffobj] = []
            for diff in parse_patch(patch):
                diffes.append(diff)
            parse_time = time.time() - st

            st = time.time()
            diffes_patche: list[Diff] = []
            for diff in parse_patch_patche(patch).diff:
                diffes_patche.append(diff)
            parse_patche_time = time.time() - st

            st = time.time()
            diffes_pydantic: list[Diff_pydantic] = []
            for diff in parse_patch_pydantic(patch):
                diffes_pydantic.append(diff)
            parse_pydantic_time = time.time() - st

            time_diff = parse_patche_time - parse_time
            percentage = (parse_patche_time / parse_time - 1) * 100

            time_diff_pydantic = parse_pydantic_time - parse_time
            percentage_pydantic = (parse_pydantic_time / parse_time - 1) * 100

            # 添加数据到表格
            table.add_row(
                patch_file,
                f"{parse_time:.8f}s",
                f"{parse_patche_time:.8f}s",
                f"{parse_pydantic_time:.8f}s",
                f"{time_diff:.8f}s",
                f"{percentage:+.2f}%",
                f"{time_diff_pydantic:.8f}s",
                f"{percentage_pydantic:+.2f}%",
            )

            time_differences.append(time_diff)
            time_differences_pydantic.append(time_diff_pydantic)

            percentage_diffs_patche.append(percentage)
            percentage_diffs_pydantic.append(percentage_pydantic)

            time_diffes.append(parse_time)
            time_diffes_patche.append(parse_patche_time)
            time_diffes_pydantic.append(parse_pydantic_time)

            assert len(diffes) == len(diffes_patche)
            for d1, d2 in zip(diffes, diffes_patche):
                assert len(d1.changes) == len(d2.changes)

        except Exception as e:
            logger.error(f"Error in {patch_file}")

    # 添加统计信息到表格
    table.add_row(
        "Average",
        f"{sum(time_diffes)/len(time_diffes):.8f}s",
        f"{sum(time_diffes_patche)/len(time_diffes_patche):.8f}s",
        f"{sum(time_diffes_pydantic)/len(time_diffes_pydantic):.8f}s",
        f"{sum(time_differences) / len(time_differences):.8f}s",
        f"{sum(percentage_diffs_patche) / len(percentage_diffs_patche):+.2f}%",
        f"{sum(time_differences_pydantic)/len(time_differences_pydantic):.8f}s",
        f"{sum(percentage_diffs_pydantic)/len(percentage_diffs_pydantic):+.2f}%",
    )

    # 显示表格
    console = Console()
    console.print(table)


if __name__ == "__main__":
    bench_parse()
