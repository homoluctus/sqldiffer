import re
from dataclasses import dataclass
from typing import Optional


DB_CREDENTIAL_REGEX = re.compile(
    r'(?P<user>.*):(?P<password>.*)'
    + r'@(?P<host>.*):(?P<port>[0-9]+)/(?P<database>.*)')


@dataclass
class Credential:
    user: str
    password: str
    host: str
    port: int
    database: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.port, int) is False:
            self.port = int(self.port)

    @classmethod
    def parse(cls, target: str) -> Optional['Credential']:
        m = re.match(DB_CREDENTIAL_REGEX, target)

        if m is None:
            return None

        result = m.groupdict()
        return cls(**result)  # type: ignore
