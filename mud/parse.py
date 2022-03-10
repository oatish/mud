"""
Module to extract information about local modules
"""

from dataclasses import dataclass, field
from glob import glob
import os
from pathlib import Path
import re
from typing import List, Tuple, Dict, Union


@dataclass
class ModuleInfo:
    """
    Dataclass to hold all needed information about a local module

    Keyword arguments:
        name -- Name of module
        internal_mods -- Dictionary mapping module name to methods used for local modules
        external_mods -- Dictionary mapping module name to methods used for external modules
        description -- Description of module
        path -- Module path
    """

    name: str
    internal_mods: Dict[str, List[str]] = field(default_factory=dict)
    external_mods: Dict[str, List[str]] = field(default_factory=dict)
    description: str = ""
    path: str = ""


def extract_hash_block(content: str) -> str:
    """
    Function to extract the text in the top block of # comments so long as the comment is first in string.

    Keyword arguments:
        content -- Text to extract top comment block from
    """
    if content:
        content = content.lstrip().replace("\t", "    ")
        valid_top_lines = []
        min_init_spaces, init_spaces = len(content[1:]) - len(
            content[1:].lstrip(" ")
        ), len(content[1:]) - len(content[1:].lstrip(" "))
        for line in content.split("\n"):
            if len(line) > 1:
                if line[:1] == "#":
                    current_spaces = len(line[1:]) - len(line[1:].lstrip(" "))
                    min_init_spaces = min(min_init_spaces, current_spaces)
                    valid_top_lines.append(line)
                else:
                    break
        valid_text = "\n".join(
            map(lambda s: s[min_init_spaces + 1:], valid_top_lines)
        ).strip()
        return " " * (init_spaces - min_init_spaces) + valid_text
    return ""


def extract_string_block(content: str) -> str:
    """
    Function to extract the text in the top block of triple quote string comments so long as the triple quote is first in string.

    Keyword arguments:
        content -- Text to extract top comment block from
    """
    if content:
        content = content.lstrip()
        separated = content.split('"""')
        if len(separated) > 1:
            init_string_block = separated[1]
            if separated[0] == "":
                return init_string_block.strip()
            return ""
        return ""
    return ""


def extract_comment_block(content: str) -> str:
    """
    Utility function to parse any comment black regardless of type
    """
    if content.strip()[0] == "#":
        return extract_hash_block(content)
    return extract_string_block(content)


def extract_base_module(key: str, base_modules: bool) -> str:
    """
    Utility function to extract base module from module import

    Keyword arguments:
        key -- Module name to parse
        base_modules -- True if parsing for base module, False otherwise
    """
    if base_modules:
        return key.split(".")[0]
    return key


def extract_imports(content: str, base_modules: bool = True) -> Dict[str, List[str]]:
    """
    Function to extract module names from import statements in a text

    Keyword arguments:
        content -- Text to extract imported module names from
        base_modules -- True to extract just base module names, False otherwise
    """
    import_map: Dict[str, List[str]] = {}
    for line in content.split("\n"):
        relative_imports = re.findall(r"from \.+ import ([a-zA-Z0-9_.\-]+)\s*", line)
        conditional_import_re = re.findall(
            r"from \.*([a-zA-Z0-9_.\-]+) import ([a-zA-Z0-9_.\-,\s]+)", line
        )
        full_imports_re = re.findall(r"import ([a-zA-Z0-9_.\-]+)\s*", line)
        if conditional_import_re:
            current_val = import_map.get(conditional_import_re[0][0], [])
            if "*" not in current_val:
                import_map[
                    extract_base_module(conditional_import_re[0][0], base_modules)
                ] = current_val + conditional_import_re[0][1].split(", ")
        elif full_imports_re:
            import_map[extract_base_module(full_imports_re[0], base_modules)] = ["*"]
        elif relative_imports:
            import_map[extract_base_module(relative_imports[0], base_modules)] = ["*"]
    return import_map


def infer_local_code_files(
    glob_pattern: str = ".",
    recursive: bool = True,
    excluded: Tuple = (),
    included: Tuple = (),
) -> List[str]:
    """
    Function to find all internal modules that can be called.

    Keyword arguments:
        glob_pattern -- Starting folder or glob pattern
        recursive -- True to glob all files recursively
        excluded -- Tuple containing files to be explicitly excluded
        included -- Tuple containing all files to be included.  Overrides glob_pattern if non-empty
    """
    modules: List[str] = []
    if included:
        file_iter = included
    elif recursive:
        file_iter = tuple(Path(glob_pattern).rglob("*.py"))
    else:
        file_iter = tuple(glob(glob_pattern + "*.py"))
    for module in file_iter:
        if os.path.basename(module) not in excluded:
            print(f"[info] inferring module {module}")
            if not re.findall(r"__([a-zA-Z0-9_.\-]+)__.py", os.path.basename(module)):
                modules.append(module)
    return modules


def infer_local_modules(
    base_dir: str = ".",
) -> List[str]:
    """
    Function to find all internal modules that can be called.

    Keyword arguments:
        base_dir -- Base directory to start walk looking for Python modules
    """
    modules: List[str] = []
    for p, d, f in os.walk(base_dir):
        if "__init__.py" in f:
            modules.append(os.path.basename(p))
    return modules


def infer_module_name(module_path: str) -> str:
    """
    Utility function to convert a path into the importable name of the module.
    """
    return os.path.basename(module_path).split(".")[0]


def extract_module_info(
    module_path: str, local_modules: Union[List[str], None] = None
) -> ModuleInfo:
    """
    Function to create a ModuleInfo dataclass for a given module path.

    Keyword arguments:
        module_path -- File path to the module info is to be extracted from
        local_modules -- List of all local modules to be included.  If None, includes only module_path
    """
    if local_modules is None:
        local_modules = [module_path]
    local_module_names = [infer_module_name(f) for f in local_modules]
    module_name = infer_module_name(module_path)
    with open(module_path, "r") as f:
        content = f.read()
    if content:
        module_description = extract_comment_block(content)
        modules_imported = extract_imports(content)
        local_modules_imported = {
            k: v for k, v in modules_imported.items() if k in local_module_names
        }
        external_modules_imported = {
            k: v for k, v in modules_imported.items() if k not in local_module_names
        }
        return ModuleInfo(
            module_name,
            local_modules_imported,
            external_modules_imported,
            module_description,
            os.path.relpath(module_path),
        )
    return ModuleInfo(module_name, path=module_path)


def infer_modules_info(
    glob_pattern: str = ".",
    recursive: bool = True,
    excluded: Tuple = (),
    included: Tuple = (),
) -> Dict[str, ModuleInfo]:
    """
    Function to infer all local modules and extract model info for all of them.

    Keyword arguments:
        glob_pattern -- Starting folder or glob pattern
        recursive -- True to glob all files recursively
        excluded -- Tuple containing files to be explicitly excluded
        included -- Tuple containing all files to be included.  Overrides glob_pattern if non-empty
    """
    local_modules = infer_local_code_files(glob_pattern, recursive, excluded, included)
    return {
        infer_module_name(module): extract_module_info(module, local_modules)
        for module in local_modules
    }
