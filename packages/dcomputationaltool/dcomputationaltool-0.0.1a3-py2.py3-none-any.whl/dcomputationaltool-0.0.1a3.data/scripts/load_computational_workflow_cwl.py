import django
import argparse

django.setup()

from django import db
from django.core import management

from dcomputationaltool.cwl_utils import insert_computationalwf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse and insert a CWL workflow in the database')
    parser.add_argument('-m', help='Migrate the dcomputationaltool app before inserting', action='store_true',
                        required=False,
                        default=False)
    parser.add_argument('--cwl', help='CWL location', required=True)

    print("Using database: %s on Host: %s as user: %s" % (
        db.connections.databases['default']['NAME'],
        db.connections.databases['default']['HOST'],
        db.connections.databases['default']['USER']
    ))

    args = parser.parse_args()
    migrate = args.m
    cwl_location = args.cwl

    if migrate:
        management.call_command("makemigrations", "dcomputationaltool")
        management.call_command("migrate", "dcomputationaltool")

    print('Loading CWL')
    insert_computationalwf(cwl_location)
