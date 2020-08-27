import argparse
import os
from dataclasses import InitVar, dataclass, field
from typing import Any

from sqldiffer import __version__
from sqldiffer.db.credential import Credential
from sqldiffer.exceptions import InvalidDbCredentialError


@dataclass
class CliOption:
    server1: InitVar[str]
    server2: InitVar[str]

    auto_increment: bool
    charset: bool
    output_dir: str

    source: Credential = field(init=False)
    target: Credential = field(init=False)

    def __post_init__(self, server1: str, server2: str) -> None:
        if (cred1 := Credential.parse(server1)) is None \
                or (cred2 := Credential.parse(server2)) is None:
            raise InvalidDbCredentialError()
        self.source = cred1
        self.target = cred2


def get_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        prog='sqldiffer',
        allow_abbrev=False,
        description='Check the difference of MySQL schema (CREATE TABLE)'
    )


def setup_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--server1',
        required=True,
        help='''Comparison source.
        [Format] user:password@host:port/database
        '''
    )

    parser.add_argument(
        '--server2',
        required=True,
        help='''Comparison target.
        [Format] user:password@host:port/database
        '''
    )

    parser.add_argument(
        '-o', '--output-dir',
        dest='output_dir',
        default=os.getcwd(),
        help='Directory to save files. Default is current directory.'
    )

    parser.add_argument(
        '--skip-auto-increment',
        action='store_true',
        dest='auto_increment',
        help='Whether to ignore the difference of "AUTO_INCREMENT=[0-9]+"'
    )

    parser.add_argument(
        '--skip-charset',
        action='store_true',
        dest='charset',
        help='Whether to ignore the difference of "CHARSET=[a-z0-9]+"'
    )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
        help='Show command version'
    )


def parse_options(args: Any = None) -> CliOption:
    parser = get_parser()
    setup_options(parser)
    options = vars(parser.parse_args(args))
    return CliOption(**options)
