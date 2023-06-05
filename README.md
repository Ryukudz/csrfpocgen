# CSRFPOCGEN

Generates CSRF POC for application/x-www-form-urlencoded Content-type, ill improve it to support json & multipart/form-data soon.

## Installation

```sh
git clone https://github.com/Ryukudz/csrfpocgen
```

## Usage

```sh
python3 csrfpocgen.py -h
```

This will display help for the tool.

```yaml
usage: csrfpocgen.py [-h] [-f FILE]

CSRF POC Generator

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the Burp Suite request file
```

the script takes a Burp Suite file request path as an argument using -f or --file option.
