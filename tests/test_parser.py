import parse


def test_extract_hash_block():
    t = """# \n# Hey\n# This one is simple\n#  - Right?\n# \nfrom code import test\n\nprint('working')\n"""
    assert parse.extract_hash_block(t) == "Hey\nThis one is simple\n - Right?"

    t = """# \n# Another\n# One.\n# """
    assert parse.extract_hash_block(t) == "Another\nOne."