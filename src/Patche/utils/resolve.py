from Patche.app import logger
from Patche.config import settings
from Patche.model import ApplyResult, Hunk, Line
from Patche.utils.common import find_list_positions


def apply_change(
    hunk_list: list[Hunk],
    target: list[Line],
    reverse: bool = False,
    flag_hunk_list: list[int] = None,
    fuzz: int = 2,  # set fuzz=2 according GNU Patch
) -> ApplyResult:
    """Apply a diff to a target string."""

    flag_hunk_list = [] if flag_hunk_list is None else flag_hunk_list

    if fuzz > settings.max_diff_lines or fuzz < 0:
        raise Exception(f"fuzz value should be less than {settings.max_diff_lines}")

    if reverse:
        for hunk in hunk_list:
            for change in hunk.context + hunk.middle + hunk.post:
                change.old, change.new = change.new, change.old

    # 然后对每个hunk进行处理，添加偏移
    failed_hunk_list: list[Hunk] = []
    last_pos = None
    for hunk in hunk_list:

        current_hunk_fuzz = 0

        while current_hunk_fuzz <= fuzz:

            # hunk.context = hunk.context[1:]
            # hunk.post = hunk.post[: fuzz - current_hunk_fuzz]

            logger.debug(
                f"current_fuzz: {current_hunk_fuzz} len(hunk.context): {len(hunk.context)} len(hunk.post): {len(hunk.post)}"
            )

            changes_to_search = hunk.context + hunk.middle + hunk.post
            pos_list = find_list_positions(
                [line.content for line in target],
                [change.line for change in changes_to_search if change.old is not None],
            )

            if len(pos_list) != 0:
                break

            current_hunk_fuzz += 1

            if current_hunk_fuzz <= fuzz:
                hunk.context = hunk.context[1:]
                hunk.post = hunk.post[: 3 - current_hunk_fuzz]

        # 初始位置是 context 的第一个
        # 注意，前几个有可能是空
        pos_origin = None
        for change in changes_to_search:
            if change.old is not None:
                pos_origin = change.old
                break

        # TODO: 这里不太对，要想一下怎么处理，不应该是加入 failed hunk list
        # 仅在 -F 3 且只有添加行 的情况下出现（指与 GNU patch 行为不一致）
        # 也可以看一下这样的情况有多少
        if current_hunk_fuzz == fuzz and not pos_origin:
            failed_hunk_list.append(hunk)
            logger.debug(f"Could not determine pos_origin")
            logger.warning(f"Apply failed with hunk {hunk.index}")
            continue

        if len(pos_list) == 0:
            failed_hunk_list.append(hunk)
            logger.debug(f"Could not determine proper position")
            logger.warning(f"Apply failed with hunk {hunk.index}")
            continue

        offset_list = [pos + 1 - pos_origin for pos in pos_list]  # 确认这里是否需要 1？

        # 计算最小 offset
        min_offset = None
        for offset in offset_list:
            if min_offset is None or abs(offset) < abs(min_offset):
                min_offset = offset

        logger.info(
            f"Apply hunk {hunk.index} with offset {min_offset} fuzz {current_hunk_fuzz}"
        )

        # 直接按照 pos 进行替换
        # 选择 offset 最小的 pos
        pos_new = pos_origin + min_offset - 1

        # 处理 pos_new 小于 last_pos 的情况
        logger.debug(f"pos_origin: {pos_origin}, last_pos: {last_pos}")
        if last_pos is None:
            last_pos = pos_new
        elif pos_new < last_pos:
            # 特别主要 pos_new 小于 last_pos 的情况
            logger.warning(f"Apply failed with hunk {hunk.index}")
            logger.error(f"pos: {pos_new} is greater than last_pos: {last_pos}")
            failed_hunk_list.append(hunk)
            continue
        else:
            last_pos = pos_new

        old_lines = [
            change.line
            for change in hunk.context + hunk.middle + hunk.post
            if change.old is not None
        ]
        new_lines = [
            change.line
            for change in hunk.context + hunk.middle + hunk.post
            if change.new is not None
        ]

        # 检查 pos_new 位置的行是否和 old_lines 一致
        for i in range(len(old_lines)):
            if target[pos_new + i].content != old_lines[i]:
                raise Exception(
                    f'line {pos_new + i}, "{target[pos_new + i].content}" does not match "{old_lines[i]}"'
                )

        # 以切片的方式进行替换
        target = (
            target[:pos_new]
            + [
                Line(index=pos_new + i, content=new_lines[i])
                for i in range(len(new_lines))
            ]
            + target[pos_new + len(old_lines) :]
        )

    return ApplyResult(
        new_line_list=target,
        conflict_hunk_num_list=[],
        failed_hunk_list=failed_hunk_list,
    )
