import parse


def test_extract_hash_block():
    t = """# \n# Hey\n# This one is simple\n#  - Right?\n# \nfrom code import test\n\nprint('working')\n"""
    assert parse.extract_hash_block(t) == "Hey\nThis one is simple\n - Right?"

    t = """# \n# Another\n# One.\n# """
    assert parse.extract_hash_block(t) == "Another\nOne."


def test_extract_string_block():
    t = '''"""This\nis\na\ntest"""'''
    assert parse.extract_string_block(t) == "This\nis\na\ntest"

    t = '''from badstuff import first"""Here"""'''
    assert parse.extract_string_block(t) == ""

    t = '''"""\n This\n is\n a\n test\n """'''
    assert parse.extract_string_block(t) == "\n This\n is\n a\n test\n "
