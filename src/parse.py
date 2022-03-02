# Functions to parse comment blocks

import os
import re
from typing import List, Tuple, Dict


def extract_hash_block(content: str) -> str:
    """
    Function to extract the text in the top block of # comments so long as the comment is first in string.

    Keyword arguments:
        content -- Text to extract top comment block from
    """
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
    """
    Function to extract the text in the top block of triple quote string comments so long as the triple quote is first in string.

    Keyword arguments:
        content -- Text to extract top comment block from
    """
    content = content.lstrip()
    init_string_block = content.split('"""')[1]
    if content.split('"""')[0] == "":
        return init_string_block
    else:
        return ""


def extract_imports(content: str) -> Dict[str, List[str]]:
    full_imports: List[str] = list()
    conditional_imports: List[Tuple[str, str]] = list()
    import_map: Dict[str, List[str]] = dict()
    for line in content.split("\n"):
        full_imports = full_imports + re.findall(r"^import ([a-zA-Z0-9_.\-]+)\s*", line)
        conditional_imports = conditional_imports + re.findall(
            r"^from ([a-zA-Z0-9_.\-]+) import ([a-zA-Z0-9_.\-]+)\s*", line
        )
    for key, val in conditional_imports:
        import_map[key] = import_map.get(key, []) + [val]
    for full_import in full_imports:
        import_map[full_import] = ["*"]
    return import_map
