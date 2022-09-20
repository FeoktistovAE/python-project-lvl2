import itertools


REPLACER = '  '
SPACES_COUNT = 1


def to_str(content):
    if isinstance(content, bool):
        return (str(content)).lower()
    elif content is None:
        return 'null'
    return str(content)


def render_stylish(content, depth=0):
    deep_indent_size = depth + SPACES_COUNT
    deep_indent = REPLACER * deep_indent_size
    current_indent = REPLACER * depth
    lines = []
    if isinstance(content, dict):
        for key, val in content.items():
            lines.append(f'  {deep_indent}  {key}: {render_stylish(val, deep_indent_size+1)}')
        result = itertools.chain("{", lines, [deep_indent + "}"])
        return "\n".join(result)
    elif not isinstance(content, list):
        return to_str(content)
    for i in content:
        if i['action'] == 'has_child':
            lines.append(
                f'{deep_indent}  {i["key"]}: {render_stylish(i["childrens"], deep_indent_size+1)}'
            )
        elif i['action'] == 'updated':
            lines.append(
                f'{deep_indent}- {i["key"]}: {render_stylish(i["old_value"], deep_indent_size)}'
            )
            lines.append(
                f'{deep_indent}+ {i["key"]}: {render_stylish(i["new_value"], deep_indent_size)}'
            )
        elif i['action'] == 'removed':
            lines.append(
                f'{deep_indent}- {i["key"]}: {render_stylish(i["value"], deep_indent_size)}'
            )
        elif i['action'] == 'added':
            lines.append(
                f'{deep_indent}+ {i["key"]}: {render_stylish(i["value"], deep_indent_size)}'
            )
        elif i['action'] == 'unchanged':
            lines.append(
                f'{deep_indent}  {i["key"]}: {render_stylish(i["value"], deep_indent_size)}'
            )
    result = itertools.chain("{", lines, [current_indent + "}"])
    return "\n".join(result)