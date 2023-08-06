import json
import os
import tempfile

import pytest
import yaml


def load_fixture_read(path):
    with open(f'fixtures/{path}', 'r') as file:
        return file.read()


def load_fixture_unread(path):
    return open(f'fixtures/{path}', 'r')


def load_fixture_json(path):
    file = load_fixture_read(path)
    return json.loads(file)


def load_fixture_yml(path):
    with open(f'fixtures/{path}', 'r') as file:
        return yaml.load(file)


def trim_comment(comment):
    return comment.replace('\n"""', '').replace('"""\n', '')


@pytest.fixture()
def generate_sandbox():
    base = tempfile.TemporaryDirectory().name
    os.mkdir(base)
    return base


@pytest.fixture()
def generate_files():
    folders = ['alerts', 'incidents', 'hotdogs', 'users']
    files = ['poop.md', 'controller.py', 'doc.py', 'fake.py']
    base = tempfile.TemporaryDirectory().name
    os.mkdir(base)
    paths = []
    for folder in folders:
        os.mkdir(f"{base}/{folder}")
    for index, file in enumerate(files):
        item = f'{base}/{folders[index]}/{file}'
        doc_contents = open('fixtures/full_comment.py').read()
        bare_contents = open('fixtures/bare_comment.py').read()
        dummy_contents = 'this is a test file'
        with open(item, 'w') as test_file:
            if file == 'doc.py':
                test_file.write(doc_contents)
            elif file == 'controller.py':
                test_file.write(bare_contents)
            else:
                test_file.write(dummy_contents)
        paths.append(item)
    return {'base': base, 'paths': paths}
