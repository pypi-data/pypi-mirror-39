import json

import click
import yaml

from ipecac.tools.generate import create_definition


@click.command()
@click.option('--filetype',
              default='json',
              help='The type of swagger file to generate')
@click.option('--destination',
              default='',
              help='Where do you want your definition saved?')
def create(filetype, destination):
    """
    ipecac is a program for generating a Swagger/OAS definition file from
    comments in your code.
    """
    definition = create_definition()
    if filetype == 'yaml' or filetype == 'yml':
        output = yaml.dump(definition, default_flow_style=False)
        filename = 'swagger.yml'
    if filetype == 'json':
        output = json.dumps(definition, indent=2)
        filename = 'swagger.json'
    if len(destination) != 0 and destination[-1] != '/':
        destination = destination + '/'
    file_path = destination + filename
    with open(file_path, 'w') as file:
        file.write(output)
    print(f'ipecac generated your docs and placed them in {file_path}')


if __name__ == '__main__':
    create()
