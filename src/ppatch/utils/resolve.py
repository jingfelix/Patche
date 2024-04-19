import typer

from ppatch.config import settings
from ppatch.model import ApplyResult, Change, Hunk, Line
from ppatch.utils.common import find_list_positions


def apply_change(
    changes: list[Change],
    target: list[Line],
    reverse: bool = False,
    flag: bool = False,
    flag_hunk: int = -1,
    fuzz: int = 0,
) -> ApplyResult:
    """Apply a diff to a target string."""

    if fuzz > settings.max_diff_lines or fuzz < 0:
        raise Exception(f"fuzz value should be less than {settings.max_diff_lines}")

    # 如果反向，则交换所有的 old 和 new
    if reverse:
        for change in changes:
            change.old, change.new = change.new, change.old

    # 首先统计 Hunk 数
    hunk_indexes = []
    for change in changes:
        if change.hunk not in hunk_indexes:
            hunk_indexes.append(change.hunk)

    # TODO: 支持 -F 参数
    # 将changes按照hunk分组，注意同一个 hunk 中的 change 要进行分类，前三行要放入前置上下文，中间的要放入中间上下文，后三行要放入后置上下文
    hunk_list: list[Hunk] = []
    conflict_hunk_num_list: list[int] = []
    failed_hunk_list: list[Hunk] = []
    for hunk_index in hunk_indexes:
        hunk_changes = [change for change in changes if change.hunk == hunk_index]

        # 这里遍历的顺序已经是正确的顺序
        hunk_context = []
        hunk_middle = []
        hunk_post = []
        # 首先正向遍历，获取前置上下文
        for change in hunk_changes:
            if change.old is not None and change.new is not None:
                hunk_context.append(change)
            else:
                break

        # 然后反向遍历，获取后置上下文
        for change in reversed(hunk_changes):
            if change.old is not None and change.new is not None:
                hunk_post.append(change)
            else:
                break

        assert len(hunk_context) <= settings.max_diff_lines
        assert len(hunk_post) <= settings.max_diff_lines

        # 最后获取中间代码
        for change in hunk_changes:
            if change not in hunk_context and change not in hunk_post:
                hunk_middle.append(change)

        hunk_context = hunk_context[0 : 3 - fuzz]
        hunk_post = hunk_post[0 : 3 - fuzz]

        # 注意把后置上下文反转回来
        hunk_post = list(reversed(hunk_post))

        hunk_list.append(
            Hunk(
                index=hunk_index,
                context=hunk_context,
                middle=hunk_middle,
                post=hunk_post,
                all_=hunk_changes,
            )
        )

    # 然后对每个hunk进行处理，添加偏移
    changes: list[Change] = []
    for hunk in hunk_list:
        changes_to_search = hunk.context + hunk.middle + hunk.post
        pos_list = find_list_positions(
            [line.content for line in target],
            [change.line for change in changes_to_search if change.old is not None],
        )

        # 初始位置是 context 的第一个
        # 注意，前几个有可能是空
        pos_origin = None
        for change in changes_to_search:
            if change.old is not None:
                pos_origin = change.old
                break

        if pos_origin is None:
            failed_hunk_list.append(hunk)
            # hunk_list.remove(hunk)
            continue

        offset_list = [pos + 1 - pos_origin for pos in pos_list]  # 确认这里是否需要 1？

        if len(offset_list) == 0:
            failed_hunk_list.append(hunk)
            typer.echo(f"Apply failed with hunk {hunk.index}")
            # hunk_list.remove(hunk)
            continue
            # raise Exception("offsets do not intersect")

        # 计算最小 offset
        min_offset = None
        for offset in offset_list:
            if min_offset is None or abs(offset) < abs(min_offset):
                min_offset = offset

        for change in hunk.middle:
            changes.append(
                Change(
                    hunk=change.hunk,
                    old=change.old + min_offset if change.old is not None else None,
                    new=change.new + min_offset if change.new is not None else None,
                    line=change.line,
                )
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

    flag_line_list = []
    add_count = 0
    del_count = 0

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
                    flag=True
                    if flag and (change.hunk == flag_hunk or flag_hunk == -1)
                    else False,
                    hunk=change.hunk,
                ),
            )
            add_count += 1

        elif change.new is None and change.old is not None:
            index = change.old - 1 - del_count + add_count

            # 如果被修改行有标记，则将其添加进标记列表
            if target[index].flag:
                flag_line_list.append(target[index])

            del target[index]
            del_count += 1

            conflict_hunk_num_list.append(change.hunk)

        else:
            # 对其他行也要标记 flag
            index = change.old - 1 - del_count + add_count
            assert index == change.new - 1
            target[index].flag = (
                True
                if flag and (change.hunk == flag_hunk or flag_hunk == -1)
                else target[index].flag
            )

    new_line_list = []
    for index, line in enumerate(target):
        # 判断是否在 Flag 行附近进行了修改
        # 如果该行为 changed，且前后行为flag，则也加入标记列表
        if line.changed and not line.flag:
            if index > 0 and target[index - 1].flag:
                line.flag = True
            if index < len(target) - 1 and target[index + 1].flag:
                line.flag = True

            if line.flag:
                flag_line_list.append(line)
                conflict_hunk_num_list.append(line.hunk)

        new_line_list.append(Line(index=index, content=line.content, flag=line.flag))

    return ApplyResult(
        new_line_list=new_line_list,
        flag_line_list=flag_line_list,
        conflict_hunk_num_list=conflict_hunk_num_list,
        failed_hunk_list=failed_hunk_list,
    )
