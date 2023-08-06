from test import utils
from ipecac.tools import extract


def test_get_file_comments_bare():
    expected = ['"""\n@api get /incidents/\n'
                'description: Get some stuff about incidents\n"""']
    fixture = utils.load_fixture_unread('bare_comment.py')
    actual = extract.get_block_comments(fixture)
    assert expected == actual


def test_get_file_comments_full():
    comment = utils.load_fixture_read('full_comment.py')
    expected = [f'{comment}']
    fixture = utils.load_fixture_unread('full_comment.py')
    actual = extract.get_block_comments(fixture)
    assert expected == actual


def test_get_file_comments_none_found():
    expected = list()
    fixture = utils.load_fixture_unread('ignore_comment.py')
    actual = extract.get_block_comments(fixture)
    assert expected == actual


def test_separate_block():
    fixture = utils.load_fixture_read('bare_comment.py')
    expected = {'meta': '@api get /incidents/',
                'body': 'description: Get some stuff about incidents'}
    actual = extract.separate_block(fixture)
    assert expected == actual


def test_separate_block_full():
    fixture = utils.load_fixture_read('full_comment.py')
    expected_meta = utils.trim_comment(fixture)[0:21]
    expected_body = utils.trim_comment(fixture)[22:]
    expected = {'meta': expected_meta, 'body': expected_body}
    actual = extract.separate_block(fixture)
    assert expected == actual


def test_parse_meta():
    expected = {'method': 'post', 'path': '/incidents/'}
    actual = extract.parse_meta('@api post /incidents/')
    assert expected == actual


def test_parse_body():
    expected = {'description': 'GET'}
    actual = extract.parse_body('description: GET')
    assert expected == actual


def test_parse_block():
    expected = utils.load_fixture_json('bare_comment.json')
    fixture = utils.load_fixture_read('bare_comment.py')
    actual = extract.parse_block(fixture)
    assert expected == actual


def test_parse_block_full():
    expected = utils.load_fixture_json('full_comment.json')
    fixture = utils.load_fixture_read('full_comment.py')
    actual = extract.parse_block(fixture)
    assert expected == actual


def test_read_comments():
    expected = utils.load_fixture_json('bare_comment.json')
    fixture = utils.load_fixture_unread('bare_comment.py')
    actual = extract.read_comments(fixture)
    assert [expected] == actual


def test_read_comments_full():
    expected = utils.load_fixture_json('full_comment.json')
    fixture = utils.load_fixture_unread('full_comment.py')
    actual = extract.read_comments(fixture)
    assert [expected] == actual


def test_get_file_comments():
    sandbox = utils.generate_files()
    base = sandbox['base']
    files = [
        f'{base}/incidents/controller.py',
        f'{base}/hotdogs/doc.py'
    ]
    controller = open(files[0]).read()
    doc = open(files[1]).read()
    expected = [extract.parse_block(controller), extract.parse_block(doc)]
    actual = extract.get_file_comments(files)
    assert expected == actual
