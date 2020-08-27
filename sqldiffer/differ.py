import os
import re
from dataclasses import dataclass
from difflib import HtmlDiff
from typing import Pattern


AUTO_INCREMENT_REGEX = re.compile(r' AUTO_INCREMENT=[0-9]+')
CHARSET_REGEX = re.compile(r' CHARSET=[a-z0-9]+')


@dataclass
class Skipper:
    auto_increment: bool = False
    charset: bool = False

    def _innter_skip(self, target: str, pattern: Pattern) -> str:
        m = re.search(pattern, target)

        if not m:
            return target
        return target[:m.start()] + target[m.end():]

    def skip(self, target: str) -> str:
        if not target:
            return target

        if self.auto_increment:
            target = self._innter_skip(target, AUTO_INCREMENT_REGEX)

        if self.charset:
            target = self._innter_skip(target, CHARSET_REGEX)

        return target


@dataclass
class Differ:
    source: str
    target: str
    skipper: Skipper = Skipper()

    def check(self) -> bool:
        source = self.skipper.skip(self.source)
        target = self.skipper.skip(self.target)

        if source == target:
            return True
        return False

    def to_html(self, filename: str, output_dir: str = os.getcwd()) -> None:
        source = self.source.splitlines(keepends=True)
        target = self.target.splitlines(keepends=True)

        os.makedirs(output_dir, mode=0o755, exist_ok=True)
        diff = HtmlDiff().make_file(source, target)
        with open(filename, mode='wt') as fd:
            fd.write(diff)
