#!/usr/bin/python

from __future__ import print_function
import os
import sys
from io import FileIO
import re


def main():
    errors = False
    for file_name in sys.argv[1:]:
        with FileIO(file_name, 'r') as file_handle:
            data = file_handle.readall()
            if '\r' in data:
                print(file_name + " contains DOS line endings", file=sys.stderr)
                errors = True
            if '\t' in data and file_name.endswith('.py'):
                print(file_name + " contains tabs", file=sys.stderr)
                errors = True
            if 'console.log' in data:
                print(file_name + " contains console.log calls", file=sys.stderr)
                errors = True
            if data.startswith('#!') and not os.access(file_name, os.X_OK):
                print(file_name + " contains shebang but is not executable", file=sys.stderr)
                errors = True
            if not data.startswith('#!') and os.access(file_name, os.X_OK):
                print(file_name + " is executable but does not contain shebang", file=sys.stderr)
                errors = True
            decoded_data = None
            try:
                decoded_data = data.decode('utf-8')
            except UnicodeDecodeError:
                print(file_name + " is not utf-8", file=sys.stderr)
                errors = True
            copyright_list = re.findall("Copyright.*by Adaptive Computing Enterprises, Inc", decoded_data)
            for line in copyright_list:
                if not re.match(u"Copyright \u00A9 \d\d\d\d", line):
                    print(file_name + " contains bogus copyright line", file=sys.stderr)
                    errors = True
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
