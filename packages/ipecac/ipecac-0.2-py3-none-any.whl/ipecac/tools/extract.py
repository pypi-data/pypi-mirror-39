import tokenize

import yaml


def get_block_comments(file):
    """
    Given that we have a file opened, we want to tokenize it. That is, we want
    to iterate through the file and categorise every bit of syntax.

    In our use case, we're only interested in the token_type of 3, which is
    the "type" that block comments are given. On top of that, we're only
    interested in block comments that contain the "@api" indicator.

    This is one of the main core parts of this project, because applied
    recursively to an entire directory, we get everything we need to build
    our Swagger/OAS documentation, aside from some generic parsing bits and
    pieces.

    :param file: <_io.TextIOWrapper> (an opened but unread file)
    :return: list
    """
    comments = list()
    for token_type, token, _, _, _ in tokenize.generate_tokens(file.readline):
        if token_type == 3 and '@api' in token:
            comments.append(token)
    file.close()
    return comments


def separate_block(comment):
    """
    We have a comment but it's not much use as a big chunk of text.

    This function simply strips away the opening and closing comment syntax
    and then splits the first line from the second.

    The meta elements (the first line) needs a bit of splitting up but as for
    the rest, because it's straight YAML, we can just parse the entire block
    without having to clean up or modify anything. Easy!

    :param comment: list
    :return: dictionary
    """
    block = dict()
    comment = comment.replace('"""\n', '').replace('\n"""', '')
    block['meta'] = comment.split('\n')[0]
    block['body'] = '\n'.join(comment.split('\n')[1:])
    return block


def parse_meta(block):
    """
    All we need to do with the meta content is extract the HTTP method and
    endpoint path.

    Originally I uppercased the method here to be consistent with how methods
    are portrayed eg post -> POST but this actually breaks the Swagger/OAS
    spec it seems!

    :param block: string
    :return: dictionary
    """
    meta = block.split(' ')
    return {'method': meta[1], 'path': meta[2]}


def parse_body(block):
    """
    The entire body should be syntactically correct YAML so all we need to do
    is apply the PyYAML library and we get back a nice usable dictionary.

    :param block: string
    :return: dictionary
    """
    return yaml.load(block)


def parse_block(comment):
    """
    This is just a wrapper function that performs everything required to go
    from a comment to a parsed dictionary ready for use in building our
    Swagger/OAS definition

    :param comment: string
    :return: dictionary
    """
    block = separate_block(comment)
    meta = parse_meta(block['meta'])
    body = parse_body(block['body'])
    return {'meta': meta, 'body': body}


def read_comments(file):
    """
    A function that just takes everything in this file and wraps it up into
    a nice little bow.

    Pass it an unread python file and it'll perform everything needed to get
    back a list of parsed comments.

    :param file: <_io.TextIOWrapper> (an opened but unread file)
    :return: list
    """
    comments = get_block_comments(file)
    results = list()
    for comment in comments:
        block = parse_block(comment)
        results.append(block)
    return results


def get_file_comments(files):
    """
    Once we have a list of files that we want to operate on, this function
    iteratively performs everything we need to extract comments from a file.

    We end up with a list of lists (one list for each file) which is a pain
    in the bit so I also do a list comprehension at the end.

    If it looks confusing, all it's doing is turning that list of lists into
    one big list instead.

    :param files: list
    :return: list
    """
    comments = []
    for path in files:
        with open(path, 'r') as file:
            comments.append(read_comments(file))
    return [item for sublist in comments for item in sublist]
