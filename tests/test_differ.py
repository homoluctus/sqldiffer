import filecmp
from pathlib import Path

import pytest

from sqldiffer.differ import Differ, Skipper


SOURCE = '''CREATE TABLE `sqldiffer` (
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(10) DEFAULT homoluctus
) ENGINE=InnoDB AUTO_INCREMENT=100 CHARSET=utf8
'''

TARGET_DIFF = '''CREATE TABLE `sqldiffer` (
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(10) DEFAULT system
) ENGINE=InnoDB AUTO_INCREMENT=105 CHARSET=utf8
'''

TARGET_DIFF_INCREMENT = '''CREATE TABLE `sqldiffer` (
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(10) DEFAULT homoluctus
) ENGINE=InnoDB AUTO_INCREMENT=105 CHARSET=utf8
'''

TARGET_DIFF_CHARSET = '''CREATE TABLE `sqldiffer` (
    `id` INT(10) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(10) DEFAULT homoluctus
) ENGINE=InnoDB AUTO_INCREMENT=100 CHARSET=aaaa
'''


@pytest.mark.parametrize(
    'source, target, skipper, expectation',
    (
        (SOURCE, SOURCE, Skipper(), True),
        (SOURCE, SOURCE, Skipper(auto_increment=True), True),
        (SOURCE, SOURCE, Skipper(charset=True), True),
        (SOURCE, SOURCE, Skipper(auto_increment=True, charset=True), True),
        (SOURCE, TARGET_DIFF, Skipper(), False),
        (SOURCE, TARGET_DIFF, Skipper(auto_increment=True), False),
        (SOURCE, TARGET_DIFF, Skipper(charset=True), False),
        (SOURCE, TARGET_DIFF, Skipper(
            auto_increment=True, charset=True), False),
        (SOURCE, TARGET_DIFF_INCREMENT, Skipper(), False),
        (SOURCE, TARGET_DIFF_INCREMENT, Skipper(auto_increment=True), True),
        (SOURCE, TARGET_DIFF_INCREMENT, Skipper(charset=True), False),
        (SOURCE, TARGET_DIFF_INCREMENT, Skipper(
            auto_increment=True, charset=True), True),
        (SOURCE, TARGET_DIFF_CHARSET, Skipper(), False),
        (SOURCE, TARGET_DIFF_CHARSET, Skipper(auto_increment=True), False),
        (SOURCE, TARGET_DIFF_CHARSET, Skipper(charset=True), True),
        (SOURCE, TARGET_DIFF_CHARSET, Skipper(
            auto_increment=True, charset=True), True)
    )
)
def test_differ_check(
        source: str,
        target: str,
        skipper: Skipper,
        expectation: bool):
    actual_result = Differ(source, target, skipper).check()
    assert actual_result is expectation


EXPECTED_FILE = f'{Path(__file__).parent}/result.html'


@pytest.mark.parametrize(
    'source, target, expected_file',
    ((SOURCE, TARGET_DIFF, EXPECTED_FILE),)
)
def test_differ_html(
        source: str,
        target: str,
        expected_file: str):
    filename = 'actual_result.html'
    Differ(source, target).to_html(filename)

    assert filecmp.cmp(filename, expected_file, shallow=False) is True

    Path(filename).unlink()
