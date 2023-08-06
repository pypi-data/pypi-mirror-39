import json
import os

import yaml

from ipecac.tools import scan


welcome_message = """
                  Hi there! It looks like you're new around here?
                  In order to get started, I'll need to ask you a
                  few quick questions about your project
                  """
title_input = "What's your project called? (my cool project): "
server_input = "What's the URL of your server? (http://example.com): "


def merge_endpoints(comment_tree):
    """
    All of our comments are grouped together into one big list of dictionary
    objects so we're about ready to start generating our Swagger/OAS
    definition.

    In order to begin, we need to restructure our endpoints so that they match
    the OAS 3.0 paths definition which is roughly as follows:

    paths:
        /path/:
            method:
                description: blah
                responses: blah

    Once that's all done, we also need to do a quick sort so that the
    resulting endpoints are all alphabetically ordered for sanity.

    :param comment_tree: list
    :return: dictionary
    """
    endpoints = dict()
    for item in comment_tree:
        path = item['meta']['path']
        method = item['meta']['method']
        body = item['body']
        if path not in endpoints:
            endpoints[path] = dict()
        endpoints[path][method] = body
    paths = sorted(endpoints.keys())
    sorted_endpoints = dict()
    for path in paths:
        sorted_endpoints[path] = endpoints[path]
    return sorted_endpoints


def build_paths_from_scratch(root=''):
    """
    Wish you could pass a directory to a function and get back a dictionary
    of OAS/Swagger-compatible paths? Well, now you can!

    It also makes things easier to process for my small pea brain :)

    :param root: string
    :return: dictionary
    """
    comments = scan.find_and_parse(root)
    return merge_endpoints(comments)


def create_definition(root=''):
    """
    Given a starting directory, create an entire Swagger/OAS definition!

    :param root: string
    :return: dictionary
    """
    paths = build_paths_from_scratch(root)
    base = read_definition_base(root=root)
    return {**base, 'paths': paths}


def read_definition_base(title=None, server=None, root='', get_input=True):
    """
    There's a few possibilities when it comes to reading the base segment
    used in generating our Swagger/OAS definitions.

    1) The user already has a base stored as a JSON file so we load that
    2) The user already has a base stored as a YAML file so we load that
    3) The user doesn't have a base so we ask them some questions in order
    to build one for them

    The actual input questions are stored behind a boolean purely for
    testing reasons.

    :param root: string
    :param get_input: boolean
    :param title: string
    :param server: string
    :return:
    """
    json_base = f'{root}base.json'
    yaml_base = f'{root}base.yml'
    if os.path.exists(json_base) and os.path.exists(yaml_base):
        error_msg = 'You have two base files. One is JSON and one is YAML. ' \
                    'Please remove one in order for ipecac to work correctly.'
        raise RuntimeError(error_msg)
    if os.path.exists(json_base):
        with open(json_base, 'r') as file:
            return json.loads(file.read())
    if os.path.exists(yaml_base):
        with open(yaml_base, 'r') as file:
            return yaml.load(file)
    if get_input:
        print(welcome_message)
        title = input(title_input)
        server = input(server_input)
    return create_definition_base(title, server)


def create_definition_base(title, server):
    """
    New users won't have any of the required meta information about their
    Swagger/OAS documentation so we can just generate them a base after
    asking some questions.

    For now, just the title and server will be enough. If the user is
    interested enough, they can see examples of valid syntax here:

    https://swagger.io/specification/#infoObject


    :param title: string
    :param server: string
    :return: dictionary
    """
    return {
        'openapi': '3.0.0',
        'info': {
            'version': '1.0.0',
            'title': title
        },
        'servers': [
            {
                'url': server,
                'description': f'The production server for {title}'
            }
        ]
    }
