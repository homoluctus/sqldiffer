import sys

from sqldiffer.cli import parse_options
from sqldiffer.db.connection import Connection
from sqldiffer.differ import Differ, Skipper
from sqldiffer.exceptions import DbConnectError
from sqldiffer.logger import get_logger


logger = get_logger(__name__)


def run() -> None:
    options = parse_options()
    source_conn = Connection(options.source)

    try:
        source_conn.connect()
    except DbConnectError as err:
        logger.error(err)
        logger.error('Failed to connect to server1')
        sys.exit(1)

    tables = source_conn.get_tables()
    if not tables:
        source_conn.close()
        logger.error('Not Found tables on server1')
        return

    target_conn = Connection(options.target)
    try:
        target_conn.connect()
    except DbConnectError as err:
        source_conn.close()
        logger.error(err)
        logger.error('Failed to connect to server2')
        sys.exit(1)

    skipper = Skipper(
        auto_increment=options.auto_increment,
        charset=options.charset)

    for table in tables:
        source = source_conn.get_schema(table) or ''
        target = target_conn.get_schema(table) or ''

        differ = Differ(source, target, skipper=skipper)
        if differ.check() is False:
            try:
                differ.to_html(f'{table}.html', options.output_dir)
            except Exception as err:
                logger.error(err)

    source_conn.close()
    target_conn.close()


def main() -> None:
    try:
        run()
    except KeyboardInterrupt:
        logger.error('Abort')
        sys.exit(1)
    except Exception as err:
        logger.error(err)
        sys.exit(1)


if __name__ == '__main__':
    main()
