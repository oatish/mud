import document
from parse import ModuleInfo, extract_module_info


def test_document_module_md():
    module_info = ModuleInfo(
        name="parse",
        internal_mods={"dog": ["bark", "chow"]},
        external_mods={
            "dataclasses": ["dataclass", "field"],
            "glob": ["glob"],
            "os": ["*"],
            "pathlib": ["Path"],
            "re": ["*"],
            "typing": ["List", "Tuple", "Dict", "Union"],
            "statements": ["*"],
        },
        description="Just a test module.",
    )
    module_md = document.document_module_md(module_info)
    expected = """## Parse\n> Just a test module.\n#### Internal Modules\n * dog\n#### External Modules\n * dataclasses\n * glob\n * os\n * pathlib\n * re\n * typing\n * statements"""
    assert module_md == expected


def test_document_all_md(module_extra, module_simple):
    extra = extract_module_info(module_extra)
    simple = extract_module_info(module_simple)
    modules = {"extra": extra, "simple": simple}
    expected = """# Test Library\nThis is just a test.\n\n## Extra\n> Test file\nDescription of test file\n#### External Modules\n * pets\n * toys\n\n## Simple\n> Simple test module.\n#### External Modules\n * cats\n"""
    actual = document.document_all_md(
        modules, "Test Library", description="This is just a test."
    )
    assert actual == expected
