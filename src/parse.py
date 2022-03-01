# Functions to parse comment blocks

import os


def extract_hash_block(content: str) -> str:
    content = content.lstrip().replace("\t", "    ")
    valid_top_lines = list()
    min_init_spaces, init_spaces = len(content[1:]) - len(content[1:].lstrip(" ")), len(
        content[1:]
    ) - len(content[1:].lstrip(" "))
    for line in content.split("\n"):
        if line[:1] == "#":
            current_spaces = len(line[1:]) - len(line[1:].lstrip(" "))
            min_init_spaces = min(min_init_spaces, current_spaces)
            valid_top_lines.append(line)
        else:
            break
    valid_text = "\n".join(
        map(lambda s: s[min_init_spaces + 1 :], valid_top_lines)
    ).strip()
    return " " * (init_spaces - min_init_spaces) + valid_text


def extract_string_block(content: str) -> str:
    content = content.lstrip()
    init_string_block = content.split('"""')[1]
    if content.split('"""')[0] == "":
        return init_string_block
    else:
        return ""
