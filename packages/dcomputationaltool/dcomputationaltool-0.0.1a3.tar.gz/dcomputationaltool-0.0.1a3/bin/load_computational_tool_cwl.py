import yaml
import django
import argparse

django.setup()

from django import db
from django.core import management

from dcomputationaltool.models import ComputationalTool, ComputationalToolCWLImport
from dcomputationaltool.cwl_utils import insert_computationaltool_inputs
from urllib.request import urlopen


def create_computationaltool(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ComputationalTool.objects.create(**defaults)


def create_computationaltoolcwlimport(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ComputationalToolCWLImport.objects.create(**defaults)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse and insert a CWL tool in the database')
    parser.add_argument('-m', help='Migrate the dcomputationaltool app before inserting', action='store_true',
                        required=False,
                        default=False)
    parser.add_argument('--name', help='Name', required=True)
    parser.add_argument('--cwl', help='CWL location', required=True)
    parser.add_argument('--yml', help='YML location', required=False)
    parser.add_argument('--yml_name', help='YML name', required=False)
    parser.add_argument('--version', help='Version', required=True)
    parser.add_argument('--description', help='Description', required=True)
    parser.add_argument('--url', help='URL', required=True)

    print("Using database: %s on Host: %s as user: %s" % (
        db.connections.databases['default']['NAME'],
        db.connections.databases['default']['HOST'],
        db.connections.databases['default']['USER']
    ))

    args = parser.parse_args()
    migrate = args.m
    name = args.name
    cwl_location = args.cwl
    yml_location = args.yml
    yml_name = args.yml_name
    version = args.version
    description = args.description
    url = args.url

    if migrate:
        management.call_command("makemigrations", "dcomputationaltool")
        management.call_command("migrate", "dcomputationaltool")

    comptool = create_computationaltool(name=name,
                                        version=version,
                                        description=description,
                                        url=url,
                                        cwl=cwl_location)

    if yml_location:
        create_computationaltoolcwlimport(name='Docker YML',
                                          cwl=yml_location,
                                          computationaltool=comptool)

    print('Loading CWL')
    cwl = yaml.load(urlopen(comptool.cwl))
    print('Inserting options')
    insert_computationaltool_inputs(comptool)
