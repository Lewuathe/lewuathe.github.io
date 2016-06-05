#!/usr/bin/env python

import sys
import os

def append_blog(file_name):
    new_lines = []
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            if line == 'layout: post\n':
                new_lines.append(line)
                new_lines.append('blog: true\n')
            else:
                new_lines.append(line)

    with open(file_name + '.tmp', 'w') as f:
        for line in new_lines:
            f.write(line)

    os.rename(file_name + '.tmp', file_name)


if __name__ == "__main__":
    append_blog(sys.argv[1])
