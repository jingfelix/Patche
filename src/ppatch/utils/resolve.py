from ppatch.app import logger
from ppatch.config import settings
from ppatch.model import ApplyResult, Change, Hunk, Line
from ppatch.utils.common import find_list_positions


def apply_change(
    hunk_list: list[Hunk],
    target: list[Line],
    reverse: bool = False,
    flag: bool = False,
    trace: bool = False,
    flag_hunk_list: list[int] = None,
    fuzz: int = 0,
) -> ApplyResult:
    """Apply a diff to a target string."""

    flag_hunk_list = [] if flag_hunk_list is None else flag_hunk_list

    if fuzz > settings.max_diff_lines or fuzz < 0:
        raise Exception(f"fuzz value should be less than {settings.max_diff_lines}")

    # TODO: 注意，修改了该函数后，需要将此处修改为对 hunk 内的 change 进行修改
    if reverse:
        if flag:
            raise Exception("flag is not supported with reverse")

        for hunk in hunk_list:
            for change in hunk.context + hunk.middle + hunk.post:
                change.old, change.new = change.new, change.old

    # 然后对每个hunk进行处理，添加偏移
    changes: list[Change] = []
    failed_hunk_list: list[Hunk] = []
    for hunk in hunk_list:

        current_hunk_fuzz = 0

        while current_hunk_fuzz <= fuzz:

            hunk.context = hunk.context[1:]
            hunk.post = hunk.post[: fuzz - current_hunk_fuzz]

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

        # 如果 reverse 为 True，则直接替换，不进行 flag 追踪
        if reverse:
            # 直接按照 pos 进行替换
            # 选择 offset 最小的 pos
            pos_new = pos_origin + min_offset - 1

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

        else:
            for change in hunk.middle:
                changes.append(
                    Change(
                        hunk=change.hunk,
                        old=change.old + min_offset if change.old is not None else None,
                        new=change.new + min_offset if change.new is not None else None,
                        line=change.line,
                    )
                )

    if reverse:
        return ApplyResult(
            new_line_list=target,
            conflict_hunk_num_list=[],
            failed_hunk_list=failed_hunk_list,
        )

    # 注意这里的 changes 应该使用从 hunk_list 中拼接出来的（也就是修改过行号的）
    for change in changes:
        if change.old is not None and change.line is not None:
            if change.old > len(target):
                raise Exception(
                    f'context line {change.old}, "{change.line}" does not exist in source'
                )
            if target[change.old - 1].content != change.line:
                raise Exception(
                    f'context line {change.old}, "{change.line}" does not match "{target[change.old - 1]}"'
                )

    add_count = 0
    del_count = 0

    conflict_hunk_num_list: list[int] = []
    for change in changes:
        # 只修改新增行和删除行（只有这些行是被修改的）
        if change.old is None and change.new is not None:
            target.insert(
                change.new - 1,
                Line(
                    index=change.new - 1,
                    content=change.line,
                    changed=True,
                    status=True,
                    flag=True if change.hunk in flag_hunk_list and flag else False,
                    hunk=change.hunk,
                ),
            )
            add_count += 1

        elif change.new is None and change.old is not None:
            index = change.old - 1 - del_count + add_count

            # 如果被修改行有标记，则标记将其删除的 hunk
            if target[index].flag:
                conflict_hunk_num_list.append(change.hunk)

            del target[index]
            del_count += 1

        else:
            # 对其他行也要标记 flag
            index = change.old - 1 - del_count + add_count

            try:
                assert index == change.new - 1  # TODO: but why? 44733
            except AssertionError:
                logger.error(
                    f"index: {index}, change.new: {change.new}, hunk: {change.hunk}"
                )

            target[index].flag = (
                True if flag and change.hunk in flag_hunk_list else target[index].flag
            )  # 加点注释解释一下 # TODO: 确认这个条件是否是正确的

    new_line_list: list[Line] = []
    for index, line in enumerate(target):
        # 判断是否在 Flag 行附近进行了修改
        # 如果该行为 changed，且前后行为flag，则也加入标记列表
        if flag and line.changed and not line.flag:
            before_flag = (
                index > 0 and target[index - 1].flag and not target[index - 1].changed
            )
            after_flag = (
                index < len(target) - 1
                and target[index + 1].flag
                and not target[index + 1].changed
            )

            if before_flag or after_flag:
                line.flag = True

            if line.flag:
                conflict_hunk_num_list.append(line.hunk)

            # 当 trace 为 True 时，将所有 conflict hunk 的行都标记为冲突
            if trace and line.hunk in conflict_hunk_num_list:
                line.flag = True

        new_line_list.append(
            Line(index=index, content=line.content, flag=line.flag)
        )  # 注意洗掉 hunk changed

    failed_hunk_list.extend(
        [
            hunk
            for hunk in hunk_list
            if hunk.index in conflict_hunk_num_list and hunk not in failed_hunk_list
        ]
    )

    return ApplyResult(
        new_line_list=new_line_list,
        conflict_hunk_num_list=conflict_hunk_num_list,
        failed_hunk_list=failed_hunk_list,
    )
