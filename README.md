# sqldiffer

Check the difference of MySQL schema (CREATE TABLE)

<!-- TOC depthFrom:2 -->

- [Feature](#feature)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
  - [Check the differences](#check-the-differences)
  - [Ignore charset](#ignore-charset)
  - [Ignore auto_increment and charset](#ignore-auto_increment-and-charset)

<!-- /TOC -->

## Feature

- Check the difference of MySQL schema
  - Compare CREATE TABLE
  - Choose whether to ignore AUTO_INCREMENT and CHARSET
- Output HTML
  - Save the difference for each table in HTML (Click [here](./tests/result.html) for sample)

## Installation

```bash
pip install sqldiffer
```

## Usage

```
sqldiffer -h
usage: sqldiffer [-h] --server1 SERVER1 --server2 SERVER2 [-o OUTPUT_DIR] [--skip-auto-increment] [--skip-charset] [-V]

Check the difference of MySQL schema (CREATE TABLE)

optional arguments:
  -h, --help            show this help message and exit
  --server1 SERVER1     Comparison source. [Format] user:password@host:port/database
  --server2 SERVER2     Comparison target. [Format] user:password@host:port/database
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory to save files. Default is current directory.
  --skip-auto-increment
                        Whether to ignore the difference of "AUTO_INCREMENT=[0-9]+"
  --skip-charset        Whether to ignore the difference of "CHARSET=[a-z0-9]+"
  -V, --version         Show command version
```

## Examples

### Check the differences

```bash
sqldiffer --server1 homoluctus:test@aroundtheworld:3306/aaa \
          --server2 homoluctus:test@anothersky:3306/aaa
```

### Ignore charset

```bash
sqldiffer --server1 homoluctus:test@aroundtheworld:3306/aaa \
          --server2 homoluctus:test@anothersky:3306/aaa \
          --skip-charset
```

### Ignore auto_increment and charset

```bash
sqldiffer --server1 homoluctus:test@aroundtheworld:3306/aaa \
          --server2 homoluctus:test@anothersky:3306/aaa \
          --skip-auto-increment \
          --skip-charset
```
