from test import utils

import shutil

import pytest

from ipecac.tools import generate, scan

CURR_DIR = utils.CURR_DIR


def test_merge_endpoints():
    fixture = [
        {'meta': {'method': 'post', 'path': '/incidents/'},
         'body': {'description': 'nice'}},
        {'meta': {'method': 'delete', 'path': '/incidents/'},
         'body': {'description': 'cool'}},
        {'meta': {'method': 'get', 'path': '/alerts'},
         'body': {'description': 'hmm'}}
    ]
    expected = {
        '/alerts': {
            'get': {'description': 'hmm'}
        },
        '/incidents/': {
            'delete': {'description': 'cool'},
            'post': {'description': 'nice'}
        }
    }
    actual = generate.merge_endpoints(fixture)
    assert expected == actual


def test_create_definition_base_from_scratch():
    expected = {
        'openapi': '3.0.0',
        'info': {
            'version': '1.0.0',
            'title': 'Pavement Hotdogs'
        },
        'servers': [
            {
                'url': 'http://example.com',
                'description': 'The production server for Pavement Hotdogs'
            }
        ]
    }
    actual = generate.create_definition_base(title="Pavement Hotdogs",
                                             server="http://example.com")
    assert expected == actual


def test_build_paths_from_scratch():
    sandbox = utils.generate_files()
    base = sandbox['base']
    comments = scan.find_and_parse(f'{base}/')
    expected = generate.merge_endpoints(comments)
    actual = generate.build_paths_from_scratch(f'{base}/')
    assert expected == actual
    shutil.rmtree(base)


def test_read_definition_base_scratch():
    expected = {
        'openapi': '3.0.0',
        'info': {
            'version': '1.0.0',
            'title': 'Pavement Hotdogs'
        },
        'servers': [
            {
                'url': 'http://example.com',
                'description': 'The production server for Pavement Hotdogs'
            }
        ]
    }
    actual = generate.read_definition_base(title='Pavement Hotdogs',
                                           server='http://example.com',
                                           get_input=False)
    assert expected == actual


def test_read_definition_from_json():
    expected = utils.load_fixture_json('base.json')
    base = utils.generate_sandbox()
    shutil.copyfile(f'{CURR_DIR}/fixtures/base.json', f'{base}/base.json')
    actual = generate.read_definition_base(root=f'{base}/')
    assert actual == expected
    shutil.rmtree(base)


def test_read_definition_from_yml():
    expected = utils.load_fixture_yml('base.yml')
    base = utils.generate_sandbox()
    shutil.copyfile(f'{CURR_DIR}/fixtures/base.yml', f'{base}/base.yml')
    actual = generate.read_definition_base(root=f'{base}/')
    assert actual == expected
    shutil.rmtree(base)


def test_read_definition_json_and_yml():
    base = utils.generate_sandbox()
    shutil.copyfile(f'{CURR_DIR}/fixtures/base.yml', f'{base}/base.yml')
    shutil.copyfile(f'{CURR_DIR}/fixtures/base.json', f'{base}/base.json')
    with pytest.raises(RuntimeError):
        generate.read_definition_base(root=f'{base}/')


def test_create_definition():
    full_comment = utils.load_fixture_json('full_comment.json')
    base = utils.load_fixture_yml('base.yml')
    paths = generate.merge_endpoints([full_comment])
    expected = {**base, 'paths': paths}
    base = utils.generate_sandbox()
    shutil.copyfile(f'{CURR_DIR}/fixtures/base.yml', f'{base}/base.yml')
    shutil.copyfile(f'{CURR_DIR}/fixtures/full_comment.py', f'{base}/full_comment.py')
    actual = generate.create_definition(f'{base}/')
    assert expected == actual
    shutil.rmtree(base)
