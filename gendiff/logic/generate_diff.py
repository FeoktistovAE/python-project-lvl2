import json

def bool_to_json(file):
    for i in file.keys():
        if isinstance(file[i], bool):
            file[i] = json.dumps(file[i])
    return file


def generate_diff(path1, path2):
    file1 = bool_to_json(json.load(open(path1)))
    file2 = bool_to_json(json.load(open(path2)))
    file1_set = set(file1.keys())
    file2_set = set(file2.keys())
    only_file1_set = file1_set - file2_set
    only_file2_set = file2_set - file1_set
    files_intersection = file1_set & file2_set
    keys_with_diff_values = set()
    for i in files_intersection:
        if file1[i] != file2[i]:
            keys_with_diff_values.add(i)
    all_keys = list(file1_set | file2_set)
    all_keys.sort()
    output = ''
    for i in all_keys:
        if i in keys_with_diff_values:
            output += f'- {i}: {file1[i]}\n+ {i}: {file2[i]}\n'
        elif i in only_file1_set:
            output += f'- {i}: {file1[i]}\n'
        elif i in only_file2_set:
            output += f'+ {i}: {file2[i]}\n'
        elif i in files_intersection:
            output += f'  {i}: {file1[i]}\n'
    return f'{{\n{output}}}'

