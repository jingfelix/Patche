import logging
import os
import subprocess
from subprocess import CompletedProcess

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

LOG_DIR = "/home/laboratory/workspace/repos/Patche/test_logs"
PATCHES_DIR = "/home/laboratory/workspace/archive/patches"
KERNEL_DIR = "/home/laboratory/workspace/exps/ppatch/linux-stable"

logger = logging.getLogger(__name__)


def test_ppatch_apply(exec: str, poc_index: str) -> int:

    res: CompletedProcess = None

    if exec == "ppatch":
        # ppatch apply -R -F 3 ~/workspace/archive/patches/poc_1005.patch
        res = subprocess.run(
            [
                f"patche",
                "apply",
                "-R",
                "-F",
                "3",
                f"{PATCHES_DIR}/poc_{poc_index}.patch",
            ],
            check=False,
            capture_output=True,
        )

    elif exec == "patch":
        #  patch -R -F 3 -p 1 -f -i ~/workspace/archive/patches/poc_1005.patch && git diff > ../poc_1005.diff && gclean
        res = subprocess.run(
            [
                f"patch",
                "-R",
                "-F",
                "3",
                "-p",
                "1",
                "-f",
                "-i",
                f"{PATCHES_DIR}/poc_{poc_index}.patch",
            ],
            check=False,
            capture_output=True,
        )
    else:
        logger.error("Unknown executable")
        return 2

    # 将 stdout 和 stderr 输出到文件中
    with open(f"{LOG_DIR}/{exec}_apply_{poc_index}_stdout.log", "w") as f:
        f.write(res.stdout.decode("utf-8", errors="ignore"))

    with open(f"{LOG_DIR}/{exec}_apply_{poc_index}_stderr.log", "w") as f:
        f.write(res.stderr.decode("utf-8", errors="ignore"))

    if res.returncode != 0:
        logger.error(f"{exec} apply poc_{poc_index} failed")
        # git restore --stage . && git clean -f -q && git restore .
        # subprocess.run(["git", "clean", "-f", "-q"], check=False)
        subprocess.run(["git", "restore", "."], check=False)

        return 1
    else:
        # 将 git diff 信息输出到文件中
        res = subprocess.run(["git", "diff"], check=True, stdout=subprocess.PIPE)
        with open(f"{LOG_DIR}/{exec}_apply_{poc_index}_diff.log", "w") as f:
            f.write(res.stdout.decode("utf-8", errors="ignore"))

        # subprocess.run(["git", "clean", "-f", "-q"], check=False)
        subprocess.run(["git", "restore", "."], check=False)

        return 0


if __name__ == "__main__":

    # 切换目录到 linux-stable
    os.chdir("/home/laboratory/workspace/exps/ppatch/linux-stable")

    same_poc_list = []
    diff_poc_list = []
    strange_poc_list = []

    poc_index_list = []

    for file in os.listdir(PATCHES_DIR):

        if file.endswith(".patch"):
            poc_index = file.split("_")[1].split(".")[0]
            poc_index_list.append(poc_index)

        else:
            continue

    # 使用排序后的 poc_index_list
    poc_index_list.sort(key=lambda x: int(x))

    for poc_index in poc_index_list:

        ppatch_ret = test_ppatch_apply("ppatch", poc_index)
        patch_ret = test_ppatch_apply("patch", poc_index)

        if not ppatch_ret and not patch_ret:
            # 测试两者的 diff 是否一致
            res = subprocess.run(
                [
                    "diff",
                    f"{LOG_DIR}/ppatch_apply_{poc_index}_diff.log",
                    f"{LOG_DIR}/patch_apply_{poc_index}_diff.log",
                ],
                check=False,
                capture_output=True,
            )

            if res.returncode != 0:
                diff_poc_list.append(poc_index)
                logger.warning(f"poc_{poc_index} diff is different")
            else:
                same_poc_list.append(poc_index)

            continue

        logger.info(f"ppatch_ret: {ppatch_ret}, patch_ret: {patch_ret}")

        if ppatch_ret and not patch_ret:
            diff_poc_list.append(poc_index)
            logger.warning(f"poc_{poc_index} diff is different: ppatch failed")

        elif (not ppatch_ret) and patch_ret:
            diff_poc_list.append(poc_index)
            logger.warning(f"poc_{poc_index} diff is different: patch failed")

        else:
            strange_poc_list.append(poc_index)
            logger.warning(f"poc_{poc_index} diff is strange")

    # 分别将 same_poc_list, diff_poc_list, strange_poc_list 写入文件
    with open(f"{LOG_DIR}/same_poc_list.log", "w") as f:
        f.write("\n".join(same_poc_list))

    with open(f"{LOG_DIR}/diff_poc_list.log", "w") as f:
        f.write("\n".join(diff_poc_list))

    with open(f"{LOG_DIR}/strange_poc_list.log", "w") as f:
        f.write("\n".join(strange_poc_list))
