from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pymysql
from pymysql.connections import Connection as PyMySQLConnection

from sqldiffer.db.credential import Credential
from sqldiffer.db.sql import SHOW_CREATE_TABLE, SHOW_TABLES
from sqldiffer.exceptions import DbConnectError
from sqldiffer.logger import get_logger


logger = get_logger(__name__)


@dataclass
class Connection:
    cred: Credential

    read_timeout: int = 60
    connect_timeout: int = 30
    charset: str = 'utf8mb4'

    _conn: Optional[PyMySQLConnection] = field(init=False, default=None)

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    @property
    def conn(self) -> PyMySQLConnection:
        if self._conn is None:
            self._conn = self.connect()
        return self._conn

    def connect(self) -> PyMySQLConnection:
        if self._conn:
            return self._conn

        try:
            self._conn = pymysql.connect(
                host=self.cred.host,
                port=self.cred.port,
                user=self.cred.user,
                password=self.cred.password,
                db=self.cred.database,
                charset=self.charset,
                cursorclass=pymysql.cursors.DictCursor,
                read_timeout=self.read_timeout,
                connect_timeout=self.connect_timeout,
            )
            return self._conn
        except Exception as err:
            raise DbConnectError(err)

    def fetch(
            self,
            sql: str,
            *,
            params: Optional[Dict[str, str]] = None,
            whole: bool = False) -> Any:
        with self.conn.cursor() as cursor:
            cursor.execute(sql, args=params)

            if whole:
                return cursor.fetchall()
            return cursor.fetchone()

    def get_tables(self) -> Optional[List[str]]:
        raw_results = self.fetch(SHOW_TABLES, whole=True)

        if not raw_results:
            return None

        return [
            result[f'Tables_in_{self.cred.database}']
            for result in raw_results]

    def get_schema(self, table: str) -> Optional[str]:
        try:
            raw_result = self.fetch(
                SHOW_CREATE_TABLE.format(table=table), whole=False)
        except pymysql.ProgrammingError as err:
            logger.error(err)
            return None

        if isinstance(raw_result, dict) is False \
                or (sql := raw_result.get('Create Table')):
            return None
        return sql
