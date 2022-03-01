# Functions to parse comment blocks

import os


def extract_hash_block(content):
    content = content.lstrip().replace("\t", "    ")
    valid_top_lines = list()
    min_init_spaces, init_spaces = len(content[1:]) - len(content[1:].lstrip(" ")), len(content[1:]) - len(content[1:].lstrip(" "))
    for line in content.split("\n"):
        if line[:1] == "#":
            current_spaces = len(line[1:]) - len(line[1:].lstrip(" "))
            min_init_spaces = min(min_init_spaces, current_spaces)
            valid_top_lines.append(line)
        else:
            break
    valid_top_lines = map(lambda s: s[min_init_spaces + 1:], valid_top_lines)
    valid_top_lines = "\n".join(valid_top_lines)
    return " " * (init_spaces - min_init_spaces) + valid_top_lines.strip()


def extract_from_file(file_path):
    with open(file_path, "r") as f:
        pass
