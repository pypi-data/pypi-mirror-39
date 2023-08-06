from argparse import ArgumentParser
import json
import logging

from pastpy.database.database import Database
from pastpy.gen.database.database_configuration import DatabaseConfiguration


class Cli(object):
    def main(self):
        args = self.__parse_args()

        with open(args.configuration_file_path, 'rb') as configuration_file:
            configuration = DatabaseConfiguration.from_builtins(json.load(configuration_file))

        database = Database.create(configuration=configuration)

        if args.command == "download":
            if not hasattr(database, "download"):
                raise ValueError("configured database is not downloadable")
            database.download()
        elif args.command == "parse":
            if not hasattr(database, "download"):
                raise ValueError("configured database is not parseable")
            for object_detail in database.parse_object_details():
                print(object_detail.id)

    def __parse_args(self):
        argument_parser = ArgumentParser()
        argument_parser.add_argument("-c", "--configuration-file-path", default=".pastpy.json")
        argument_parser.add_argument(
            '--debug',
            action='store_true',
            help='turn on debugging'
        )
        argument_parser.add_argument(
            '--logging-level',
            help='set logging-level level (see Python logging module)'
        )

        subparsers = argument_parser.add_subparsers()

        subparser = subparsers.add_parser("download")
        subparser.set_defaults(command="download")

        subparser = subparsers.add_parser("parse")
        subparser.set_defaults(command="parse")

        parsed_args = argument_parser.parse_args()

        if not hasattr(parsed_args, "command"):
            argument_parser.print_usage()
            raise SystemExit(0)

        if parsed_args.debug:
            logging_level = logging.DEBUG
        elif parsed_args.logging_level is not None:
            logging_level = getattr(logging, parsed_args.logging_level.upper())
        else:
            logging_level = logging.INFO
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(lineno)s:%(name)s:%(levelname)s: %(message)s',
            level=logging_level
        )

        return parsed_args


def main():
    Cli().main()
