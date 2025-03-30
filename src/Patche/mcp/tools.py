import os

from Patche.app import logger
from Patche.config import settings
from Patche.mcp.model import PatcheApply, PatcheConfig, PatcheList, PatcheShow
from Patche.model import File
from Patche.utils.parse import parse_patch
from Patche.utils.resolve import apply_change


def patche_config() -> str:
    """
    Show the config of patche
    """
    return settings.model_dump_json()


def patche_list(patche_dir: str) -> str:
    """
    List all the patches in the directory
    """
    pass

    patches: list[str] = []

    for file in os.listdir(patche_dir):
        if file.endswith(".patch"):
            patches.append(file)

    return "\n".join(patches)


def patche_show(patch_path: str) -> str:
    """
    Show the patch
    """

    if not os.path.exists(patch_path):
        err = f"Warning: {patch_path} not found!"
        logger.error(err)
        return err

    content = ""
    with open(patch_path, mode="r", encoding="utf-8") as (f):
        content = f.read()

    patch = parse_patch(content)

    result = []
    result.append(f"Patch: {patch_path}")
    result.append(f"Sha: {patch.sha}")
    result.append(f"Author: {patch.author}")
    result.append(f"Date: {patch.date}")
    result.append(f"Subject: {patch.subject}")

    for diff in patch.diff:
        result.append(f"Diff: {diff.header.old_path} -> {diff.header.new_path}")

    return "\n".join(result)


def patche_apply(patch_path: str, target_dir: str, reverse: bool = False) -> str:
    """
    Apply the patch
    """

    # Change dir to target_dir
    os.chdir(target_dir)
    logger.info(f"Changing directory to {target_dir}")
    logger.info(f"Applying patch: {patch_path}")

    # Maybe we can just catch typer.Exit() and return the error message?
    if not os.path.exists(patch_path):
        logger.error(f"Warning: {patch_path} not found!")
        return f"Error: patch {patch_path} not found!"

    if reverse:
        logger.info("Reversing patch...")

    has_failed = False

    with open(patch_path, mode="r", encoding="utf-8") as (f):
        diffes = parse_patch(f.read()).diff

        for diff in diffes:

            old_filename = diff.header.old_path
            new_filename = diff.header.new_path
            if reverse:
                old_filename, new_filename = new_filename, old_filename

            logger.debug(f"old_filename: {old_filename} new_filename: {new_filename}")

            if old_filename == "/dev/null":
                # 根据 diffes 创建新文件
                try:
                    assert len(diff.hunks) == 1

                    new_line_list = []
                    for line in diff.changes:

                        assert line.old is None
                        new_line_list.append(line)

                    with open(new_filename, mode="w+", encoding="utf-8") as f:
                        for line in new_line_list:
                            f.write(line.content + "\n")

                except AssertionError:
                    err = "Failed to create new file: invalid diff!"
                    logger.error(err)
                    return err

            elif new_filename == "/dev/null":
                # 移除 old_filename
                if os.path.exists(old_filename):
                    os.remove(old_filename)
                else:
                    err = f"{old_filename} not found!"
                    logger.error(err)
                    return err

            else:
                if os.path.exists(old_filename):

                    logger.info(f"Applying patch to {old_filename}...")

                    new_line_list = File(file_path=old_filename).line_list
                    apply_result = apply_change(
                        diff.hunks,
                        new_line_list,
                        reverse=reverse,
                        fuzz=3,  # Should be a config option?
                    )
                    new_line_list = apply_result.new_line_list

                    # 检查失败数
                    for failed_hunk in apply_result.failed_hunk_list:
                        has_failed = True
                        logger.error(f"Failed hunk: {failed_hunk.index}")
                else:
                    err = f"{old_filename} not found!"
                    logger.error(err)
                    return err

                # 写入文件
                if not has_failed:
                    with open(new_filename, mode="w+", encoding="utf-8") as f:
                        for line in new_line_list:
                            if line.status:
                                f.write(line.content + "\n")

    if has_failed:
        err = "Error: Failed to apply patch! Please check the log for details."
        logger.error(err)
        return err
    else:
        info = "Patch applied successfully!"
        logger.info(info)
        return info
