import shutil

from ipecac.tools import extract, scan
from test import utils


def test_detect_expected_files():
    sandbox = utils.generate_files()
    base = sandbox['base']
    expected = ['incidents/controller.py', 'hotdogs/doc.py', 'users/fake.py']
    actual = scan.detect_comments(f'{base}/')
    for item in actual:
        assert expected[0] in item or expected[1] in item
        assert expected[2] not in item
    shutil.rmtree(base)


def test_find_and_parse():
    sandbox = utils.generate_files()
    base = sandbox['base']
    files = [
        f'{base}/incidents/controller.py',
        f'{base}/hotdogs/doc.py'
    ]
    controller = open(files[0]).read()
    doc = open(files[1]).read()
    expected = [extract.parse_block(doc), extract.parse_block(controller)]
    actual = scan.find_and_parse(f'{base}/')
    assert expected == actual
    shutil.rmtree(base)
