import os
from glob import iglob

from ipecac.tools import extract
from ipecac.settings import Constants

IGNORED_DIRS = Constants.IGNORED_DIRS


def detect_comments(root=''):
    """
    This is one of the main core bits of ipecac which is file discovery.

    All it's doing is using globbing to recursively parse from the current
    working directory.

    In order to discover what files are relevant, it has to read the file
    and see if there is any mention of "@api" which is kind of double
    handling, since we have to touch every file but it's kind of unavoidable.

    It's super quick anyway so it's not really a problem.

    We also want to ignore some default directories (xxx.egg-info, test,
    venv) as well as user defined directories that might not be relevant.

    One example is templating. We have a scaffolding service that generates
    ipecac-specific comments and it becomes a recursive thing where the
    template would be picked up if we didn't ignore the directory.

    I thought it was kind of a funny example. Kinda like the project is
    eating itself, huh?

    :param root: string
    :return: list
    """
    files = []
    for file in iglob(f'{root}**/*.py',
                      recursive=True):
        if os.path.isfile(file) and not [i for i in IGNORED_DIRS if i in file]:
            if '@api' in open(file).read():
                files.append(file)
    return files


def find_and_parse(root=''):
    """
    Give me a starting path and I'll dig up all the comments!

    :param root: string
    :return: list
    """
    valid_files = detect_comments(root)
    return extract.get_file_comments(valid_files)
