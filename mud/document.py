"""
Module to convert extracted info into formatted text
"""

from typing import List, Tuple, Dict
from parse import ModuleInfo


def document_module_md(module_info: ModuleInfo) -> str:
    doc_lines: List = []
    doc_lines.append("## " + module_info.name.capitalize())
    if module_info.description:
        doc_lines.append("> " + module_info.description)
    if module_info.internal_mods:
        doc_lines.append("#### Internal Modules")
        for internal_module in module_info.internal_mods:
            doc_lines.append(" * " + internal_module)
    if module_info.external_mods:
        doc_lines.append("#### External Modules")
        for external_module in module_info.external_mods:
            doc_lines.append(" * " + external_module)
    return "\n".join(doc_lines)


def document_all_md(
    modules: Dict[str, ModuleInfo],
    title: str = "",
    excluded: Tuple = tuple(),
    description=str,
) -> str:
    combined_doc: List[str] = [f"# {title}"] if title else [""]
    if description:
        combined_doc.append(description + "\n")
        combined_doc.append("------")
    for module_name, module in modules.items():
        if module_name not in excluded:
            print(f"[info] documenting module {module_name}")
            combined_doc.append("------")
            combined_doc.append(document_module_md(module))
            combined_doc.append("------")
    return "\n".join(combined_doc)
