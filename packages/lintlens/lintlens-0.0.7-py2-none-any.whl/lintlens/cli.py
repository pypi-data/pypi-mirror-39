#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import argparse
import codecs
import sys

import lintlens
from .git import get_diff_lines
from .lint.unix import parse_lint_line, ParseError
from .utils import check_line_overlap_hunks


def handle_range(revision_range, lint_lines):
    diff_lines = {}
    parse_errors = []
    for filename, hunks in get_diff_lines(revision_range):
        diff_lines[filename[1]] = hunks

    for lint_line in lint_lines:
        try:
            lint_entry = parse_lint_line(lint_line)
        except ParseError as e:
            parse_errors.append(e)
            continue

        # skip file not changed in revision_range
        if lint_entry.filename not in diff_lines:
            continue

        hunks = diff_lines[lint_entry.filename]
        if check_line_overlap_hunks(lint_entry.line, hunks, threshold=1):
            print(lint_line, end='')

    for parse_error in parse_errors:
        print(str(parse_error).strip('\n'), file=sys.stderr)


def read_file_lines(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines


def main():
    parser = argparse.ArgumentParser(prog='lintlens')
    parser.add_argument('--version', action='version', version='%(prog)s ' + str(lintlens.__version__))
    parser.add_argument('revision_range',
                        help='Include changes in the specified revision range. '
                             'Example: "master..HEAD".'
                        )
    parser.add_argument('input_filename',
                        help='Input filename')

    args = parser.parse_args()

    lint_lines = read_file_lines(args.input_filename)

    handle_range(args.revision_range, lint_lines)


if __name__ == "__main__":
    main()
