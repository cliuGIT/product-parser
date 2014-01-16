#!/usr/bin/env python
__author__ = 'cliu'

import sys
import time

from productparser import get, ensure_console, logger


def usage():
    print """
    Product Parser batch test.

    Usage 1:
    ./test.py

    Usage 2:
    ./test.py <test_url_filename>
"""


def main(filename):
    errors = list()
    url_count = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                logger.info('-' * 60)
                url_count += 1
                title, price, srcs = get(line.strip())
                logger.info(ensure_console(title))
                logger.info(price)
                for src in srcs:
                    logger.info(src)
                if not (title and price and srcs):
                    errors.append(line)

    # print test summary
    time.sleep(0.3)
    print '-' * 30, 'Error URLs', '-' * 30
    for url in errors:
        print url
    print 'Total:'.rjust(10), url_count
    print 'Errors:'.rjust(10), len(errors)

    # write error urls to a new file
    if errors:
        with open(filename + '.errors', 'w') as f:
            f.write('\n'.join(errors))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        filename = 'testurl.txt'
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        usage()
        sys.exit()

    main(filename)